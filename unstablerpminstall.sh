ARTIFACTORY_USER=arka-pramanik-hpe
ARTIFACTORY_TOKEN=
STREAM=unstable
HTTP_PROXY=http://hpeproxy.its.hpecorp.net:443 zypper --plus-repo=https://${ARTIFACTORY_USER}:${ARTIFACTORY_TOKEN}@artifactory.algol60.net/artifactory/csm-rpms/hpe/${STREAM}/noos --no-gpg-checks -n in -y --oldpackage craycli=0.90.1.dev24+gbd5043d-1

