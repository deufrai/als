set -e

artifact_name="als-${ALS_VERSION_STRING}.run"

python -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel
pip install -r ci/builds/build_dist_amd64_linux_req.txt

python setup.py develop

echo "version = \"${ALS_VERSION_STRING}\"" > src/als/version.py

echo "Building package ${artifact_name} ..."
pyinstaller -F -n "${artifact_name}" --windowed --hidden-import='scipy._lib.array_api_compat.numpy.fft' src/als/main.py --hiddenimport=scipy.special._special_ufuncs
mv dist/${artifact_name} .
echo "Build of package ${artifact_name} completed OK."

