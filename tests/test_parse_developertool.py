import unittest
from unittest import TestCase

from pyrotoolbox.parsers import read_developertool
import datetime
import numpy as np
import os

script_dir = os.path.dirname(__file__)


class TestDeveloperTool_v150(unittest.TestCase):
    directory = script_dir + '/testdata/developertool_v150/'

    def test_load_f1(self):
        file1 = "FSP1 243B1F055AC97A89 2022-06-23 10'52'38 Ch1.txt"
        df, m = read_developertool(self.directory + file1)
        self.assertEqual({'software_version': 'PyroSimpleLogger\tv150\t(c) 2021 by\tPyroScience GmbH',
 'experiment_name': "FSP1 243B1F055AC97A89 2022-06-23 10'52'38 Ch1.txt",
 'experiment_description': '', 'device': 'FSP1', 'uid': '243B1F055AC97A89', 'firmware': '405:3',
 'channel': '1', 'settings': {'temperature': 'external sensor', 'pressure': 'internal sensor',
  'salinity': 7.5, 'duration': '16ms', 'intensity': '40%', 'amp': '400x', 'frequency': 3000, 'crc_enable': False,
  'write_lock': False, 'auto_flash_duration': False, 'auto_amp': True, 'analyte': 'pH', 'fiber_type': '1 mm',
  'referenceMode': 'smart averaging', 'refDurationAveragingMode': 4, 'refDurationStandardMode': 50, 'timeLimitSmartAveragingMode ': 10},
 'calibration': {'pka': 6.561, 'slope': 1.0, 'dphi_ref': 57.8, 'pka_t': -0.007344, 'dyn_t': -0.000645, 'bottom_t': -0.000834,
  'slope_t': 0.0, 'f': 0.03576, 'lambda_std': 623.0, 'pka_is1': 1.358, 'pka_is2': 0.250,
  'bkgdAmpl': 0.0, 'bkgdDphi': 0.0, 'offset': 0.0, 'dphi1': 17.58, 'pH1': 2.0,
  'temp1': 24.096, 'salinity1': 7.5, 'ldev1': 623.252, 'dphi2': 52.051, 'pH2': 14.0,
  'temp2': 20.0, 'salinity2': 7.5, 'ldev2': 623.0, 'Aon': 2.127515, 'Aoff': 0.12703,
  'date_calibration_acid': datetime.datetime(2022, 6, 23, 9, 23),
  'date_calibration_base': None,
  'date_calibration_offset': None}}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['comment', 'ambient_light', 'dphi', 'humidity', 'ldev', 'pH',
       'pressure', 'signal_intensity', 'status', 'case_temperature',
       'sample_temperature', 'time_s'], list(df.columns))
        self.assertEqual(265, len(df))
        self.assertDictEqual({'comment': np.nan,
 'ambient_light': 32.233,
 'dphi': 25.51,
 'humidity': 53.069,
 'ldev': 623.714,
 'pH': 6.452,
 'pressure': 975.434,
 'signal_intensity': 221.603,
 'status': 0.0,
 'case_temperature': 27.226,
 'sample_temperature': 24.11,
 'time_s': 300.024}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})
        self.assertDictEqual({'comment': np.nan, 'ambient_light': 32.233, 'dphi': 25.51,
 'humidity': 53.069, 'ldev': 623.714, 'pH': 6.452, 'pressure': 975.434, 'signal_intensity': 221.603,
 'status': 0.0, 'case_temperature': 27.226, 'sample_temperature': 24.11,
 'time_s': 300.024}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})


