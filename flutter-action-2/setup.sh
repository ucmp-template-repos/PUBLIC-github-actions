#!/bin/bash

OS_NAME=$(echo "$RUNNER_OS" | awk '{print tolower($0)}')
MANIFEST_BASE_URL="https://storage.googleapis.com/flutter_infra_release/releases"
MANIFEST_URL="${MANIFEST_BASE_URL}/releases_${OS_NAME}.json"

# convert version like 2.5.x to 2.5
normalize_version() {
  if [[ $1 == *x ]]; then
    echo ${1::-2}
  else
    echo $1
  fi
}

latest_version() {
  jq --arg channel "$1" '.releases | map(select(.channel==$channel)) | first'
}

wildcard_version() {
  if [[ $1 == any ]]; then
    jq --arg version "^$2" '.releases | map(select(.version | test($version))) | first'
  else
    jq --arg channel "$1" --arg version "^$2" '.releases | map(select(.channel==$channel) | select(.version | test($version))) | first'
  fi
}

get_version() {
  if [[ -z $2 ]]; then
    latest_version $1
  else
    wildcard_version $1 $2
  fi
}

get_version_manifest() {
  releases_manifest=$(curl --silent --connect-timeout 15 --retry 5 $MANIFEST_URL)
  version_manifest=$(echo $releases_manifest | get_version $1 $(normalize_version $2))

  if [[ $version_manifest == null ]]; then
    # fallback through legacy version format
    echo $releases_manifest | wildcard_version $1 "v$(normalize_version $2)"
  else
    echo $version_manifest
  fi
}

download_archive() {
  archive_url="$MANIFEST_BASE_URL/$1"
  archive_name=$(basename $1)
  archive_local="$RUNNER_TEMP/$archive_name"

  curl --connect-timeout 15 --retry 5 $archive_url >$archive_local

  # Create the target folder
  mkdir -p "$2"

  if [[ $archive_name == *zip ]]; then
    unzip -q -o "$archive_local" -d "$RUNNER_TEMP"
    # Remove the folder again so that the move command can do a simple rename
    # instead of moving the content into the target folder.
    # This is a little bit of a hack since the "mv --no-target-directory"
    # linux option is not available here
    rm -r "$2"
    mv ${RUNNER_TEMP}/flutter "$2"
  else
    tar xf "$archive_local" -C "$2" --strip-components=1
  fi

  rm $archive_local
}

transform_path() {
  if [[ $OS_NAME == windows ]]; then
    echo $1 | sed -e 's/^\///' -e 's/\//\\/g'
  else
    echo $1
  fi
}

SDK_CACHE=""

while getopts 'c:' flag; do
  case "${flag}" in
  c) SDK_CACHE="$(transform_path $OPTARG)" ;;
  ?) exit 2 ;;
  esac
done

CHANNEL="${@:$OPTIND:1}"
VERSION="${@:$OPTIND+1:1}"

if [[ $OS_NAME == windows ]]; then
  PUB_CACHE="${USERPROFILE}\\.pub-cache"
else
  PUB_CACHE="${HOME}/.pub-cache"
fi

if [[ ! -x "${SDK_CACHE}/bin/flutter" ]]; then
  if [[ $CHANNEL == master ]]; then
    git clone -b master https://github.com/flutter/flutter.git "$SDK_CACHE"
  else
    VERSION_MANIFEST=$(get_version_manifest $CHANNEL $VERSION)

    if [[ $VERSION_MANIFEST == null ]]; then
      echo "Unable to determine Flutter version for $CHANNEL $VERSION"
      exit 1
    fi

    ARCHIVE_PATH=$(echo $VERSION_MANIFEST | jq -r '.archive')
    download_archive "$ARCHIVE_PATH" "$SDK_CACHE"
  fi
fi

echo "FLUTTER_ROOT=${SDK_CACHE}" >>$GITHUB_ENV
echo "PUB_CACHE=${PUB_CACHE}" >>$GITHUB_ENV

echo "${SDK_CACHE}/bin" >>$GITHUB_PATH
echo "${SDK_CACHE}/bin/cache/dart-sdk/bin" >>$GITHUB_PATH
echo "${PUB_CACHE}/bin" >>$GITHUB_PATH
