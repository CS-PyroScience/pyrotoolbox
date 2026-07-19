# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`pyrotoolbox` is a Python package (>=3.10) for processing measurement data from PyroScience GmbH devices: parsing logfiles into pandas DataFrames, recalculating oxygen and pH values with new calibrations, and generating HTML reports. Published to PyPI; docs on readthedocs (Sphinx, sources in `docs/`).

## Commands

- **Run all tests:** `python3 -m unittest discover -v` (or `make test`)
- **Run a single test:** `python3 -m unittest tests.test_parse.TestWorkbench.test_load_1020`
- **Format:** `black --line-length 120 */*.py` (or `make black`)
- **Build package:** `python3 -m build` (or `make build`)
- **Build docs (PDF):** `sphinx-build docs docs/_build -b simplepdf` (or `make doku`)

A virtualenv lives in `.venv/`. The package version is in `pyproject.toml` (beta versions like `1.15b`).

## Architecture

The central data contract: **every parser returns `(pandas.DataFrame, metadata_dict)` with standardized column names and metadata keys, regardless of input format**. All other modules (oxygen/pH recalculation, HtmlReporter, FireResponse) rely on these naming conventions.

- **`pyrotoolbox/parsers.py`** — `parse(fname)` auto-detects the logfile format from the first lines and dispatches to a format-specific reader: `read_workbench`, `read_fireplate_workbench`, `read_developertool`, `read_aquaphoxlogger`, `read_fsgo2`, `read_fdo2_logger`. Metadata parsing (settings/calibration blocks) is format-specific via `_parse_*` helpers. `CURRENT_WORKBENCH_VERSION` / `CURRENT_DEVELOPERTOOL_VERSION` at the top are used to warn when a logfile comes from a newer software version — bump them when adding support for new versions.
- **`pyrotoolbox/oxygen.py`** — oxygen unit conversions and recalculation. hPa is the pivot unit: `convert_to_hPa()` first, then `hPa_to_*()` (torr, %O2, %airsat, µM, mg/L). `i_only_think_in_hpa(df, m)` / `i_have_a_fireplate_and_still_only_think_in_hPa(df, m)` operate directly on parser output. Recalculating pO2 from raw phase angle (dphi) uses a compiled C library (`oxycalc.so` / `oxycalc.dll`) loaded via ctypes at import time — Linux and Windows only; the C source is not in this repo.
- **`pyrotoolbox/pH.py`** — pH recalculation from the R value with a calibration dict, including drift correction (interpolation between calibrations via lmfit, and prospective drift compensation). Only valid for device firmware >= 4.10 (2023).
- **`pyrotoolbox/phase.py`** — low-level phase-angle math (tau/dphi conversion, background subtraction, R calculation) shared by the calculation modules.
- **`pyrotoolbox/HtmlReporter.py`** — plotly-based HTML report generation. Console entry point `PyroHtmlReporter` (see `main()`); separate plotting paths for regular channels and FirePlate (multi-well) data.
- **`pyrotoolbox/FireResponse/`** — PyQt5/pyqtgraph GUI for sensor response-time analysis. GUI entry point `FireResponse`; requires the `fireresponse` optional dependency group.

## Tests

Tests are `unittest`-based and run against real device logfiles in `tests/testdata/`, organized in one directory per software/firmware version (e.g. `workbench_V1.5.4.2482`, `developertool_v162`). Parser tests assert the complete parsed metadata dict and spot-check data values. When adding support for a new logfile format or software version, add a testdata directory for it and a corresponding test case following the existing pattern.
