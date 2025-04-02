import unittest

from pyrotoolbox.parsers import read_aquaphoxlogger
import datetime
import numpy as np
import os

script_dir = os.path.dirname(__file__)


class AquapHOx_400(unittest.TestCase):
    directory = script_dir + '/testdata/aquaphox_400/'

    def test_load_f1(self):
        file1 = "2020-01-13 14_44 AUSTE01.txt"
        df, m = read_aquaphoxlogger(self.directory + file1)
        self.assertEqual({'experiment_name': 'AUS01', 'experiment_description': '', 'device': 'FireSting sub',
 'uid': '24C53408575BA55E', 'firmware': '400:6', 'software_version': 'Firmware 400:6', 'channel': '1',
 'settings': {'temperature': 'external sensor', 'pressure': 1006.0, 'salinity': 31.0, 'duration': '64ms', 'intensity': '30%',
  'amp': '40x', 'frequency': 3000, 'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True, 'auto_amp': True,
  'analyte': 'pH', 'fiber_type': '1 mm', 'referenceMode': 'smart averaging', 'refDurationAveragingMode': 4, 'refDurationStandardMode': 50,
  'timeLimitSmartAveragingMode ': 10}, 'calibration': {'pka': 7.94, 'slope': 1032.0, 'dphi_ref': 57.8,
  'pka_t': -0.0115, 'dyn_t': -0.00209, 'bottom_t': 0.000199, 'slope_t': 0.0, 'f': 0.0325, 'lambda_std': 623.0,
  'pka_is1': 0.0, 'pka_is2': 0.0, 'bkgdAmpl': 0.0, 'bkgdDphi': 0.0, 'offset': 0.0, 'dphi1': 16.912, 'pH1': 4.01,
  'temp1': 22.67, 'salinity1': 7.5, 'ldev1': 624.037, 'dphi2': 53.564, 'pH2': 10.03, 'temp2': 22.563, 'salinity2': 7.5,
  'ldev2': 623.929, 'Aon': 2191.039, 'Aoff': 72.49}}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['status', 'dphi', 'sample_temperature', 'case_temperature',
       'signal_intensity', 'ambient_light', 'pressure', 'humidity', 'pH',
       'ldev', 'time_s'], list(df.columns))
        self.assertEqual(4440, len(df))
        self.assertDictEqual({'status': 0.0, 'dphi': 18.468, 'sample_temperature': 8.088, 'case_temperature': 11.51,
 'signal_intensity': 183.576, 'ambient_light': 1.805, 'pressure': 1055.502, 'humidity': 16.302, 'pH': 6.952,
 'ldev': 621.801, 'time_s': 600.0}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})


class AquapHOx_403(unittest.TestCase):
    directory = script_dir + '/testdata/aquaphox_403/'

    def test_load_f1(self):
        file1 = "2020-08-13 Aquakultur.txt"
        df, m = read_aquaphoxlogger(self.directory + file1)
        self.assertEqual({'experiment_name': 'AQUACULT', 'experiment_description': '',
 'device': 'AquapHOx L1', 'uid': '24967102575BA4F1', 'firmware': '403:1', 'software_version': 'Firmware 403:1',
 'channel': '1', 'settings': {'temperature': 'external sensor', 'pressure': 1013.0, 'salinity': 35.0, 'duration': '16ms',
  'intensity': '10%', 'amp': '400x', 'frequency': 4000, 'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True,
  'auto_amp': True, 'analyte': 'oxygen', 'fiber_type': '1 mm', 'referenceMode': 'smart averaging', 'refDurationAveragingMode': 4,
  'refDurationStandardMode': 50, 'timeLimitSmartAveragingMode ': 10}, 'calibration': {'dphi0': 53.481, 'dphi100': 21.887,
  'temp0': 25.742, 'temp100': 22.849, 'pressure': 973.3, 'humidity': 58.0, 'f': 0.804, 'm': 0.122, 'freq': 4000.0,
  'tt': -0.00056, 'kt': 0.00969, 'bkgdAmpl': 0.0, 'bkgdDphi': 0.0, 'ft': 0.0, 'mt': -0.000303,
  'percentO2': 20.95}}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['status', 'dphi', 'oxygen_µM', 'oxygen_hPa', 'oxygen_%airsat',
       'sample_temperature', 'case_temperature', 'signal_intensity',
       'ambient_light', 'pressure', 'humidity', 'oxygen_%O2', 'time_s'], list(df.columns))
        self.assertEqual(13758, len(df))
        self.assertDictEqual({'status': 0.0, 'dphi': 21.752, 'oxygen_µM': 199.918, 'oxygen_hPa': 197.116,
 'oxygen_%airsat': 96.038, 'sample_temperature': 25.841, 'case_temperature': 26.38, 'signal_intensity': 467.036, 'ambient_light': 1.002,
 'pressure': 1078.841, 'humidity': 19.332, 'oxygen_%O2': 19.458, 'time_s': 300.0},
                             {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})


