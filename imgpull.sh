#!/bin/bash
set -euo pipefail
source .env

NEXUS_USERNAME="$(kubectl -n nexus get secret nexus-admin-credential --template {{.data.username}} | base64 -d)"

NEXUS_PASSWORD="$(kubectl -n nexus get secret nexus-admin-credential --template {{.data.password}} | base64 -d)"


IMAGES=(
"csm-docker/unstable/cray-rrs-api:1.0.0-20250408181846_7e6c7e5"
)
for IMAGE in "${IMAGES[@]}"; do
    mkdir ./dir
    export https_proxy=http://hpeproxy.its.hpecorp.net:443
    export http_proxy=http://hpeproxy.its.hpecorp.net:443
    export no_proxy=localhost,127.0.0.1,registry.local
    export HTTPS_PROXY=$https_proxy
    export HTTP_PROXY=$http_proxy
    export NO_PROXY=$no_proxy
    podman run -v ./dir:/images --rm --network host quay.io/skopeo/stable:v1 copy --src-tls-verify=false --src-creds "${ARTIFACTORY_USER}:${ARTIFACTORY_TOKEN}" --dest-creds "${NEXUS_USERNAME}:${NEXUS_PASSWORD}" --dest-tls-verify=false docker://artifactory.algol60.net/$IMAGE docker-archive:/images/sma-rsyslog.tar
    unset http_proxy
    unset no_proxy
    unset HTTPS_PROXY
    unset HTTP_PROXY
    unset NO_PROXY
    podman run  -v ./dir:/images --rm --network host quay.io/skopeo/stable:v1 copy --src-tls-verify=false --src-creds "${ARTIFACTORY_USER}:${ARTIFACTORY_TOKEN}" --dest-creds "${NEXUS_USERNAME}:${NEXUS_PASSWORD}" --dest-tls-verify=false docker-archive:/images/sma-rsyslog.tar docker://registry.local/artifactory.algol60.net/$IMAGE
    rm -rf ./dir
done