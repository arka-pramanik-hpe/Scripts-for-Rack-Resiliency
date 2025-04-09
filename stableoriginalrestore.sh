ARTIFACTORY_USER=arka-pramanik-hpe
ARTIFACTORY_TOKEN=
STREAM=stable
HTTP_PROXY=http://hpeproxy.its.hpecorp.net:443 zypper --plus-repo=https://${ARTIFACTORY_USER}:${ARTIFACTORY_TOKEN}@artifactory.algol60.net/artifactory/csm-rpms/hpe/${STREAM}/noos --no-gpg-checks -n in -y --oldpackage craycli=0.90.0-1