class AquapHOx_405(unittest.TestCase):
    directory = script_dir + '/testdata/aquaphox_405/'

    def test_load_f1(self):
        file1 = "2021-12-02 14_23 WSEE2.txt"
        df, m = read_aquaphoxlogger(self.directory + file1)
        self.assertEqual({'experiment_name': 'wsee2', 'experiment_description': '', 'device': 'AquapHOx-LX',
                          'uid': '24EB9B04575BA4FC', 'firmware': '405:3', 'software_version': 'Firmware 405:3', 'channel': '1',
                          'settings': {'temperature': 'external sensor', 'pressure': 1013.0, 'salinity': 0.375, 'duration': '16ms',
                                       'intensity': '30%', 'amp': '400x', 'frequency': 3000, 'crc_enable': False, 'write_lock': False, 'auto_flash_duration': False,
                                       'auto_amp': True, 'analyte': 'pH', 'fiber_type': '1 mm', 'referenceMode': 'smart averaging', 'refDurationAveragingMode': 20,
                                       'refDurationStandardMode': 50, 'timeLimitSmartAveragingMode ': 10}, 'calibration': {'pka': 7.051, 'slope': 1037.0,
                                                                                                                           'dphi_ref': 57.8, 'pka_t': -0.00957, 'dyn_t': -0.000955, 'bottom_t': -0.000677, 'slope_t': 0.0, 'f': 0.0395,
                                                                                                                           'lambda_std': 623.0, 'pka_is1': 2330.0, 'pka_is2': 250.0, 'bkgdAmpl': 0.343, 'bkgdDphi': 0.0, 'offset': 0.0,
                                                                                                                           'dphi1': 22.597, 'pH1': 2.272, 'temp1': 24.287, 'salinity1': 2.0, 'ldev1': 623.062, 'dphi2': 54.566, 'pH2': 11.191,
                                                                                                                           'temp2': 24.0, 'salinity2': 6.0, 'ldev2': 623.004, 'Aon': 0.0, 'Aoff': 0.0,
                                                                                                                           'date_calibration_acid': datetime.datetime(2021, 12, 2, 13, 38),
                                                                                                                           'date_calibration_base': datetime.datetime(2021, 12, 2, 14, 21),
                                                                                                                           'date_calibration_offset': None}, 'sensor_code': 'FAD7-257-072'}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['status', 'dphi', 'sample_temperature', 'case_temperature',
                          'signal_intensity', 'ambient_light', 'pressure', 'humidity', 'pH',
                          'ldev', 'time_s'], list(df.columns))
        self.assertEqual(22280, len(df))
        self.assertDictEqual({'status': 0.0, 'dphi': 35.158, 'sample_temperature': 28.524, 'case_temperature': 24.6,
                              'signal_intensity': 466.722, 'ambient_light': 26.979, 'pressure': 971.262, 'humidity': 36.973,
                              'pH': 7.298, 'ldev': 622.94, 'time_s': 600.0}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})

    def test_load_f2(self):
        file1 = "2021-09-29 09_33 ULVIK29S.txt"
        df, m = read_aquaphoxlogger(self.directory + file1)
        self.assertEqual({'experiment_name': 'ULVIK29S', 'experiment_description': '', 'device': 'AquapHOx-L-pH',
                          'uid': '24E4C301575BA56A', 'firmware': '405:3', 'software_version': 'Firmware 405:3', 'channel': '1',
                          'settings': {'temperature': 'external sensor', 'pressure': 'internal sensor', 'salinity': 35.0, 'duration': '16ms',
                                       'intensity': '15%', 'amp': '400x', 'frequency': 3000, 'crc_enable': False, 'write_lock': False, 'auto_flash_duration': False,
                                       'auto_amp': True, 'analyte': 'pH', 'fiber_type': '1 mm', 'referenceMode': 'smart averaging', 'refDurationAveragingMode': 20,
                                       'refDurationStandardMode': 50, 'timeLimitSmartAveragingMode ': 10}, 'calibration': {'pka': 8.009, 'slope': 1033.0,
                                                                                                                           'dphi_ref': 57.8, 'pka_t': -0.0163, 'dyn_t': -0.000521, 'bottom_t': -0.001255, 'slope_t': 0.0, 'f': 0.0325,
                                                                                                                           'lambda_std': 623.0, 'pka_is1': 969.7, 'pka_is2': 126.3, 'bkgdAmpl': 0.343, 'bkgdDphi': 0.0, 'offset': 0.0,
                                                                                                                           'dphi1': 16.952, 'pH1': 2.246, 'temp1': 27.3, 'salinity1': 2.0, 'ldev1': 624.024, 'dphi2': 53.732, 'pH2': 10.0,
                                                                                                                           'temp2': 26.966, 'salinity2': 6.5, 'ldev2': 624.056, 'Aon': 2186.741, 'Aoff': 73.231,
                                                                                                                           'date_calibration_acid': datetime.datetime(2021, 7, 26, 18, 43),
                                                                                                                           'date_calibration_base': datetime.datetime(2021, 7, 26, 18, 55),
                                                                                                                           'date_calibration_offset': None},
                          'sensor_code': 'FCB7-392-881'}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['status', 'dphi', 'sample_temperature', 'case_temperature',
                          'signal_intensity', 'ambient_light', 'pressure', 'humidity', 'pH',
                          'ldev', 'time_s'], list(df.columns))
        self.assertEqual(6348, len(df))
        self.assertDictEqual({'status': 0.0, 'dphi': 28.738, 'sample_temperature': 20.207, 'case_temperature': 12.57,
                              'signal_intensity': 165.73, 'ambient_light': 3.765, 'pressure': 995.552, 'humidity': 36.956, 'pH': 7.997,
                              'ldev': 620.926, 'time_s': 600.0}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})

