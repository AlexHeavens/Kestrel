#!/usr/bin/env bash
# Start the real web server from the kestrel:local image (make build_docker) and
# fetch the map page and the health endpoint, as a browser and a load balancer do.

set -o errexit
set -o pipefail
set -o nounset

image="${KESTREL_IMAGE:-kestrel:local}"

container=$(docker run --detach --publish 127.0.0.1::8080 "${image}")
trap 'docker rm --force "${container}" >/dev/null' EXIT
port=$(docker port "${container}" 8080/tcp | head --lines=1 | sed 's/.*://')
base_url="http://127.0.0.1:${port}"

curl --fail --silent --show-error --retry 20 --retry-delay 1 --retry-connrefused \
	--output /dev/null "${base_url}/health"

health=$(curl --fail --silent --show-error "${base_url}/health")
if [[ "${health}" != "OK" ]]; then
	echo "e2e test failed: /health returned '${health}', expected 'OK'"
	exit 1
fi

page=$(curl --fail --silent --show-error "${base_url}/")
for expected in leaflet "Scottish National Party"; do
	if ! grep --quiet --fixed-strings "${expected}" <<<"${page}"; then
		echo "e2e test failed: the map page does not contain '${expected}'"
		exit 1
	fi
done

echo 'e2e test passed: / serves the map and /health returns OK'
