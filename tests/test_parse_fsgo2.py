import unittest

from pyrotoolbox.parsers import read_fsgo2
import datetime
import numpy as np
import os

script_dir = os.path.dirname(__file__)


class Firmware_336(unittest.TestCase):
    directory = script_dir + '/testdata/go2_3.36/'

    def test_load_f1(self):
        file1 = "2020-06-24 10'44 LOG026.txt"
        df, m = read_fsgo2(self.directory + file1)
        self.assertEqual({'experiment_name': 'LOG026', 'experiment_description': '',
 'device': 'FireStingGO2_Pocket_Oxygen_Meter', 'firmware': '3.36', 'uid': '24C53408575BA6A3', 'software_version': 'Firmware 3.36',
 'settings': {'analyte': 'oxygen', 'temperature': 'internal sensor', 'pressure': 'internal sensor', 'salinity': 0.0,
  'amp': '400x', 'frequency': '3000 Hz'}, 'calibration': {'dphi0': 53.0, 'dphi100': 20.0, 'temp0': 20.0,
  'temp100': 20.0, 'pressure': 1013.0, 'humidity': 100.0, 'f': 0.85, 'm': 0.081,
  'tt': -0.0007000000000000001, 'kt': 0.01184, 'bkgdAmpl': 0.0, 'bkgdDphi': 0.0, 'ft': 0.0, 'mt': -0.00037,
  'percentO2': 20.95, 'date_calibration_high': None, 'date_calibration_zero': None},
 'sensor_code': 'XA7-530-200'}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['oxygen_%O2', 'sample_temperature', 'pressure', 'humidity', 'time_s',
       'status', 'dphi', 'signal_intensity', 'ambient_light',
       'case_temperature'], list(df.columns))
        self.assertEqual(30, len(df))
        self.assertDictEqual({'oxygen_%O2': np.nan,
 'sample_temperature': np.nan,
 'pressure': 978.0,
 'humidity': 37.2,
 'time_s': 1.0,
 'status': 34.0,
 'dphi': 9.75,
 'signal_intensity': 1.2,
 'ambient_light': 18.4,
 'case_temperature': 24.88},
                             {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})


class Firmware_339(unittest.TestCase):
    directory = script_dir + '/testdata/go2_3.39/'

    def test_load_f1(self):
        file1 = "2024-07-25 15'41 TEST1(1).txt"
        df, m = read_fsgo2(self.directory + file1)
        self.assertEqual({'experiment_name': 'TEST1', 'experiment_description': '',
                          'device': 'FireStingGO2_Pocket_Oxygen_Meter', 'firmware': '3.39', 'uid': '24EB9B03596FCD7D',
                          'software_version': 'Firmware 3.39',
                          'settings': {'analyte': 'oxygen', 'temperature': 'internal sensor',
                                       'pressure': 'internal sensor',
                                       'salinity': 0.0, 'amp': '400x', 'frequency': '4000 Hz'},
                          'calibration': {'dphi0': 51.6,
                                          'dphi100': 22.9, 'temp0': 20.0, 'temp100': 20.0, 'pressure': 1013.0,
                                          'humidity': 0.0, 'f': 0.836,
                                          'm': 0.049, 'tt': -0.00029, 'kt': 0.00549, 'bkgdAmpl': 0.6, 'bkgdDphi': 0.0,
                                          'ft': 0.0, 'mt': -3.2e-05, 'percentO2': 20.95, 'date_calibration_high': None,
                                          'date_calibration_zero': None},
                          'sensor_code': 'HC7-516-229'}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['oxygen_mgL', 'sample_temperature', 'pressure', 'humidity', 'time_s',
                          'status', 'dphi', 'signal_intensity', 'ambient_light',
                          'case_temperature'], list(df.columns))
        self.assertEqual(151, len(df))
        self.assertDictEqual({'oxygen_mgL': np.nan,
                              'sample_temperature': 26.49, 'pressure': 1002.2, 'humidity': 44.7, 'time_s': 2.0,
                              'status': 2.0, 'dphi': -180.0, 'signal_intensity': 0.6, 'ambient_light': 0.0,
                              'case_temperature': 28.26},
                             {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})

    def test_load_f2(self):
        file1 = "2024-08-27 09'05 LOG003.txt"
        df, m = read_fsgo2(self.directory + file1)
        self.assertEqual({'experiment_name': 'LOG003', 'experiment_description': '',
 'device': 'FireStingGO2_Pocket_Oxygen_Meter', 'firmware': '3.39', 'uid': '24C53408575BA6A3', 'software_version': 'Firmware 3.39',
 'settings': {'analyte': 'oxygen', 'temperature': '25.6°C', 'pressure': 'internal sensor', 'salinity': 0.0,
  'amp': '200x', 'frequency': '4000 Hz'}, 'calibration': {'dphi0': 52.0, 'dphi100': 21.128,
  'temp0': 20.0, 'temp100': 25.2, 'pressure': 979.0, 'humidity': 45.0, 'f': 0.817, 'm': 0.106,
  'tt': -0.0007000000000000001, 'kt': 0.00953, 'bkgdAmpl': 0.0, 'bkgdDphi': 0.0, 'ft': 0.0,
  'mt': -0.000301, 'percentO2': 20.95, 'date_calibration_high': datetime.datetime(2024, 8, 27, 0, 0),
  'date_calibration_zero': None},
 'sensor_code': 'ZA6-520-204'}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['oxygen_%O2', 'sample_temperature', 'pressure', 'humidity', 'time_s',
       'status', 'dphi', 'signal_intensity', 'ambient_light',
       'case_temperature'], list(df.columns))
        self.assertEqual(31, len(df))
        self.assertDictEqual({'oxygen_%O2': 20.699, 'sample_temperature': np.nan, 'pressure': 979.1,
 'humidity': 44.7, 'time_s': 11.0, 'status': 32.0, 'dphi': 21.053, 'signal_intensity': 150.3,
 'ambient_light': 7.6, 'case_temperature': 26.16}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})


if __name__ == '__main__':
    unittest.main()