class AquapHOx_410(unittest.TestCase):
    directory = script_dir + '/testdata/aquaphox_410/'

    def test_load_f1(self):
        file1 = "2024-06-11 08_55 POST.txt"
        df, m = read_aquaphoxlogger(self.directory + file1)
        self.assertEqual({'experiment_name': 'POST', 'experiment_description': '', 'device': 'AquapHOx-L-O2',
 'uid': '24C53407596FCADA', 'firmware': '410:5', 'software_version': 'Firmware 410:5', 'channel': '1',
 'settings': {'temperature': 'external sensor', 'pressure': 1013.0, 'salinity': 35.0, 'duration': '16ms',
  'intensity': '10%', 'amp': '200x', 'frequency': 4000, 'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True,
  'auto_amp': True, 'analyte': 'oxygen', 'fiber_type': '1 mm', 'referenceMode': 'smart averaging', 'refDurationAveragingMode': 20,
  'refDurationStandardMode': 50, 'timeLimitSmartAveragingMode ': 10}, 'calibration': {'dphi0': 53.819, 'dphi100': 21.834,
  'temp0': 25.051, 'temp100': 23.457, 'pressure': 969.0, 'humidity': 51.0, 'f': 0.804, 'm': 0.122, 'freq': 4000.0,
  'tt': -0.00056, 'kt': 0.00969, 'bkgdAmpl': 0.0, 'bkgdDphi': 0.0, 'ft': 0.0, 'mt': -0.000303, 'percentO2': 20.95,
  'date_calibration_high': datetime.datetime(2024, 6, 11, 8, 52),
  'date_calibration_zero': datetime.datetime(2024, 6, 11, 8, 55)},
 'sensor_code': 'SA6-540-205'}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['status', 'dphi', 'oxygen_µM', 'oxygen_hPa', 'oxygen_%airsat',
       'sample_temperature', 'case_temperature', 'signal_intensity',
       'ambient_light', 'pressure', 'humidity', 'oxygen_%O2', 'time_s'], list(df.columns))
        self.assertEqual(2, len(df))
        self.assertDictEqual({'status': 0.0, 'dphi': 53.842, 'oxygen_µM': -0.051, 'oxygen_hPa': -0.049,
 'oxygen_%airsat': -0.024, 'sample_temperature': 25.042, 'case_temperature': 25.2, 'signal_intensity': 1022.71, 'ambient_light': 0.361,
 'pressure': 1032.634, 'humidity': 49.351, 'oxygen_%O2': -0.004, 'time_s': 10.0}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})

    def test_load_f2(self):
        file1 = "2023-08-17 14_26 AFNETZ.txt"
        df, m = read_aquaphoxlogger(self.directory + file1)
        self.assertEqual({'experiment_name': 'AFNETZ',
 'experiment_description': 'Neue_anti_fouling_folie_fox484_mit_innerem_und_äußeren_netz', 'device': 'AquapHOx-L-O2',
 'uid': '24C53407596FCADA', 'firmware': '410:5', 'software_version': 'Firmware 410:5', 'channel': '1',
 'settings': {'temperature': 'external sensor', 'pressure': 1013.0, 'salinity': 35.0, 'duration': '16ms',
  'intensity': '10%', 'amp': '200x', 'frequency': 4000, 'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True,
  'auto_amp': True, 'analyte': 'oxygen', 'fiber_type': '1 mm', 'referenceMode': 'smart averaging', 'refDurationAveragingMode': 20,
  'refDurationStandardMode': 50, 'timeLimitSmartAveragingMode ': 10}, 'calibration': {'dphi0': 53.728, 'dphi100': 20.597,
  'temp0': 28.627, 'temp100': 28.282, 'pressure': 976.0, 'humidity': 55.0, 'f': 0.804, 'm': 0.122,
  'freq': 4000.0, 'tt': -0.00056, 'kt': 0.00969, 'bkgdAmpl': 0.0, 'bkgdDphi': 0.0, 'ft': 0.0, 'mt': -0.000303,
  'percentO2': 20.95, 'date_calibration_high': datetime.datetime(2023, 8, 17, 13, 42),
  'date_calibration_zero': datetime.datetime(2023, 8, 17, 14, 25)},
 'sensor_code': 'SA6-540-205'}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['status', 'dphi', 'oxygen_µM', 'oxygen_hPa', 'oxygen_%airsat',
       'sample_temperature', 'case_temperature', 'signal_intensity',
       'ambient_light', 'pressure', 'humidity', 'oxygen_%O2', 'time_s'], list(df.columns))
        self.assertEqual(858553, len(df))
        self.assertDictEqual({'status': 0.0, 'dphi': 53.771, 'oxygen_µM': -0.084, 'oxygen_hPa': -0.086,
 'oxygen_%airsat': -0.042, 'sample_temperature': 28.672, 'case_temperature': 30.26, 'signal_intensity': 603.79, 'ambient_light': 3.753,
 'pressure': 1042.969, 'humidity': 27.794, 'oxygen_%O2': -0.008, 'time_s': 30.0}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})

    def test_load_f3(self):
        file1 = "563OHNE.txt"
        df, m = read_aquaphoxlogger(self.directory + file1)
        self.assertEqual({'experiment_name': '563OHNE', 'experiment_description': 'pk8_mit_zineb_563_ohne_Kupfer_Netz',
 'device': 'AquapHOx-LX', 'uid': '2411E505575BA512', 'firmware': '410:5', 'software_version': 'Firmware 410:5',
 'channel': '1', 'settings': {'temperature': 'external sensor', 'pressure': 1013.0, 'salinity': 35.0,
  'duration': '16ms', 'intensity': '60%', 'amp': '400x', 'frequency': 3000, 'crc_enable': False, 'write_lock': False,
  'auto_flash_duration': False, 'auto_amp': True, 'analyte': 'pH', 'fiber_type': '1 mm', 'referenceMode': 'smart averaging',
  'refDurationAveragingMode': 20, 'refDurationStandardMode': 50, 'timeLimitSmartAveragingMode ': 10},
 'calibration': {'R1': 0.045034, 'pH1': 11.0, 'temp1': 29.605, 'salinity1': 2.0, 'R2': 0.1, 'pH2': 14.0, 'temp2': 20.0,
  'salinity2': 7.5, 'offset': 0.0, 'dphi_ref': 57.8, 'attenuation_coefficient': 0.0339, 'bkgdAmpl': 0.0,
  'bkgdDphi': 0.0, 'dsf_dye': 0.9047, 'dtf_dye': -0.00567, 'pka': 8.301, 'slope': 1.087, 'bottom_t': -0.0159,
  'top_t': -0.002465, 'slope_t': 0.0, 'pka_t': -0.01147, 'pka_is1': 2.54, 'pka_is2': 0.25,
  'date_calibration_acid': datetime.datetime(2023, 8, 17, 15, 28),
  'date_calibration_base': datetime.datetime(2022, 5, 12, 16, 32),
  'date_calibration_offset': None}, 'sensor_code': 'XHF7-505-050'}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['status', 'dphi', 'sample_temperature', 'case_temperature',
       'signal_intensity', 'ambient_light', 'pressure', 'humidity', 'pH', 'R',
       'time_s'], list(df.columns))
        self.assertEqual(258920, len(df))
        self.assertDictEqual({'status': 0.0, 'dphi': 55.082, 'sample_temperature': 29.644, 'case_temperature': 30.69,
 'signal_intensity': 299.555, 'ambient_light': 35.038, 'pressure': 986.342, 'humidity': 34.106,
 'pH': 10.995, 'R': 0.055965, 'time_s': 30.0}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})

    def test_load_f4(self):
        file1 = "2024-04-08 13_46 PH1ROV_Stegende links.txt"
        df, m = read_aquaphoxlogger(self.directory + file1)
        self.assertEqual({'experiment_name': 'pH1Rov',
 'experiment_description': 'pK8T_std_ohne_Cu_Netz_Rov_start_0904', 'device': 'AquapHOx-LX',
 'uid': '24967102575BA4F1', 'device_serial': '0', 'firmware': '410:6', 'software_version': 'Firmware 410:6', 'channel': '1',
 'settings': {'temperature': 'external sensor', 'pressure': 'internal sensor', 'salinity': 35.0, 'duration': '16ms',
  'intensity': '30%', 'amp': '400x', 'frequency': 3000, 'crc_enable': False, 'write_lock': False,
  'auto_flash_duration': False, 'auto_amp': True, 'analyte': 'pH', 'fiber_type': '1 mm', 'referenceMode': 'smart averaging',
  'refDurationAveragingMode': 20, 'refDurationStandardMode': 50, 'timeLimitSmartAveragingMode ': 10}, 'calibration': {'R1': 1.628864,
  'pH1': 2.261, 'temp1': 25.514, 'salinity1': 2.0, 'R2': 0.048546, 'pH2': 11.23, 'temp2': 25.734, 'salinity2': 6.0,
  'offset': 0.0, 'dphi_ref': 57.8, 'attenuation_coefficient': 0.0339, 'bkgdAmpl': 0.044, 'bkgdDphi': 0.0,
  'dsf_dye': 0.9047, 'dtf_dye': -0.00567, 'pka': 8.104, 'slope': 1.034, 'bottom_t': -0.001108, 'top_t': -0.000803,
  'slope_t': 0.0, 'pka_t': -0.01628, 'pka_is1': 0.97, 'pka_is2': 0.126, 'date_calibration_acid': datetime.datetime(2024, 4, 8, 13, 35),
  'date_calibration_base': datetime.datetime(2024, 4, 8, 13, 41),
  'date_calibration_offset': None},
 'sensor_code': 'FID7-867-931'}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['status', 'dphi', 'sample_temperature', 'case_temperature',
       'signal_intensity', 'ambient_light', 'pressure', 'humidity', 'pH', 'R',
       'time_s'], list(df.columns))
        self.assertEqual(132623, len(df))
        self.assertDictEqual({'status': 0.0, 'dphi': 53.939,
 'sample_temperature': 25.841, 'case_temperature': 27.11, 'signal_intensity': 234.234, 'ambient_light': 29.447,
 'pressure': 981.114, 'humidity': 29.716, 'pH': 9.658, 'R': 0.0823, 'time_s': 60.0}, {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})


if __name__ == '__main__':
    unittest.main()
