set -e

venv_name="venv"
artifact_name="als-${ALS_VERSION_STRING}-arm64.dmg"

python3 -m venv "${venv_name}"
. "${venv_name}"/bin/activate
pip install -r ci/builds/build_dist_arm64_osx_req.txt

python setup.py develop

echo "version = \"${ALS_VERSION_STRING}\"" > src/als/version.py

echo "Building package ${artifact_name} ..."

pyinstaller -i src/resources/als_logo.icns \
            -n als \
            --windowed \
            --exclude-module tkinter  \
            src/als/main.py  \
            --hiddenimport=scipy.special._cdflib  \
            --runtime-hook ci/builds/arm64_osx_hook.py
cp -vf /opt/homebrew/Cellar/libpng/1.6.44/lib/libpng16.16.dylib dist/als.app/Contents/MacOS
sed -e "s/##VERSION##/${ALS_VERSION_STRING}/"  ci/builds/Info.plist > dist/als.app/Contents/Info.plist
create-dmg --volname "ALS ${ALS_VERSION_STRING}" \
           --window-pos 200 120 \
           --window-size 500 300 \
           --icon-size 100 \
           --icon "als.app" 120 140 \
           --hide-extension "als.app" \
           --app-drop-link 370 140 \
           --background src/resources/starfield.png \
           ${artifact_name} dist/als.app

echo "Build of package ${artifact_name} completed OK."
