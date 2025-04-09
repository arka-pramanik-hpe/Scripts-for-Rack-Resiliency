
export NEXUS_USERNAME="$(kubectl -n nexus get secret nexus-admin-credential --template {{.data.username}} | base64 -d)"
export NEXUS_PASSWORD="$(kubectl -n nexus get secret nexus-admin-credential --template {{.data.password}} | base64 -d)"
export ARTIFACTORY_USER="arka-pramanik-hpe"
export ARTIFACTORY_TOKEN=""

export IMAGE="csm-docker/unstable/cray-rrs-api:1.0.0-20250409073820_c7f17c7"
 podman run  -v ./dir:/images --rm --network host quay.io/skopeo/stable:v1 copy --src-tls-verify=false --src-creds "${ARTIFACTORY_USER}:${ARTIFACTORY_TOKEN}" --dest-creds "${NEXUS_USERNAME}:${NEXUS_PASSWORD}" --dest-tls-verify=false docker-archive:/images/sma-rsyslog.tar docker://registry.local/artifactory.algol60.net/$IMAGE