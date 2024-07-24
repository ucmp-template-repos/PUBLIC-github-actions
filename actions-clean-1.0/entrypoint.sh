#!/usr/bin/env bash
set -o errexit -o nounset -o xtrace -o pipefail
shopt -s inherit_errexit nullglob dotglob

# 작업 디렉토리 초기화
rm -rf "${GITHUB_WORKSPACE:?}"/* "${GITHUB_WORKSPACE:?}/.git*"

if test "${RUNNER_DEBUG:-0}" != '1'; then
  set +o xtrace
fi