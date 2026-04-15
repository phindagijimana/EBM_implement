"""CLI and lifecycle (subprocess + pid file)."""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from ebm_tle import paths
from ebm_tle.cli import cmd_check, cmd_logs, cmd_start, cmd_stop


def test_cmd_check_exits_zero():
    # Requires dev env with kde_ebm + pySuStaIn
    assert cmd_check() == 0


def test_ebm_module_check_subprocess():
    repo = Path(__file__).resolve().parents[1]
    r = subprocess.run(
        [sys.executable, "-m", "ebm_tle", "check"],
        cwd=str(repo),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert r.returncode == 0, r.stderr + r.stdout


def test_cmd_stop_clears_stale_pid(tmp_path, monkeypatch):
    pid_file = tmp_path / "pid"
    monkeypatch.setattr(paths, "PID_FILE", pid_file)
    pid_file.write_text("999999001")
    assert cmd_stop() == 0
    assert not pid_file.exists()


def test_cmd_logs_reads_tail(tmp_path, monkeypatch):
    log = tmp_path / "fit.log"
    log.write_text("line1\nline2\nline3\n")
    monkeypatch.setattr(paths, "LOG_FILE", log)
    class A:
        lines = 2

    assert cmd_logs(A()) == 0


def test_cmd_stop_sigterm_live_process(tmp_path, monkeypatch):
    pid_file = tmp_path / "pid"
    log_file = tmp_path / "fit.log"
    monkeypatch.setattr(paths, "PID_FILE", pid_file)
    monkeypatch.setattr(paths, "LOG_FILE", log_file)
    monkeypatch.setattr(paths, "RUN_DIR", tmp_path / "run")
    monkeypatch.setattr(paths, "LOG_DIR", tmp_path / "logs")
    paths.RUN_DIR.mkdir(parents=True, exist_ok=True)
    paths.LOG_DIR.mkdir(parents=True, exist_ok=True)

    proc = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(120)"],
        start_new_session=True,
    )
    pid_file.write_text(str(proc.pid))
    assert cmd_stop() == 0
    assert not pid_file.exists()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        raise AssertionError("child still running after SIGTERM")
    assert proc.returncode not in (0, None)


@pytest.mark.slow
def test_cmd_start_stop_background_demo(tmp_path, monkeypatch):
    repo = Path(__file__).resolve().parents[1]
    out = tmp_path / "bg_demo"
    monkeypatch.setattr(paths, "ROOT", repo)
    monkeypatch.setattr(paths, "VENV_PY", Path(sys.executable))
    monkeypatch.setattr(paths, "RUN_DIR", tmp_path / ".ebm" / "run")
    monkeypatch.setattr(paths, "LOG_DIR", tmp_path / ".ebm" / "logs")
    monkeypatch.setattr(paths, "PID_FILE", tmp_path / ".ebm" / "run" / "pid")
    monkeypatch.setattr(paths, "LOG_FILE", tmp_path / ".ebm" / "logs" / "fit.log")
    paths.RUN_DIR.mkdir(parents=True, exist_ok=True)
    paths.LOG_DIR.mkdir(parents=True, exist_ok=True)

    class Args:
        output = str(out)
        mcmc = 1200
        subjects = 80

    assert cmd_start(Args()) == 0
    assert paths.PID_FILE.is_file()
    pid = int(paths.PID_FILE.read_text().strip())
    time.sleep(0.5)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        pass  # demo may finish quickly on a fast host
    assert cmd_stop() == 0
    assert not paths.PID_FILE.exists()