class TestDeveloperTool_v155(unittest.TestCase):
    directory = script_dir + '/testdata/developertool_v155/'

    def test_load_f1(self):
        file1 = "FSP20 247AA5035D64A770 2022-08-16 09'37'46 Ch1.txt"
        df, m = read_developertool(self.directory + file1)
        self.assertEqual({'software_version': 'PyroSimpleLogger\tv155\t(c) 2022 by\tPyroScience GmbH',
 'experiment_name': "FSP20 247AA5035D64A770 2022-08-16 09'37'46 Ch1.txt", 'experiment_description': '',
 'device': 'FSP20', 'uid': '247AA5035D64A770', 'firmware': '410:3', 'channel': '1',
 'settings': {'temperature': 25.0, 'pressure': 'internal sensor', 'salinity': 7.5, 'duration': '16ms',
  'intensity': '40%', 'amp': '400x', 'frequency': 3000, 'crc_enable': False, 'write_lock': False,
  'auto_flash_duration': False, 'auto_amp': True, 'analyte': 'pH', 'fiber_type': '1 mm', 'fiber_length_mm': 1000,
  'referenceMode': 'smart averaging', 'refDurationAveragingMode': 20, 'refDurationStandardMode': 50, 'timeLimitSmartAveragingMode ': 10},
 'calibration': {'R1': 1.76, 'pH1': 0.0, 'temp1': 20.0, 'salinity1': 7.5, 'R2': 0.078, 'pH2': 14.0,
  'temp2': 20.0, 'salinity2': 7.5, 'offset': 0.0, 'dphi_ref': 57.8, 'attenuation_coefficient': 0.0339, 'bkgdAmpl': 0.0,
  'bkgdDphi': 0.0, 'dsf_dye': 0.9049, 'dtf_dye': -0.00567, 'pka': 8.295, 'slope': 1.087, 'bottom_t': -0.0159, 'top_t': -0.002465,
  'slope_t': 0.0, 'pka_t': -0.01147, 'pka_is1': 2.54, 'pka_is2': 0.25, 'date_calibration_acid': None, 'date_calibration_base': None,
  'date_calibration_offset': None}}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['comment', 'R', 'ambient_light', 'dphi', 'humidity', 'pH', 'pressure',
       'signal_intensity', 'status', 'case_temperature', 'sample_temperature',
       'time_s'], list(df.columns))
        self.assertEqual(1782, len(df))
        self.assertDictEqual({'comment': np.nan, 'R': 2.529082, 'ambient_light': 0.347,
 'dphi': 14.531, 'humidity': 41.217, 'pH': np.nan, 'pressure': 969.176,
 'signal_intensity': 369.73, 'status': 32.0, 'case_temperature': 28.031, 'sample_temperature': np.nan,
 'time_s': 29.981}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})


class TestDeveloperTool_v157(unittest.TestCase):
    directory = script_dir + '/testdata/developertool_v157/'

    def test_load_f1(self):
        file1 = "PICO-OEM 2491CB0658B63D92 2022-11-15 Spot 1.txt"
        df, m = read_developertool(self.directory + file1)
        self.assertEqual({'software_version': 'PyroSimpleLogger\tv157\t(c) 2022 by\tPyroScience GmbH',
 'experiment_name': "PICO-OEM 2491CB0658B63D92 2022-11-15 14'54'09 Ch1.txt", 'experiment_description': '',
 'device': 'PICO-OEM', 'uid': '2491CB0658B63D92', 'firmware': '405:2', 'channel': '1',
 'settings': {'temperature': 'external sensor', 'pressure': 1013.0, 'salinity': 7.0, 'duration': '16ms', 'intensity': '10%',
  'amp': '400x', 'frequency': 4000, 'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True, 'auto_amp': True,
  'analyte': 'oxygen', 'fiber_type': '1 mm', 'fiber_length_mm': 2000, 'referenceMode': 'smart averaging', 'refDurationAveragingMode': 20,
  'refDurationStandardMode': 50, 'timeLimitSmartAveragingMode ': 10}, 'calibration': {'dphi0': 32.3, 'dphi100': 46.4, 'temp0': 20.0,
  'temp100': 20.0, 'pressure': 1013.0, 'humidity': 0.0, 'f': 0.804, 'm': 0.122, 'freq': 4000.0, 'tt': -0.00056, 'kt': 0.00969,
  'bkgdAmpl': 0.0, 'bkgdDphi': 0.0, 'ft': 0.0, 'mt': -0.000303, 'percentO2': 20.95, 'date_calibration_high': None, 'date_calibration_zero': None}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['comment', 'oxygen_%airsat', 'ambient_light', 'dphi', 'humidity',
       'oxygen_hPa', 'oxygen_%O2', 'pressure', 'signal_intensity', 'status',
       'case_temperature', 'sample_temperature', 'oxygen_µM', 'time_s'], list(df.columns))
        self.assertEqual(59475, len(df))
        self.assertDictEqual(df.iloc[1].to_dict(), {'comment': np.nan,
 'oxygen_%airsat': -111.434, 'ambient_light': 0.407, 'dphi': 24.435, 'humidity': 0.0, 'oxygen_hPa': -229.595, 'oxygen_%O2': -22.664,
 'pressure': 0.0, 'signal_intensity': 427.371, 'status': 0.0, 'case_temperature': 25.908, 'sample_temperature': 23.83, 'oxygen_µM': -281.975,
 'time_s': 0.974})
        self.assertDictEqual({'comment': np.nan, 'oxygen_%airsat': -111.434, 'ambient_light': 0.407, 'dphi': 24.435,
                              'humidity': 0.0, 'oxygen_hPa': -229.595, 'oxygen_%O2': -22.664, 'pressure': 0.0, 'signal_intensity': 427.371,
                              'status': 0.0, 'case_temperature': 25.908, 'sample_temperature': 23.83, 'oxygen_µM': -281.975,
                              'time_s': 0.974}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})


