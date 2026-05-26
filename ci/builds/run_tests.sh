set -e

venv_name="venv"

python3 -m venv "${venv_name}"
. "${venv_name}"/bin/activate
pip install -r ci/builds/build_dist_arm64_osx_req.txt

python setup.py develop
pytest -q
