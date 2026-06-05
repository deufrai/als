#!/usr/bin/env python
# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess
from pathlib import Path


def main():
    project_root_path = Path(__file__).parent.parent
    als_project_file = project_root_path / "als.pro"

    print("Updating translation files\n" + "=" * 27)

    command = [
        "pylupdate5",
        "-verbose",
        "-noobsolete",
        str(als_project_file),
    ]

    print("Executing command : {}".format(" ".join(command)))
    completed_process = subprocess.run(command)

    if completed_process.returncode != 0:
        raise RuntimeError(f"Failed to update translation files. Command returned with code {completed_process.returncode}")

if __name__ == "__main__":
    main()
