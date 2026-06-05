#!/usr/bin/env python
# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess
from pathlib import Path


def main():
    project_root_path = Path(__file__).parent.parent
    i18n_path = project_root_path / "i18n"
    resources_path = project_root_path / "src" / "resources" / "i18n"

    print("Releasing translation files\n" + "=" * 27)

    ts_file_paths = sorted(i18n_path.glob("*.ts"))
    if not ts_file_paths:
        raise RuntimeError("No TS files found in {}".format(i18n_path))

    for ts_file_path in ts_file_paths:
        qm_file_path = resources_path / ts_file_path.with_suffix(".qm").name
        command = [
            "lrelease",
            str(ts_file_path),
            "-qm",
            str(qm_file_path),
        ]

        print("Executing command : {}".format(" ".join(command)))
        completed_process = subprocess.run(command)
        if completed_process.returncode != 0:
            raise RuntimeError("Translation release failed for {}".format(ts_file_path))


if __name__ == "__main__":
    main()
