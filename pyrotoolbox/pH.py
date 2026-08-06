#!/usr/bin/env python3
# pyrotoolbox, a collection of tools to work with PyroScience GmbH data.
# Copyright (C) 2025, Christoph Staudinger
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Module to calculate pH for devices from Pyroscience.

The following functions are only valid for devices with Firmware >= 4.10 (released 2023).
"""

import numpy as np
import pandas as pd
import datetime as dt


drift_constants = {
    "PK7":   {"d0": 6.0508e+08, "d1": 7.7907e+03, "d2": 0, "d3": 0},
    "PK8":   {"d0": 4.3652e+10, "d1": 9.0761e+03, "d2": 0, "d3": 0},
    "PK8T":  {"d0": 4.3652e+10, "d1": 9.0761e+03, "d2": 0, "d3": 0},
    "PK6":   {"d0": 3.9569e+08, "d1": 7.5899e+03, "d2": 0, "d3": 0},
    "PK65": {"d0": 3.1111e+05, "d1": 5.4952e+03, "d2": 0, "d3": 0},
    "PK5":   {"d0": 3.2839e+03, "d1": 4.2170e+03, "d2": 0, "d3": 0},
}


class LinearFit:
    """Result of an unweighted least-squares fit of a straight line."""

    def __init__(self, slope: float, intercept: float):
        self.slope = slope
        self.intercept = intercept

    def eval(self, x):
        """Evaluate the fitted line at x."""
        return self.slope * np.asarray(x, dtype=float) + self.intercept

    def __call__(self, x):
        return self.eval(x)

    def __repr__(self):
        return f"LinearFit(slope={self.slope!r}, intercept={self.intercept!r})"


def _linear_fit(x, y) -> LinearFit:
    """Fit y = slope * x + intercept by unweighted least squares.

    x is centered before fitting - the x-values are epoch seconds (~1e9) which would otherwise make the
    fit badly conditioned - and the result is shifted back to the original x-axis.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    x0 = x.mean()
    slope, intercept = np.polyfit(x - x0, y, 1)
    return LinearFit(slope, intercept - slope * x0)


def _calc_top_and_bottom(calibration: dict) -> tuple[float, float]:
    """Calculate top and bottom (upper and lower limit of the R value for 20°C).

    :param calibration: dictionary with the following keys:
        - pH1
        - R1
        - temp1
        - salinity1
        - pH2
        - R2
        - temp2
        - salinity2
        - pka
        - slope
        - pka_t
        - top_t
        - bottom_t
        - slope_t
        - pka_is1
        - pka_is2
    This dictionary is created by the parse / read functions. E.g.: m['calibration']
    :return: tuple(top, bottom)
    """
    R1 = calibration["R1"]
    pH1 = calibration["pH1"]
    temp1 = calibration["temp1"]
    salinity1 = calibration["salinity1"]
    R2 = calibration["R2"]
    pH2 = calibration["pH2"]
    temp2 = calibration["temp2"]
    salinity2 = calibration["salinity2"]
    pka = calibration["pka"]
    slope = calibration["slope"]
    top_t = calibration["top_t"]
    bottom_t = calibration["bottom_t"]
    pka_t = calibration["pka_t"]
    slope_t = calibration["slope_t"]
    pka_is1 = calibration["pka_is1"]
    pka_is2 = calibration["pka_is2"]

    pka1 = (
        pka
        + pka_t * (temp1 - 20)
        - 0.5
        * pka_is1
        * (
            np.sqrt(salinity1 * 20 / 1000) / (1 + np.sqrt(salinity1 * 20 / 1000))
            - 0.2791745
            - pka_is2 * (salinity1 * 20 / 1000 - 0.15)
        )
    )
    slope1 = slope * (1 + slope_t * (temp1 - 20))
    bt1 = 1 + bottom_t * (temp1 - 20)
    tt1 = 1 + top_t * (temp1 - 20)
    N1 = 1 + 10 ** ((pH1 - pka1) / slope1)

    pka2 = (
        pka
        + pka_t * (temp2 - 20)
        - 0.5
        * pka_is1
        * (
            np.sqrt(salinity2 * 20 / 1000) / (1 + np.sqrt(salinity2 * 20 / 1000))
            - 0.2791745
            - pka_is2 * (salinity2 * 20 / 1000 - 0.15)
        )
    )
    slope2 = slope * (1 + slope_t * (temp2 - 20))
    bt2 = 1 + bottom_t * (temp2 - 20)
    tt2 = 1 + top_t * (temp2 - 20)
    N2 = 1 + 10 ** ((pH2 - pka2) / slope2)

    bottom = (R2 * N2 - R1 * N1 * tt2 / tt1) / (bt2 * N2 + bt1 * tt2 / tt1 - bt1 * N1 * tt2 / tt1 - bt2)

    top = (R1 * N1 + bottom * bt1 - bottom * bt1 * N1) / tt1
    return top, bottom


