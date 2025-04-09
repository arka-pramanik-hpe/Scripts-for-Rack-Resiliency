export https_proxy=http://hpeproxy.its.hpecorp.net:80
export http_proxy=http://hpeproxy.its.hpecorp.net:443
export no_proxy=localhost,127.0.0.1,registry.local
export HTTPS_PROXY=$https_proxy
export HTTP_PROXY=$http_proxy
export NO_PROXY=$no_proxy
wget --user arka-pramanik-hpe --password <artficatory-pass> https://artifactory.algol60.net/ui/native/csm-rpms/hpe/stable/sle-15sp4/craycli/src/craycli-0.82.8-1.src.rpm
unset https_proxy
unset http_proxy
unset no_proxy
unset HTTPS_PROXY
unset HTTP_PROXY
unset NO_PROXY
