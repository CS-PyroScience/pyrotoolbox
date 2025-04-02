import unittest

from pyrotoolbox.parsers import parse
from pyrotoolbox.oxygen import *
import os

script_dir = os.path.dirname(__file__)

df_wb, m_wb = parse(script_dir + '/testdata/workbench_V1.4.7.2305/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt')

df_dt, m_dt = parse(script_dir + "/testdata/developertool_v157/FSP1 243B1F055AC97A89 2024-05-08 12'52'26 Ch1.txt")

df_ap, m_ap = parse(script_dir + '/testdata/aquaphox_403/2020-08-13 Aquakultur.txt')
df_ap2, m_ap2 = parse(script_dir + '/testdata/aquaphox_410/2023-08-17 14_26 AFNETZ.txt')


class Test_calc_oxygen(unittest.TestCase):
    def test_workbench1(self):
        pO2 = calculate_pO2(df_wb['dphi'], df_wb['fixed_temperature'], **m_wb['calibration'])
        percentO2 = hPa_to_percentO2(pO2, df_wb['pressure'])
        self.assertAlmostEqual(percentO2.iloc[10], df_wb['oxygen_%O2'].iloc[10], 2)
        self.assertAlmostEqual(percentO2.iloc[90], df_wb['oxygen_%O2'].iloc[90], 2)

    def test_developertool(self):
        pO2 = calculate_pO2(df_dt['dphi'], m_dt['settings']['temperature'], **m_dt['calibration'])
        self.assertAlmostEqual(pO2.iloc[10], df_dt['oxygen_hPa'].iloc[10], 2)

    def test_aquaphox(self):
        pO2 = calculate_pO2(df_ap['dphi'], df_ap['sample_temperature'], **m_ap['calibration'])
        self.assertAlmostEqual(pO2.iloc[10], df_ap['oxygen_hPa'].iloc[10], 2)

    def test_aquaphox2(self):
        pO2 = calculate_pO2(df_ap2['dphi'], df_ap2['sample_temperature'], **m_ap2['calibration'])
        self.assertAlmostEqual(pO2.iloc[10], df_ap2['oxygen_hPa'].iloc[10], 2)

class Test_calc_oxygen_from_calibration(unittest.TestCase):
    def test_workbench1(self):
        pO2 = calculate_pO2_from_calibration(df_wb['dphi'], df_wb['fixed_temperature'], m_wb['calibration'])
        percentO2 = hPa_to_percentO2(pO2, df_wb['pressure'])
        self.assertAlmostEqual(percentO2.iloc[10], df_wb['oxygen_%O2'].iloc[10], 2)
        self.assertAlmostEqual(percentO2.iloc[90], df_wb['oxygen_%O2'].iloc[90], 2)

    def test_developertool(self):
        pO2 = calculate_pO2_from_calibration(df_dt['dphi'], m_dt['settings']['temperature'], m_dt['calibration'])
        self.assertAlmostEqual(pO2.iloc[10], df_dt['oxygen_hPa'].iloc[10], 2)

    def test_aquaphox(self):
        pO2 = calculate_pO2_from_calibration(df_ap['dphi'], df_ap['sample_temperature'], m_ap['calibration'])
        self.assertAlmostEqual(pO2.iloc[10], df_ap['oxygen_hPa'].iloc[10], 2)

    def test_aquaphox2(self):
        pO2 = calculate_pO2_from_calibration(df_ap2['dphi'], df_ap2['sample_temperature'], m_ap2['calibration'])
        self.assertAlmostEqual(pO2.iloc[10], df_ap2['oxygen_hPa'].iloc[10], 2)


if __name__ == '__main__':
    unittest.main()