class TestDeveloperTool_v158(unittest.TestCase):
    directory = script_dir + '/testdata/developertool_v158/'

    def test_load_f1(self):
        file1 = "FireSting-PRO 24EB9B03596FD517 2023-03-15 09'29'46 Ch1.txt"
        df, m = read_developertool(self.directory + file1)
        self.assertEqual({'software_version': 'PyroSimpleLogger\tv158\t(c) 2022 by\tPyroScience GmbH',
 'experiment_name': "FireSting-PRO 24EB9B03596FD517 2023-03-15 09'29'46 Ch1.txt", 'experiment_description': '',
 'device': 'FireSting-PRO', 'uid': '24EB9B03596FD517', 'firmware': '411:1', 'channel': '1',
 'settings': {'temperature': 'external sensor', 'pressure': 'internal sensor', 'salinity': 7.5, 'duration': '16ms',
  'intensity': '10%', 'amp': '400x', 'frequency': 4000, 'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True,
  'auto_amp': True, 'analyte': 'oxygen', 'fiber_type': '1 mm', 'fiber_length_mm': 2000, 'referenceMode': 'smart averaging',
  'refDurationAveragingMode': 20, 'refDurationStandardMode': 50, 'timeLimitSmartAveragingMode ': 10}, 'calibration': {'dphi0': 50.0,
  'dphi100': 20.0, 'temp0': 20.0, 'temp100': 20.0, 'pressure': 1013.0, 'humidity': 0.0, 'f': 0.804, 'm': 0.122,
  'freq': 4000.0, 'tt': -0.00056, 'kt': 0.00969, 'bkgdAmpl': 0.0, 'bkgdDphi': 0.0, 'ft': 0.0, 'mt': -0.000303,
  'percentO2': 20.950, 'date_calibration_high': None, 'date_calibration_zero': None}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(sorted(['comment', 'status', 'dphi', 'oxygen_µM', 'oxygen_hPa',
       'oxygen_%airsat', 'sample_temperature', 'case_temperature',
       'signal_intensity', 'ambient_light', 'pressure', 'humidity',
       'oxygen_%O2', 'time_s']), sorted(df.columns))
        self.assertEqual(117, len(df))
        self.assertDictEqual({'comment': np.nan, 'oxygen_%airsat': -3.514, 'ambient_light': 0.217, 'dphi': 53.061,
                              'humidity': 49.647, 'oxygen_hPa': -6.915, 'oxygen_%O2': -0.713, 'pressure': 968.737, 'signal_intensity': 1659.394,
                              'status': 1.0, 'case_temperature': 9.648, 'sample_temperature': 23.735, 'oxygen_µM': -8.482, 'time_s': 4.956},
                             {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})

    def test_load_f2(self):
        file1 = "FSP15 249BC3015AC980E1 2024-05-23 15'12'14 Ch1.txt"
        df, m = read_developertool(self.directory + file1)
        self.assertEqual({'software_version': 'PyroSimpleLogger\tv158\t(c) 2022 by\tPyroScience GmbH',
 'experiment_name': "FSP15 249BC3015AC980E1 2024-05-23 15'12'14 Ch1.txt", 'experiment_description': '',
 'device': 'FSP15', 'uid': '249BC3015AC980E1', 'firmware': '411:1', 'channel': '1', 'settings': {'temperature': 'external sensor',
  'pressure': 'internal sensor', 'salinity': 7.5, 'duration': '16ms', 'intensity': '80%', 'amp': '400x',
  'frequency': 3000, 'crc_enable': False, 'write_lock': False, 'auto_flash_duration': False, 'auto_amp': True,
  'analyte': 'pH', 'fiber_type': '1 mm', 'fiber_length_mm': 1000, 'referenceMode': 'smart averaging', 'refDurationAveragingMode': 20,
  'refDurationStandardMode': 50, 'timeLimitSmartAveragingMode ': 10}, 'calibration': {'R1': 1.6, 'pH1': 0.0,
  'temp1': 20.0, 'salinity1': 7.5, 'R2': 0.1, 'pH2': 14.0, 'temp2': 20.0, 'salinity2': 7.5, 'offset': 0.0, 'dphi_ref': 57.8,
  'attenuation_coefficient': 0.03593, 'bkgdAmpl': 0.0, 'bkgdDphi': 0.0, 'dsf_dye': 0.9904, 'dtf_dye': -0.006321, 'pka': 7.051,
  'slope': 1.048, 'bottom_t': -0.007805, 'top_t': -0.00154, 'slope_t': 0.0, 'pka_t': -0.008985, 'pka_is1': 2.33,
  'pka_is2': 0.25, 'date_calibration_acid': None, 'date_calibration_base': None, 'date_calibration_offset': None}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(sorted(['comment', 'R', 'ambient_light', 'dphi', 'humidity', 'pH', 'pressure',
       'signal_intensity', 'status', 'case_temperature', 'sample_temperature',
       'time_s']), sorted(df.columns))
        self.assertEqual(32971, len(df))
        self.assertDictEqual({'comment': np.nan, 'R': 1.8122539999999998,
                              'ambient_light': 0.068, 'dphi': 18.174, 'humidity': 36.982, 'pH': np.nan,
                              'pressure': 973.338, 'signal_intensity': 1006.95, 'status': 32.0,
                              'case_temperature': 26.953, 'sample_temperature': np.nan, 'time_s': 1.001},
                             {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})


class TestDeveloperTool_v162(unittest.TestCase):
    directory = script_dir + '/testdata/developertool_v162/2024-07-01 DeveloperTool kompliziertes logfile erzeugen/'

    def test_load_f1(self):
        file1 = "FSP39 24EB9B03596FC737 2024-07-01 13'42'41 Ch1.txt"
        df, m = read_developertool(self.directory + file1)
        self.assertEqual({'software_version': 'PyroSimpleLogger\tv162\t(c) 2023 by\tPyroScience GmbH',
 'experiment_name': "FSP39 24EB9B03596FC737 2024-07-01 13'42'41 Ch1.txt", 'experiment_description': '',
 'device': 'FSP39', 'uid': '24EB9B03596FC737', 'firmware': '411:1', 'channel': '1',
 'settings': {'temperature': 'external sensor', 'pressure': 1013.0, 'salinity': 7.5, 'duration': '16ms', 'intensity': '15%',
  'amp': '400x', 'frequency': 4000, 'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True, 'auto_amp': True,
  'analyte': 'oxygen', 'fiber_type': '1 mm', 'fiber_length_mm': 1000, 'referenceMode': 'smart averaging', 'refDurationAveragingMode': 20,
  'refDurationStandardMode': 50, 'timeLimitSmartAveragingMode ': 10}, 'calibration': {'dphi0': 53.0,
  'dphi100': 20.0, 'temp0': 20.0, 'temp100': 20.0, 'pressure': 1013.0, 'humidity': 0.0, 'f': 0.804,
  'm': 0.122, 'freq': 4000.0, 'tt': -0.00056, 'kt': 0.00969, 'bkgdAmpl': 0.584, 'bkgdDphi': 0.0, 'ft': 0.0,
  'mt': -0.000303, 'percentO2': 20.95, 'date_calibration_high': None, 'date_calibration_zero': None}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(sorted(['comment', 'status', 'dphi', 'oxygen_µM', 'oxygen_hPa',
       'oxygen_%airsat', 'sample_temperature', 'case_temperature',
       'signal_intensity', 'ambient_light', 'pressure', 'humidity',
       'oxygen_%O2', 'time_s']), sorted(df.columns))
        self.assertEqual(14, len(df))
        self.assertDictEqual({'comment': np.nan, 'oxygen_%airsat': np.nan, 'ambient_light': 46.65,
 'dphi': 177.861, 'humidity': 49.587, 'oxygen_hPa': np.nan, 'oxygen_%O2': np.nan, 'pressure': 970.921,
 'signal_intensity': 1.059, 'status': 34.0, 'case_temperature': 28.468, 'sample_temperature': np.nan, 'oxygen_µM': np.nan,
 'time_s': 0.976}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})

    def test_load_f2(self):
        file1 = "FSP39 24EB9B03596FC737 2024-07-01 13'42'41 Ch2.txt"
        df, m = read_developertool(self.directory + file1)
        self.assertEqual({'software_version': 'PyroSimpleLogger\tv162\t(c) 2023 by\tPyroScience GmbH',
 'experiment_name': "FSP39 24EB9B03596FC737 2024-07-01 13'42'41 Ch2.txt", 'experiment_description': '',
 'device': 'FSP39', 'uid': '24EB9B03596FC737', 'firmware': '411:1', 'channel': '2',
 'settings': {'temperature': 'internal sensor', 'pressure': 'internal sensor', 'salinity': 7.5, 'duration': '16ms', 'intensity': '60%',
  'amp': '400x', 'frequency': 3000, 'crc_enable': False, 'write_lock': False, 'auto_flash_duration': False, 'auto_amp': True,
  'analyte': 'pH', 'fiber_type': '1 mm', 'fiber_length_mm': 0, 'referenceMode': 'smart averaging', 'refDurationAveragingMode': 20,
  'refDurationStandardMode': 50, 'timeLimitSmartAveragingMode ': 10}, 'calibration': {'R1': 1.6, 'pH1': 0.0,
  'temp1': 20.0, 'salinity1': 7.5, 'R2': 0.1, 'pH2': 14.0, 'temp2': 20.0, 'salinity2': 7.5, 'offset': 0.0,
  'dphi_ref': 57.8, 'attenuation_coefficient': 0.0339, 'bkgdAmpl': 0.044, 'bkgdDphi': 0.0, 'dsf_dye': 0.9047, 'dtf_dye': -0.00567,
  'pka': 8.031, 'slope': 1.034, 'bottom_t': -0.001108, 'top_t': -0.000803, 'slope_t': 0.0, 'pka_t': -0.01628,
  'pka_is1': 0.97, 'pka_is2': 0.126, 'date_calibration_acid': None, 'date_calibration_base': None, 'date_calibration_offset': None}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(sorted(['comment', 'status', 'dphi', 'sample_temperature', 'case_temperature',
       'signal_intensity', 'ambient_light', 'pressure', 'humidity', 'pH', 'R', 'time_s']), sorted(df.columns))
        self.assertEqual(14, len(df))
        self.assertDictEqual({'comment': np.nan, 'R': 11.285887, 'ambient_light': 55.488,
 'dphi': -175.978, 'humidity': 49.599, 'pH': np.nan, 'pressure': 970.94,
 'signal_intensity': 0.636, 'status': 34.0, 'case_temperature': 28.398, 'sample_temperature': np.nan,
 'time_s': 0.98}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})

    def test_load_f3(self):
        file1 = "FSP39 24EB9B03596FC737 2024-07-01 13'42'41 Ch3.txt"
        df, m = read_developertool(self.directory + file1)
        self.assertEqual({'software_version': 'PyroSimpleLogger\tv162\t(c) 2023 by\tPyroScience GmbH',
 'experiment_name': "FSP39 24EB9B03596FC737 2024-07-01 13'42'41 Ch3.txt",
 'experiment_description': '', 'device': 'FSP39', 'uid': '24EB9B03596FC737', 'firmware': '411:1',
 'channel': '3', 'settings': {'temperature': 20.0, 'pressure': 'internal sensor', 'salinity': 0.0,
  'duration': '128ms', 'intensity': '60%', 'amp': '400x', 'frequency': 970, 'crc_enable': False, 'write_lock': False,
  'auto_flash_duration': True, 'auto_amp': True, 'analyte': 'temperature', 'fiber_type': '1 mm', 'fiber_length_mm': 1000,
  'referenceMode': 'smart averaging', 'refDurationAveragingMode': 20, 'refDurationStandardMode': 50, 'timeLimitSmartAveragingMode ': 10},
 'calibration': {'M': 400.0, 'N': 500.0, 'C': 0.097, 'temp_offset': 0.0, 'bkgdAmpl': 0.584, 'bkgdDphi': 0.0,
  'date_calibration_offset': None}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(sorted(['comment', 'status', 'dphi', 'sample_temperature', 'case_temperature',
       'signal_intensity', 'ambient_light', 'pressure', 'humidity',
       'optical_temperature', 'time_s']), sorted(df.columns))
        self.assertEqual(14, len(df))

    def test_load_f4(self):
        file1 = "FSP39 24EB9B03596FC737 2024-07-01 13'42'41 Ch4.txt"
        df, m = read_developertool(self.directory + file1)
        self.assertEqual({'software_version': 'PyroSimpleLogger\tv162\t(c) 2023 by\tPyroScience GmbH',
 'experiment_name': "FSP39 24EB9B03596FC737 2024-07-01 13'42'41 Ch4.txt", 'experiment_description': '',
 'device': 'FSP39', 'uid': '24EB9B03596FC737', 'firmware': '411:1', 'channel': '4',
 'settings': {'temperature': 'Optical Temperature Sensor on Channel 3', 'pressure': 'internal sensor',
  'salinity': 7.5, 'duration': '16ms', 'intensity': '20%', 'amp': '400x', 'frequency': 4000, 'crc_enable': False,
  'write_lock': False, 'auto_flash_duration': True, 'auto_amp': True, 'analyte': 'oxygen', 'fiber_type': '1 mm',
  'fiber_length_mm': 1000, 'referenceMode': 'smart averaging', 'refDurationAveragingMode': 20, 'refDurationStandardMode': 50,
  'timeLimitSmartAveragingMode ': 10}, 'calibration': {'dphi0': 53.0, 'dphi100': 20.0, 'temp0': 20.0, 'temp100': 20.0,
  'pressure': 1013.0, 'humidity': 0.0, 'f': 0.804, 'm': 0.122, 'freq': 4000.0, 'tt': -0.00056, 'kt': 0.00969,
  'bkgdAmpl': 0.584, 'bkgdDphi': 0.0, 'ft': 0.0, 'mt': -0.000303, 'percentO2': 20.95,
  'date_calibration_high': None, 'date_calibration_zero': None}}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(sorted(['comment', 'status', 'dphi', 'oxygen_µM', 'oxygen_hPa',
       'oxygen_%airsat', 'sample_temperature', 'case_temperature',
       'signal_intensity', 'ambient_light', 'pressure', 'humidity',
       'oxygen_%O2', 'time_s']), sorted(df.columns))
        self.assertEqual(14, len(df))


if __name__ == '__main__':
    unittest.main()
