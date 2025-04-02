import unittest
from unittest import TestCase

from pyrotoolbox.parsers import parse
from pyrotoolbox.pH import *
import pyrotoolbox.pH as pHmodule
import os

script_dir = os.path.dirname(__file__)

df_wb, m_wb = parse(script_dir + '/testdata/workbench_V1.5.0.2415/A_Firesting Pro (4 Channels)_(A Ch.1)_pH.txt')
df_dt, m_dt = parse(script_dir + "/testdata/developertool_v160/FireSting-PRO 855 2024-08-22 Ch1.txt")
df_ap, m_ap = parse(script_dir + '/testdata/aquaphox_410/2024-04-08 13_46 PH1ROV_Stegende links.txt')


class Test_calc_top_and_bottom(unittest.TestCase):
    def test_workbench(self):
        self.assertEqual((1.78604717943155, 0.0950633788014184),
                         pHmodule._calc_top_and_bottom(m_wb['calibration']))

    def test_developertool(self):
        self.assertEqual((2.0405290903363387, 0.25619353351220603),
                         pHmodule._calc_top_and_bottom(m_dt['calibration']))

    def test_aquaphox(self):
        self.assertEqual((1.636112161867461, 0.04760775604660251),
                         pHmodule._calc_top_and_bottom(m_ap['calibration']))


class Test_calc_pH(unittest.TestCase):
    def test_workbench(self):
        self.assertEqual(round(calculate_pH(df_wb['R'], df_wb['sample_temperature'], m_wb['settings']['salinity'],
                                       *pHmodule._calc_top_and_bottom(m_wb['calibration']), **m_wb['calibration']).iloc[2], 3),
                         df_wb['pH'].iloc[2])

    def test_developertool(self):
        self.assertEqual(round(calculate_pH(df_dt['R'], m_dt['settings']['temperature'], m_dt['settings']['salinity'],
                                       *pHmodule._calc_top_and_bottom(m_dt['calibration']), **m_dt['calibration']), 3).iloc[0], df_dt['pH'].iloc[0])

    def test_aquaphox(self):
        self.assertEqual(round(calculate_pH(df_ap['R'], df_ap['sample_temperature'], m_ap['settings']['salinity'],
                                       *pHmodule._calc_top_and_bottom(m_ap['calibration']), **m_ap['calibration']), 3).iloc[1], df_ap['pH'].iloc[1])

        self.assertEqual(round(calculate_pH(df_ap['R'], df_ap['sample_temperature'], m_ap['settings']['salinity'],
                                       *pHmodule._calc_top_and_bottom(m_ap['calibration']), **m_ap['calibration']), 3).iloc[4],
                         df_ap['pH'].iloc[4])

class Test_calculate_pH_from_calibration(unittest.TestCase):
    def test_workbench(self):
        self.assertEqual(round(calculate_pH_from_calibration(df_wb['R'], df_wb['sample_temperature'],
                                                             m_wb['settings']['salinity'],
                                                             m_wb['calibration']).iloc[2], 3),
                         df_wb['pH'].iloc[2])

    def test_developertool(self):
        self.assertEqual(round(calculate_pH_from_calibration(df_dt['R'], m_dt['settings']['temperature'], m_dt['settings']['salinity'],
                              m_dt['calibration']), 3).iloc[0], df_dt['pH'].iloc[0])

    def test_aquaphox(self):
        self.assertEqual(round(calculate_pH_from_calibration(df_ap['R'], df_ap['sample_temperature'], m_ap['settings']['salinity'],
                              m_ap['calibration']), 3).iloc[1], df_ap['pH'].iloc[1])

        self.assertEqual(round(calculate_pH_from_calibration(df_ap['R'], df_ap['sample_temperature'], m_ap['settings']['salinity'],
                              m_ap['calibration']).iloc[4], 3), df_ap['pH'].iloc[4])


