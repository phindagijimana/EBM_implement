"""CLI: check, demo, fit, start, stop, logs."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from ebm_tle import __version__
from ebm_tle import paths
from ebm_tle.demo import run_demo
from ebm_tle.fit import fit_from_csv


def cmd_check() -> int:
    root = paths.ROOT
    py = paths.VENV_PY
    print(f"ebm-tle {__version__}")
    print(f"ROOT={root}")
    print(f"venv_python={py} exists={py.is_file()}")
    try:
        import kde_ebm  # noqa: F401

        print("import kde_ebm: ok")
    except Exception as e:
        print(f"import kde_ebm: FAIL ({e})")
        return 1
    try:
        import pySuStaIn

        loc = Path(pySuStaIn.__file__).resolve().parent
        print(f"import pySuStaIn: ok ({loc})")
    except Exception as e:
        print(f"import pySuStaIn: FAIL ({e})")
        return 1
    return 0


def _ensure_runtime_dirs() -> None:
    paths.RUN_DIR.mkdir(parents=True, exist_ok=True)
    paths.LOG_DIR.mkdir(parents=True, exist_ok=True)


def cmd_start(args: argparse.Namespace) -> int:
    _ensure_runtime_dirs()
    if paths.PID_FILE.is_file():
        try:
            old = int(paths.PID_FILE.read_text().strip())
            os.kill(old, 0)
            print(f"ebm: already running (pid {old}). Stop first or use: ebm logs")
            return 1
        except (OSError, ProcessLookupError, ValueError):
            paths.PID_FILE.unlink(missing_ok=True)

    out = Path(args.output) if args.output else paths.ROOT / ".ebm" / "last_demo"
    out.mkdir(parents=True, exist_ok=True)
    log_f = open(paths.LOG_FILE, "a", buffering=1)
    log_f.write(f"\n--- start {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
    cmd = [
        str(paths.VENV_PY),
        "-m",
        "ebm_tle",
        "demo",
        "--output",
        str(out),
        "--mcmc",
        str(args.mcmc),
        "--subjects",
        str(args.subjects),
    ]
    proc = subprocess.Popen(
        cmd,
        cwd=str(paths.ROOT),
        stdout=log_f,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    log_f.close()
    paths.PID_FILE.write_text(str(proc.pid))
    print(f"ebm: started pid {proc.pid}; log: {paths.LOG_FILE}")
    return 0


def cmd_stop() -> int:
    if not paths.PID_FILE.is_file():
        print("ebm: no pid file (not started)")
        return 1
    pid = int(paths.PID_FILE.read_text().strip())
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"ebm: sent SIGTERM to {pid}")
    except ProcessLookupError:
        print(f"ebm: process {pid} not running")
    paths.PID_FILE.unlink(missing_ok=True)
    return 0


def cmd_logs(args: argparse.Namespace) -> int:
    if not paths.LOG_FILE.is_file():
        print(f"ebm: no log at {paths.LOG_FILE}")
        return 1
    n = args.lines
    lines = paths.LOG_FILE.read_text().splitlines()
    for line in lines[-n:]:
        print(line)
    return 0


def main() -> None:
    p = argparse.ArgumentParser(prog="ebm_tle", description="EBM_TLE internal research CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check", help="Verify venv imports and vendor paths")

    d = sub.add_parser("demo", help="Run synthetic KDE MixtureSustain demo")
    d.add_argument("--output", type=str, default=str(paths.ROOT / "runs" / "demo"))
    d.add_argument("--mcmc", type=int, default=8000)
    d.add_argument("--subjects", type=int, default=400)
    d.add_argument("--plot", action="store_true")

    f = sub.add_parser("fit", help="Fit from CSV (group 0=control 1=case)")
    f.add_argument("csv", type=str)
    f.add_argument("--output", type=str, default=str(paths.ROOT / "runs" / "fit_out"))
    f.add_argument("--group-col", type=str, default="group")
    f.add_argument("--subject-col", type=str, default="subject_id")
    f.add_argument("--mcmc", type=int, default=50_000)
    f.add_argument("--plot", action="store_true")

    s = sub.add_parser("start", help="Background demo run (logs + pid)")
    s.add_argument("--output", type=str, default=None)
    s.add_argument("--mcmc", type=int, default=8000)
    s.add_argument("--subjects", type=int, default=400)

    sub.add_parser("stop", help="Stop background job from pid file")

    lg = sub.add_parser("logs", help="Tail fit log")
    lg.add_argument("-n", "--lines", type=int, default=80)

    args = p.parse_args()
    if args.cmd == "check":
        sys.exit(cmd_check())
    if args.cmd == "demo":
        out = run_demo(
            Path(args.output),
            n_subjects=args.subjects,
            n_mcmc=args.mcmc,
            plot=args.plot,
        )
        print(f"ebm: wrote {out}")
        sys.exit(0)
    if args.cmd == "fit":
        out = fit_from_csv(
            Path(args.csv),
            Path(args.output),
            group_col=args.group_col,
            subject_col=args.subject_col,
            n_mcmc=args.mcmc,
            plot=args.plot,
        )
        print(f"ebm: wrote {out}")
        sys.exit(0)
    if args.cmd == "start":
        sys.exit(cmd_start(args))
    if args.cmd == "stop":
        sys.exit(cmd_stop())
    if args.cmd == "logs":
        sys.exit(cmd_logs(args))


if __name__ == "__main__":
    main()
