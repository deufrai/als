set -e

python -m venv venv
. venv/Scripts/activate

python -m pip install --upgrade pip
pip install wheel
pip install setuptools
pip install $(grep numpy ci/builds/build_dist_amd64_win_req.txt)
pip install -r ci/builds/build_dist_amd64_win_req.txt
pip install --upgrade astroid==2.2.0
python setup.py develop

VERSION=$(echo ${ALS_VERSION_STRING} | sed "s/^v//")
echo "version = \"${VERSION}\"" > src/als/version.py

VERPARTS=(${VERSION//-/ })
VERNUM=${VERPARTS[0]}
DOTCOUNT=$(grep -o '\.' <<< "${VERNUM}" | grep -c .)

for (( c=${DOTCOUNT}; c<3; c++ ))
do
  VERNUM=${VERNUM}.0
done

VERCODE=$(echo ${VERNUM} | sed "s/\./, /g")

echo "Building Windows installer ..."

sed -e "s/##VERSION##/${VERSION}/g" \
    -e "s/##VERCODE##/${VERCODE}/g" \
    ci/builds/file_version_info_template.txt > file_version_info.txt

pyinstaller -i src/resources/als_logo.ico \
            -n als \
            --windowed \
            --version-file=file_version_info.txt \
            --add-data 'src/resources/qt.conf:.' \
            src/als/main.py

# Build the Inno Setup installer
ISCC "//DMyAppVersion=${ALS_VERSION_STRING}" "//DMyAppName=als" ci/builds/als_win_installer.iss
echo "ALS installer build completed OK."
