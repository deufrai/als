# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

set -e

venv_name="venv"

python3 -m venv "${venv_name}"
. "${venv_name}"/bin/activate
pip install -r ci/builds/build_dist_arm64_osx_req.txt

python setup.py develop
pytest -vv -ra --tb=short --durations=10 --junit-xml=tests_report.xml