class Test_calculate_pH_from_interpolated_calibrations(unittest.TestCase):
    data, metadata = parse(script_dir + '/testdata/aquaphox_410/563OHNE.txt')
    calibs1={'R1': 1.636,
             'pH1': 2.0,
             'temp1': 26.26,
             'salinity1': 2.0,
             'R2': 0.045034,
             'pH2': 11.0,
             'temp2': 29.605,
             'salinity2': 6,
             'offset': 0.0,
             'dPhi_ref': 57.8,
             'attenuation_coefficient': 0.0339,
             'bkgdAmpl': 0.0,
             'bkgdDphi': 0.0,
             'dsf_dye': 0.9047,
             'dtf_dye': -0.00567,
             'pka': 8.301,
             'slope': 1.087,
             'bottom_t': -0.0159,
             'top_t': -0.002465,
             'slope_t': 0.0,
             'pka_t': -0.01147,
             'pka_is1': 2.54,
             'pka_is2': 0.25,
             'date_calibration_acid': dt.datetime.fromisoformat('2023-08-17 15:29:26'),
             'date_calibration_base': dt.datetime.fromisoformat('2023-08-17 15:29:26'),
             'date_calibration_offset': None}

    calibs2={'R1': 1.1800477727272727,
             'pH1': 2.0,
             'temp1': 25.590818181818182,
             'salinity1': 2.0,
             'R2': 0.045034,
             'pH2': 11.0,
             'temp2': 29.605,
             'salinity2': 6,
             'offset': 0.0,
             'dPhi_ref': 57.8,
             'attenuation_coefficient': 0.0339,
             'bkgdAmpl': 0.0,
             'bkgdDphi': 0.0,
             'dsf_dye': 0.9047,
             'dtf_dye': -0.00567,
             'pka': 8.301,
             'slope': 1.087,
             'bottom_t': -0.0159,
             'top_t': -0.002465,
             'slope_t': 0.0,
             'pka_t': -0.01147,
             'pka_is1': 2.54,
             'pka_is2': 0.25,
             'date_calibration_acid': dt.datetime.fromisoformat('2023-11-15 13:05:26'),
             'date_calibration_base': dt.datetime.fromisoformat('2023-08-17 15:29:26'),
             'date_calibration_offset': None}

    def test_input_with_dict(self):
        pH = calculate_pH_from_interpolated_calibration(self.data['R'], self.data['sample_temperature'],
                                           self.metadata['settings']['salinity'],
                                           calibrations={'2023-08-17 15:29:26':self.calibs1,
                                                         '2023-11-15 13:05:26':self.calibs2})
        self.assertAlmostEqual(pH.iloc[10], 7.256182651632969)
        self.assertAlmostEqual(pH.iloc[-110], 7.3970993597932715)

    def test_input_with_list(self):
        pH = calculate_pH_from_interpolated_calibration(self.data['R'], self.data['sample_temperature'],
                                                        self.metadata['settings']['salinity'],
                                                        [self.calibs1, self.calibs2])
        self.assertAlmostEqual(pH.iloc[10], 7.256598799655111)
        self.assertAlmostEqual(pH.iloc[-110], 7.397098650551153)


class Test_calculate_pH_with_prospective_drift_compensation(unittest.TestCase):
    data, metadata = parse(script_dir + '/testdata/aquaphox_410/563OHNE.txt')
    calibs1={'R1': 1.636,
             'pH1': 2.0,
             'temp1': 26.26,
             'salinity1': 2.0,
             'R2': 0.045034,
             'pH2': 11.0,
             'temp2': 29.605,
             'salinity2': 6,
             'offset': 0.0,
             'dPhi_ref': 57.8,
             'attenuation_coefficient': 0.0339,
             'bkgdAmpl': 0.0,
             'bkgdDphi': 0.0,
             'dsf_dye': 0.9047,
             'dtf_dye': -0.00567,
             'pka': 8.301,
             'slope': 1.087,
             'bottom_t': -0.0159,
             'top_t': -0.002465,
             'slope_t': 0.0,
             'pka_t': -0.01147,
             'pka_is1': 2.54,
             'pka_is2': 0.25,
             'date_calibration_acid': dt.datetime.fromisoformat('2023-08-17 15:29:26'),
             'date_calibration_base': dt.datetime.fromisoformat('2023-08-17 15:29:26'),
             'date_calibration_offset': None}

    def test_prospective(self):
        pH = calculate_pH_with_prospective_drift_compensation(self.data['R'], self.data['sample_temperature'],
                                                              self.metadata['settings']['salinity'], self.calibs1,
                                                              d0=3.4693e8, d1=7901.4, d2=4.3072e18, d3=15352)

        self.assertAlmostEqual(pH.iloc[10], 7.257119238758446)
        self.assertAlmostEqual(pH.iloc[-110], 7.890530189122995)


if __name__ == '__main__':
    unittest.main()
