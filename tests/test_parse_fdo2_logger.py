import unittest
from unittest import TestCase

from pyrotoolbox import parse
import datetime
import numpy as np
import os

script_dir = os.path.dirname(__file__)


class TestFDO2Logger_v145(unittest.TestCase):
    directory = script_dir + '/testdata/FDO2_Logger_145/'

    def test_load_fw355(self):
        file1 = "FDO2 2025-06-24 16'13'23 ID2453D306656DD445.txt"
        df, m = parse(self.directory + file1)
        self.assertEqual({'experiment_name': '',
 'experiment_description': '',
 'device': '',
 'firmware': '3.55',
 'uid': '2453D306656DD445',
 'software_version': '1.45',
 'settings': {'analyte': 'oxygen',
  'temperature': 'external sensor',
  'pressure': 'internal sensor',
  'salinity': 0.0,
  'duration': '16ms',
  'intensity': '15%',
  'amp': '200x',
  'frequency': 4000,
  'crc_enable': False,
  'write_lock': False,
  'auto_flash_duration': True,
  'auto_amp': True,
  'broadcast_interval_ms': 0},
 'calibration': {'dphi0': 53.209,
  'dphi100': 20.485,
  'temp0': 24.976,
  'temp100': 25.263,
  'pressure': 989.055,
  'humidity': 0.0,
  'f': 0.824,
  'm': 0.083,
  'tt': -0.00065,
  'kt': 0.00673,
  'bkgdAmpl': 0.0,
  'bkgdDphi': 0.0,
  'ft': 0.0,
  'mt': -0.000239,
  'temp_offset': 0.0,
  'percentO2': 20.02},
 'user_calibration': {'dphi0': None,
  'temp0': None,
  'dphi100': None,
  'temp100': None,
  'pressure': None,
  'humidity': None,
  'percentO2': None,
  'm': None,
  'crc_enable': False,
  'broadcast_interval_ms': 0.0}}, m)
        self.assertEqual(['time_s', 'oxygen_hPa', 'sample_temperature', 'status', 'dphi',
       'signal_intensity', 'ambient_light', 'pressure', 'humidity', 'Comment'], list(df.columns))
        self.assertEqual(2250, len(df))
        self.assertDictEqual({'time_s': 1.4,
 'oxygen_hPa': 0.839,
 'sample_temperature': 29.375,
 'status': 0.0,
 'dphi': 52.685,
 'signal_intensity': 772.543,
 'ambient_light': 0.0,
 'pressure': 994.228,
 'humidity': 36.72,
 'Comment': np.nan}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})
        self.assertTrue(df.index.is_monotonic_increasing)

    def test_load_fw341(self):
     file1 = "FDO2 2025-07-01 12'39'09 ID2479F6055E9BDBD4.txt"
     df, m = parse(self.directory + file1)
     self.assertEqual({'experiment_name': '',
 'experiment_description': '',
 'device': '',
 'firmware': '3.41',
 'uid': '2479F6055E9BDBD4',
 'software_version': '1.45',
 'settings': {'analyte': 'oxygen',
  'temperature': 'external sensor',
  'pressure': 'internal sensor',
  'salinity': 0.0,
  'duration': '16ms',
  'intensity': '10%',
  'amp': '200x',
  'frequency': 4000,
  'crc_enable': False,
  'write_lock': False,
  'auto_flash_duration': True,
  'auto_amp': True,
  'broadcast_interval_ms': 0},
 'calibration': {'dphi0': 53.617,
  'dphi100': 21.307,
  'temp0': 22.559,
  'temp100': 25.517,
  'pressure': 968.878,
  'humidity': 0.0,
  'f': 0.846,
  'm': 0.093,
  'tt': -0.0006,
  'kt': 0.00931,
  'bkgdAmpl': 0.0,
  'bkgdDphi': 0.0,
  'ft': 0.0,
  'mt': -0.000185,
  'temp_offset': 0.0,
  'percentO2': 20.95},
 'user_calibration': {}}, m)
     self.assertEqual(['time_s', 'oxygen_hPa', 'sample_temperature', 'status', 'dphi',
       'signal_intensity', 'ambient_light', 'pressure', 'humidity', 'Comment'], list(df.columns))
     self.assertEqual(482, len(df))
     self.assertDictEqual({'time_s': 10.5,
 'oxygen_hPa': 172.804,
 'sample_temperature': 30.0,
 'status': 0.0,
 'dphi': 22.67,
 'signal_intensity': 405.922,
 'ambient_light': 32.218,
 'pressure': 977.568,
 'humidity': 38.853,
 'Comment': np.nan}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[10].to_dict().items()})
     self.assertTrue(df.index.is_monotonic_increasing)

if __name__ == '__main__':
    unittest.main()
