# this script builds a full dsitribution on a RPI4
#
# BEWARE : this is still experimental
#
# USAGE : MUST be called from the top of als sources dir
#
#######################################################################
set -e

if [ ! -d venv ]
then
  python3 -m venv --system-site-packages venv
fi

. venv/bin/activate

pip install --upgrade pip
pip install --upgrade wheel
pip install setuptools
pip install /work/bamboo/pip-cache/wheels/60/50/55/2ba3115ad93b55e68a729da36185eb45ad7cfba657a25acd54/rawpy-0.13.1-cp37-cp37m-linux_armv7l.whl
patch < ci/rpi4_requirements.patch
pip install -I -r requirements.txt
pip install --upgrade astroid==2.2.0

python setup.py develop

./ci/pylint.sh

tags=$(git tag --contains HEAD)

if [ -z "${tags}" ]
then
  tag_count=0
else
  tag_count=$(echo "${tags}" | wc -l)
fi

if [ ${tag_count} -gt 1 ]
then
    echo "More that one tag exist on HEAD. Cancelling ..."
    exit 1
fi

if [ $tag_count -eq 1 ]
then
  VERSION=$(git tag --contains HEAD)
else
  VERSION=$(grep version src/als/version.py | cut -d'"' -f2)-$(git rev-parse --short HEAD)
fi

echo "version = \"${VERSION}\"" > src/als/version.py

echo "Building package version: ${VERSION}"

pyinstaller -n als-${VERSION} --windowed --hidden-import='pkg_resources.py2_warn' src/als/main.py

cd dist

tar zcf als-${VERSION}.tgz als-${VERSION}
