#!/usr/bin/env python
# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import shutil
import time
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Periodically replay sample subs into an ALS scan folder.")
    parser.add_argument(
        "source_folder",
        type=Path,
        help="Folder containing sample subs to copy")
    parser.add_argument(
        "target_folder",
        type=Path,
        help="ALS scan folder to empty and refill")
    parser.add_argument(
        "period",
        type=float,
        help="Delay in seconds between two copied files")
    return parser.parse_args()


def validate_args(source_folder: Path, target_folder: Path, period: float) -> None:
    if not source_folder.is_dir():
        raise ValueError("Source folder does not exist or is not a directory: {}".format(source_folder))

    if not target_folder.is_dir():
        raise ValueError("Target folder does not exist or is not a directory: {}".format(target_folder))

    if period < 0:
        raise ValueError("Period must be greater than or equal to 0")


def delete_target_contents(target_folder: Path) -> None:
    for item_path in target_folder.iterdir():
        if item_path.is_dir() and not item_path.is_symlink():
            shutil.rmtree(str(item_path))
        else:
            item_path.unlink()


def list_source_files(source_folder: Path):
    return sorted(
        item_path for item_path in source_folder.iterdir()
        if item_path.is_file())


def copy_source_files(source_files, target_folder: Path, period: float) -> None:
    for index, source_file_path in enumerate(source_files):
        target_file_path = target_folder / source_file_path.name
        shutil.copy2(str(source_file_path), str(target_file_path))
        print("Copied {} -> {}".format(source_file_path, target_file_path))

        if index < len(source_files) - 1:
            time.sleep(period)


def replay_subs(source_folder: Path, target_folder: Path, period: float) -> None:
    while True:
        source_files = list_source_files(source_folder)
        if not source_files:
            raise ValueError("Source folder contains no files: {}".format(source_folder))

        print("Clearing {}".format(target_folder))
        delete_target_contents(target_folder)

        print("Waiting 2 seconds before replay")
        time.sleep(2)

        copy_source_files(source_files, target_folder, period)


def main():
    args = parse_args()

    try:
        validate_args(args.source_folder, args.target_folder, args.period)
        replay_subs(args.source_folder, args.target_folder, args.period)
    except KeyboardInterrupt:
        print("\nInterrupted")


if __name__ == "__main__":
    main()
