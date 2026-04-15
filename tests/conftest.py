"""Pytest configuration: headless matplotlib, fast MCMC defaults."""

import os

os.environ.setdefault("MPLBACKEND", "Agg")
