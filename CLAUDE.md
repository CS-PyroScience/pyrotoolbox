# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`pyrotoolbox` is a Python library for post-processing measurement data from PyroScience GmbH devices/software (oxygen, pH, temperature optical sensors). It parses device logfiles into pandas DataFrames + metadata dicts, re-calculates oxygen/pH from raw phase data with new calibrations, converts between oxygen units, and generates HTML reports.

## Commands

```bash
make test                            # run full test suite (unittest discover)
python3 -m unittest tests.test_parse            # run one test module
python3 -m unittest tests.test_parse.TestWorkbench.test_load_1020   # run one test
make black                           # format (black, line length 120)
make build                           # build wheel/sdist (hatchling) into dist/
make doku                            # build PDF docs via sphinx
```

There is no linter beyond `black`. Formatting standard is `black --line-length 120`.

Console entry points (defined in `pyproject.toml`): `PyroHtmlReporter` (CLI → `HtmlReporter:main`) and `FireResponse` (GUI, needs the `fireresponse` extra: `PyQt5`, `pyqtgraph`).

## Architecture

The whole library is organized around a single data contract: **parsers produce a `(pandas.DataFrame, metadata: dict)` tuple, and every other module consumes that same shape.** Column names and metadata keys are normalized to be identical regardless of the source logfile format — downstream code depends on these canonical names, so preserve them.

### `parsers.py` — entry point for all data loading
- `parse(fname)` sniffs the first lines of a text file and dispatches to the right reader: Workbench, FirePlate Workbench, DeveloperTool, AquaphOx logger, FSGO2, FDO2 logger. Does **not** read `.pyr` files.
- Each `read_*` function returns `(df, metadata)`. Canonical DataFrame columns include `dphi`, `R`, `sample_temperature`, `pressure`, `status`, `oxygen_hPa`, `oxygen_%airsat`, `pH`, etc. (see the big `df.rename(...)` maps). The df is indexed by `date_time`.
- `metadata` is a nested dict with keys like `software_version`, `device`, `channel`, `settings` (dict), and `calibration` (dict). The `calibration` dict is exactly what the recalculation functions in `oxygen.py`/`pH.py` expect.
- `CURRENT_WORKBENCH_VERSION` / `CURRENT_DEVELOPERTOOL_VERSION` constants gate "unknown newer version" warnings. Version-dependent parsing branches on these string comparisons — when supporting a new device firmware, update these and add a corresponding testdata directory.

### `oxygen.py` — oxygen recalculation + unit conversion
- `calculate_pO2_from_calibration(dphi, temperature, calibration)` re-derives pO2 (hPa) from raw phase using a `calibration` dict from metadata.
- The core Ksv/tau0 math is delegated to a compiled C library loaded via `ctypes` at runtime: `oxycalc.so` (Linux/macOS) or `oxycalc.dll` (Windows), selected by platform. These binaries ship in the package — there is no build step for them here.
- `convert_to_hPa(...)` and the `hPa_to_*` family (`hPa_to_mgL`, `hPa_to_percent_airsat`, `hPa_to_torr`, ...) do unit conversions; everything routes through hPa/partial pressure as the internal unit. `calc_oxygen_solubility` uses Garcia 1992 seawater equations.

### `pH.py` — pH recalculation
- `calculate_pH_from_calibration(R, temperature, salinity, calibration)` is the main entry; `calculate_pH` holds the raw material-constant model.
- Drift correction variants: `calculate_pH_from_interpolated_calibration` (fits top/bottom linearly across multiple calibrations over time) and `calculate_pH_with_prospective_drift_compensation`.

### `phase.py` — low-level phase-angle helpers
Small pure functions (`calc_tau`, `calc_dphi`, background subtraction, `calc_R`) used by the calculation modules.

### `HtmlReporter.py` — reporting
`make_report` / `make_comparison_report` render plotly-based HTML reports. `main()` is the `PyroHtmlReporter` CLI: takes logfiles, supports `--start_time/--end_time/--skipfirst/--skiplast/--onlysummary`, writes `<logfile>_report.html` and a combined `summary.html`.

### `FireResponse/` — optional PyQt5 GUI
Standalone real-time viewer app; isolated from the core library and only imported through its own entry point.

## Tests

`tests/` uses `unittest`. Each `test_parse_*.py` module loads real device logfiles from `tests/testdata/<format>_<version>/` and asserts the full parsed `metadata` dict and DataFrame values. **Adding support for a new device/firmware version means adding a `tests/testdata/` fixture directory and a corresponding test** that pins the exact expected metadata — follow the existing pattern of asserting the complete dict literal.