def calculate_pH(
    R,
    temperature,
    salinity,
    top,
    bottom,
    pka,
    slope,
    pka_t,
    bottom_t,
    top_t,
    slope_t,
    pka_is1,
    pka_is2,
    offset,
    **kwargs,
):
    """Calculate pH from R, temperature, salinity and sensor constants. See also function calculate_pH_from_calibration.

    :param R: R-value from the sensor
    :param temperature: temperature of the sample in °C
    :param salinity: salinity of the sample in g/L
    :param top: material constant
    :param bottom: material constant
    :param pka: material constant
    :param slope: material constant
    :param pka_t: material constant
    :param bottom_t: material constant
    :param top_t: material constant
    :param slope_t: material constant
    :param pka_is1: material constant
    :param pka_is2: material constant
    :param offset: offset in pH-units (from 3rd calibration point)
    :param kwargs: kwargs are ignored
    :return:
    """
    B = bottom * (1 + bottom_t * (temperature - 20))
    T = top * (1 + top_t * (temperature - 20))
    IS = salinity * 20 / 1000
    SLOPE = slope * (1 + slope_t * (temperature - 20))
    PKA = (
        pka
        + pka_t * (temperature - 20)
        - 0.5 * pka_is1 * (np.sqrt(IS) / (1 + np.sqrt(IS)) - 0.2791745 - pka_is2 * (IS - 0.15))
    )
    pH = np.log10((T - R) / (R - B)) * SLOPE + PKA + offset
    return pH


def calculate_pH_from_calibration(R, temperature, salinity, calibration: dict, **kwargs):
    """apply a pH calibration to measurement data for FW >= 410

    The calibration parameters can be passed from the calibration metadata.

    Example usage:
    apply_pH_calibration(data['R'], data['temp'], data['salinity'], m['calibration'])

    :param R: R-value from the sensor
    :param temperature: temperature of the sample in °C
    :param salinity: salinity of the sample in g/L
    :param calibration: calibration dictionary as created by the parsers
    :param kwargs: kwargs are inserted into the calibration and override the values
    :return: calculated pH values
    """
    calibration = calibration.copy()
    for k, v in kwargs.items():
        if k not in calibration:
            raise ValueError(f'Unknown calibration parameter: "{k}"')
        calibration[k] = v
    top, bottom = _calc_top_and_bottom(calibration)
    return calculate_pH(R, temperature, salinity, top=top, bottom=bottom, **calibration)


def calculate_pH_from_interpolated_calibration(R, temperature, salinity, calibrations, return_fits=False):
    """Apply an interpolated pH calibration to measurement data

    The top and bottom value is calculated for every passed calibration and fitted linear over time. For every
    measurement point an individual value of top and bottom is calculated.

    :param R: data for "R"
    :param temperature: overrides temp values from df. Single value or iterable with same length as df is required
    :param salinity: Single value or iterable with same length as df is required
    :param calibrations: dict in format {timestring: calib_data} e.g. {'2019-05-05 13:10:00': {pH1: 4, temp1: 22.08, ...}}, or a list of calibration-dicts
    :param R: overrides R values from df. Single value or iterable with same length as df is required
    :param return_fits: return the fits of top, bottom and offset instead (as :class:`LinearFit` objects)
    :return: calculated pH-values

    """
    base_calibration = None
    if isinstance(calibrations, dict):
        if base_calibration is None:  # use first passed calibration as base parameters
            base_calibration = list(calibrations.values())[0]
        tops_and_bottoms_dict = {
            dt.datetime.fromisoformat(k).timestamp(): _calc_top_and_bottom(v) for k, v in calibrations.items()
        }
        date_top_dict = {k: v[0] for k, v in tops_and_bottoms_dict.items()}
        date_bottom_dict = {k: v[1] for k, v in tops_and_bottoms_dict.items()}
        date_offset_dict = {dt.datetime.fromisoformat(k).timestamp(): v["offset"] for k, v in calibrations.items()}
    elif isinstance(calibrations, list):
        base_calibration = calibrations[0]
        date_top_dict = {
            cal["date_calibration_acid"].timestamp(): _calc_top_and_bottom(cal)[0]
            for cal in calibrations
            if cal["date_calibration_acid"]
        }
        date_bottom_dict = {
            cal["date_calibration_base"].timestamp(): _calc_top_and_bottom(cal)[1]
            for cal in calibrations
            if cal["date_calibration_base"]
        }
        date_offset_dict = {
            cal["date_calibration_offset"].timestamp(): cal["offset"]
            for cal in calibrations
            if cal["date_calibration_offset"]
        }
        if len(date_top_dict) == 0:
            date_top_dict[0] = _calc_top_and_bottom(calibrations[0])[0]
        if len(date_bottom_dict) == 0:
            date_bottom_dict[0] = _calc_top_and_bottom(calibrations[0])[1]
        if len(date_offset_dict) == 0:
            date_offset_dict[0] = calibrations[0]["offset"]

    # fit both over time
    # epoch seconds, independent of the datetime64 resolution ("ns", "us", ...) backing R.index
    x_seconds = (R.index - pd.Timestamp("1970-01-01")) / pd.Timedelta(seconds=1)
    # if len is 1 do not fit!
    # top
    fits = {}
    if len(date_top_dict) > 1:
        top_fit = _linear_fit(list(date_top_dict.keys()), list(date_top_dict.values()))
        top = top_fit.eval(x=x_seconds)
        fits["top"] = top_fit
    else:
        top = list(date_top_dict.values())[0]
    if len(date_bottom_dict) > 1:
        bottom_fit = _linear_fit(list(date_bottom_dict.keys()), list(date_bottom_dict.values()))
        bottom = bottom_fit.eval(x=x_seconds)
        fits["bottom"] = bottom_fit
    else:
        bottom = list(date_bottom_dict.values())[0]
    if len(date_offset_dict) > 1:
        offset_fit = _linear_fit(list(date_offset_dict.keys()), list(date_offset_dict.values()))
        offset = offset_fit.eval(x=x_seconds)
        fits["offset"] = offset_fit
    else:
        offset = list(date_offset_dict.values())[0]
    if return_fits:
        return fits
    # return R, temp, salinity, top, bottom, base_calibration, offset

    return calculate_pH(
        R,
        temperature,
        salinity,
        top,
        bottom,
        pka=base_calibration["pka"],
        slope=base_calibration["slope"],
        pka_t=base_calibration["pka_t"],
        top_t=base_calibration["top_t"],
        bottom_t=base_calibration["bottom_t"],
        slope_t=base_calibration["slope_t"],
        pka_is1=base_calibration["pka_is1"],
        pka_is2=base_calibration["pka_is2"],
        offset=offset,
    )


