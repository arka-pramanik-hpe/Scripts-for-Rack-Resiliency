tar -xvf arka.tar.gz 
cd arka/
rm -rf  craycli-repo/craycli/cray/modules/rrs/swagg*
vi craycli-repo/craycli/cray/modules/rrs/swagger.yaml
source ./craycli-repo/venv/bin/activate
cd craycli-repo/craycli/
export https_proxy=http://hpeproxy.its.hpecorp.net:443
export http_proxy=http://hpeproxy.its.hpecorp.net:443
export no_proxy=localhost,127.0.0.1,registry.local
export HTTPS_PROXY=$https_proxy
export HTTP_PROXY=$http_proxy
export NO_PROXY=$no_proxy
nox -s swagger -- rrs cray/modules/rrs/swagger.yaml 
unset https_proxy
unset http_proxy
unset no_proxy
unset HTTPS_PROXY
unset HTTP_PROXY
unset NO_PROXY
deactivate
cat cray/modules/rrs/swagger3.json
