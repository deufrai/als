from __future__ import annotations

import csv
import re
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SECTION = "=" * 50
SUB_SECTION = "-" * 50

PROCESSING_FUNCTIONS = {
    "read_disk_image()",
    "RemoveDark.process_image()",
    "RemoveFlat.process_image()",
    "HotPixelRemover.process_image()",
    "Debayer.process_image()",
    "Standardize.process_image()",
    "Stacker._find_transformation()",
    "Stacker._apply_transformation()",
    "Stacker._align_image()",
    "Stacker._stack_image()",
    "AutoStretch.process_image()",
    "Levels.process_image()",
    "ColorBalance.process_image()",
    "ImageSaver._save_image()",
}

SESSION_FLOAT_MARKERS = {
    "*SD-RATIO*": "ratio",
    "*SD-ROT*": "rotation",
    "*SD-SCALE*": "scale",
    "*SD-MATCHES*": "matches",
    "*SD-REQ*": "req_matches",
    "*SD-Q-PRE*": "q_pre",
    "*SD-Q-STA*": "q_stack",
    "*SD-FRMTIME*": "frm_total",
    "*SD-Q-POST*": "q_post",
    "*SD-Q-SAV*": "q_save",
    "*SM-MEM*": "memory",
}

TRANSLATION_PATTERN = re.compile(r"\[\s*(\S+)\s+(\S+)\s*\]")


@dataclass(frozen=True)
class LogEntry:
    raw: str
    tokens: list[str]

    @property
    def thread(self) -> str:
        return self.tokens[0]

    @property
    def module(self) -> str:
        return self.tokens[1]

    @property
    def level(self) -> str:
        return self.tokens[2]

    @property
    def timestamp(self) -> str:
        return " ".join(self.tokens[3:5])

    @property
    def function_name(self) -> str:
        return self.tokens[5]


def main() -> None:
    args = parse_args()
    csv_out_folder = Path(args.out_folder)
    csv_out_folder.mkdir(parents=True, exist_ok=True)

    print(f"Parsing ALS log file {args.in_log}...")
    entries = load_log_entries(Path(args.in_log))
    print(f"Reassembled {len(entries)} log entries")

    function_returns = [entry for entry in entries if "returned" in entry.raw]
    print(f"Collected {len(function_returns)} function returns")

    export_csv(
        title="Exporting every function return...",
        file_name="global_returns",
        out_folder=csv_out_folder,
        fieldnames=["timestamp", "thread", "module", "name", "ret_value", "elapsed"],
        rows=extract_function_returns(function_returns),
    )

    processing_returns = [
        entry for entry in function_returns
        if entry.function_name in PROCESSING_FUNCTIONS
    ]
    export_csv(
        title="Exporting processing functions timings...",
        file_name="processing_timings",
        out_folder=csv_out_folder,
        fieldnames=["timestamp", "thread", "module", "name", "ret_value", "elapsed"],
        rows=extract_function_returns(processing_returns),
    )

    export_csv(
        title="Exporting session data...",
        file_name="session",
        out_folder=csv_out_folder,
        fieldnames=["timestamp", "type", "value"],
        rows=extract_session_data(entries),
    )

    issue_entries = [
        entry for entry in entries
        if entry.level in {"ERROR", "WARNING"}
    ]
    export_csv(
        title="Exporting issues...",
        file_name="issues",
        out_folder=csv_out_folder,
        fieldnames=["timestamp", "thread", "module", "level", "message"],
        rows=extract_issues(issue_entries),
    )


def parse_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "-i",
        "--in_log",
        help="path to the als.log file",
        default=Path.home() / "als.log",
    )
    arg_parser.add_argument(
        "-o",
        "--out_folder",
        help="path to the folder where CSV files are written",
        default="./csv",
    )
    return arg_parser.parse_args()


def load_log_entries(log_file: Path) -> list[LogEntry]:
    with open(log_file) as logfile:
        lines = logfile.readlines()

    assembled_entries = []
    current_entry = "START START START"

    for line in lines:
        line = line.replace("\n", "")
        if line.startswith("="):
            assembled_entries.append(current_entry)
            current_entry = line[1:]
        else:
            current_entry += line

    assembled_entries.append(current_entry)
    return [parse_log_entry(entry) for entry in assembled_entries]


def parse_log_entry(raw_entry: str) -> LogEntry:
    return LogEntry(raw=raw_entry, tokens=tokenize(raw_entry))


def extract_function_returns(entries: Iterable[LogEntry]) -> list[dict[str, object]]:
    return [
        {
            "timestamp": entry.timestamp,
            "thread": entry.thread,
            "module": entry.module,
            "name": entry.function_name,
            "ret_value": entry.tokens[7:-3],
            "elapsed": entry.tokens[-2],
        }
        for entry in entries
    ]


def extract_issues(entries: Iterable[LogEntry]) -> list[dict[str, str]]:
    return [
        {
            "timestamp": entry.timestamp,
            "thread": entry.thread,
            "module": entry.module,
            "level": entry.level,
            "message": " ".join(entry.tokens[5:]),
        }
        for entry in entries
    ]


def extract_session_data(entries: Iterable[LogEntry]) -> list[dict[str, object]]:
    rows = []

    for entry in entries:
        if "*SD-TRANS*" in entry.raw:
            rows.extend(extract_translation(entry))
            continue

        if "*SD-ALIGNOK*" in entry.raw:
            rows.append(session_row(entry, "align", 1.0 if entry.tokens[-1] == "Accepted" else 0.0))
            continue

        for marker, event_type in SESSION_FLOAT_MARKERS.items():
            if marker in entry.raw:
                rows.append(session_row(entry, event_type, float(entry.tokens[-1])))
                break

    return rows


def extract_translation(entry: LogEntry) -> list[dict[str, object]]:
    translation_match = TRANSLATION_PATTERN.search(entry.raw)
    return [
        session_row(entry, "x_trans", float(translation_match.group(1))),
        session_row(entry, "y_trans", float(translation_match.group(2))),
    ]


def session_row(entry: LogEntry, event_type: str, value: float) -> dict[str, object]:
    return {
        "timestamp": entry.timestamp,
        "type": event_type,
        "value": value,
    }


def export_csv(
    title: str,
    file_name: str,
    out_folder: Path,
    fieldnames: list[str],
    rows: list[dict[str, object]],
) -> None:
    print(SECTION)
    print(title)
    print(SUB_SECTION)
    write_csv(file_name, out_folder, fieldnames, rows)


def write_csv(
    file_name: str,
    out_folder: Path,
    fieldnames: list[str],
    rows: list[dict[str, object]],
) -> None:
    dest_path = out_folder / f"{file_name}.csv"
    with open(dest_path, "w", newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, delimiter=";", fieldnames=fieldnames)
        csv_writer.writeheader()

        csv_writer.writerows(rows)

    print(f"report {str(dest_path):<35} OK")


def tokenize(line: str) -> list[str]:
    return re.split(r"\s+", line)


if __name__ == "__main__":
    main()
