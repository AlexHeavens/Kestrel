#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

test_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
project_dir="${test_dir}/.."
src_dir="${project_dir}/src"
test_build_dir="${test_dir}/build"

rm --recursive --force "${test_build_dir}/*" # clean up prior tests

python "${src_dir}/obscura.py" --build-dir "${test_build_dir}"

if [[ -f "${test_build_dir}/obscura.html" ]]; then
	echo 'obscura.html created, smoke test passed'
else
	echo 'obscura.html not created, smoke test failed'
fi
