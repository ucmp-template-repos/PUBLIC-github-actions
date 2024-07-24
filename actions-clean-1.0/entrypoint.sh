#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

# 작업 디렉토리 초기화
rm -rf "${GITHUB_WORKSPACE:?}"/* "${GITHUB_WORKSPACE:?}/.git*"

if test "${RUNNER_DEBUG:-0}" != '1'; then
  set +o xtrace
fi