def calculate_pH_with_prospective_drift_compensation(
    R, temperature, salinity, calibration: dict, d0: float, d1: float, d2: float, d3: float, start_timestamp=None
):
    """apply prospective pH drift compensation to a pH measurement.

    The effect on the sensors is assumed to be only a decrease in Top.

    :param R: R-values, pandas Series or DataFrame with time index
    :param temperature: temperature data
    :param salinity: salinity data
    :param calibration: calibration dictionary as created by the parser functions
    :param start_timestamp: optional, time of the calibration. By default, the date_calibration_acid value is used
    :param d0: first coefficient of the temperature dependent drift
    :param d1: second coefficient of the temperature dependent drift
    :param d2: third coefficient of the temperature dependent drift
    :param d3: fourth coefficient of the temperature dependent drift
    :param start_timestamp: optional, start of the drift. If omitted the date of the last acid calibration is used
    :return: array of pH values
    """

    if start_timestamp is None:
        start_timestamp = calibration["date_calibration_acid"]

    top, bottom = _calc_top_and_bottom(calibration)

    top = _calc_top_prospective(top, temperature, (R.index - start_timestamp).total_seconds() / 3600 / 24, d0, d1)
    bottom = _calc_bottom_prospective(
        bottom, temperature, (R.index - start_timestamp).total_seconds() / 3600 / 24, d2, d3
    )

    return calculate_pH(R, temperature, salinity, top=top, bottom=bottom, **calibration)


def _calc_top_prospective(top: float, temperature, time_days, d0: float, d1: float) -> np.array:
    """calculate top (R1) prospective. Mainly used for prospective drift correction.

    It is assumed that top decreases exponentially over time. The rate of decrease is temperature dependent.
    d0 and d1 describe the temperature dependence of the drift rate.

    R1=R10*exp(-dtop*t[days])

    :param top: initial top value
    :param temperature: array of temperatures
    :param time_days: array of ages (in days)
    :param d0: first drift parameter
    :param d1: second drift parameter
    :return: array of top values
    """
    if len(temperature) != len(time_days):
        raise ValueError("temperature and timestamps must have the same length")
    top_list = [top]
    for i in range(len(temperature) - 1):
        # calc dtop
        t = np.mean([temperature.iloc[i], temperature.iloc[i + 1]])
        dtop = d0 * np.exp(-d1 / (t + 273.15))
        # calc delta time in days
        delta_time = time_days[i + 1] - time_days[i]

        top_list.append(top_list[-1] / np.exp(dtop * delta_time))
    return np.array(top_list)


def _calc_bottom_prospective(bottom: float, temperature, time_days, d2: float, d3: float) -> np.array:
    """calculate bottom (R2) prospective. Mainly used for prospective drift correction.

    It is assumed that bottom increases linearly over time. The rate of increase is temperature dependent.
    d2 and d3 describe the temperature dependence of the drift rate.

    bottom1 = bottom0 + d2 * exp(-d3/T) * delta_time

    :param bottom: initial bottom value
    :param temperature: array of temperatures
    :param time_days: array of ages (in days)
    :param d2: first drift parameter
    :param d3: second drift parameter
    :return: array of bottom values
    """
    if len(temperature) != len(time_days):
        raise ValueError("temperature and timestamps must have the same length")
    bottom_list = [bottom]
    for i in range(len(temperature) - 1):
        # calc dbottom
        t = np.mean([temperature.iloc[i], temperature.iloc[i + 1]])
        dbottom = d2 * np.exp(-d3 / (t + 273.15))
        # calc delta time in days
        delta_time = time_days[i + 1] - time_days[i]

        bottom_list.append(bottom_list[-1] + dbottom * delta_time)
    return np.array(bottom_list)
