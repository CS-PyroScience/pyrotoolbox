import unittest

from pyrotoolbox.parsers import read_workbench
import numpy as np
import datetime
import os

script_dir = os.path.dirname(__file__)


class TestWorkbench_1_0_20(unittest.TestCase):
    directory = script_dir + '/testdata/workbench_V1.0.20/'

    def test_load_f1(self):
        file1 = 'Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'Ecoli_AllSensors_FireStingPro1905171DO2pH3Temp',
                          'experiment_description': '', 'software_version': 'Workbench V1.0.20',
                          'device': 'FireSting pro [A] FSPLUS-4',
                          'device_serial': '', 'uid': '2466C2065AC97E6E', 'firmware': '4.01:007', 'channel': 1,
                          'sensor_code': 'SD7-531-196',
                          'settings': {'duration': '16 ms', 'intensity': '30%', 'amp': '400x', 'frequency': 4000,
                                       'crc_enable': False,
                                       'write_lock': False, 'auto_flash_duration': True, 'auto_amp': True,
                                       'analyte': 'oxygen', 'fiber_type': '1 mm',
                                       'temperature': 'external sensor', 'pressure': 'internal sensor',
                                       'salinity': 0.7}, 'calibration':
                              {'date_calibration_high': datetime.datetime(2019, 5, 17, 0, 0),
                               'date_calibration_zero': None,
                               'dphi100': 19.409, 'dphi0': 53.1, 'f': 0.804, 'm': 0.122, 'freq': 4000.0, 'tt': 0.00969,
                               'kt': -0.00056, 'bkgdAmpl': 0.577,
                               'bkgdDphi': 0.0, 'mt': -0.0, 'pressure': 1001.635, 'temp100': 40.513,
                               'humidity': 100.0, 'temp0': 20.0,
                               'percentO2': 20.95}}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['oxygen_%airsat', 'oxygen_µM', 'oxygen_hPa', 'oxygen_%airsat', 'oxygen_%O2', 'dphi',
                          'signal_intensity', 'ambient_light', 'status', 'sample_temperature', 'pressure'],
                         list(df.columns))
        self.assertEqual(37021, len(df))

    def test_load_f2(self):
        file1 = 'Firesting Pro (4 Channels)_(A Ch.2)_pH.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'Ecoli_AllSensors_FireStingPro1905171DO2pH3Temp',
                          'experiment_description': '\n', 'software_version': 'Workbench V1.0.20',
                          'device': 'FireSting pro [A] FSPLUS-4', 'device_serial': '',
                          'uid': '2466C2065AC97E6E', 'firmware': '4.01:007', 'channel': 2,
                          'sensor_code': 'SAF7-319-933', 'settings': {'duration': '64 ms', 'intensity': '60%',
                                                                      'amp': '400x', 'frequency': 3000,
                                                                      'crc_enable': False, 'write_lock': False,
                                                                      'auto_flash_duration': True, 'auto_amp': True,
                                                                      'analyte': 'pH', 'fiber_type': '1 mm',
                                                                      'temperature': 'external sensor',
                                                                      'pressure': 'internal sensor', 'salinity': 10.0},
                          'calibration': {'date_calibration_acid': datetime.datetime(2019, 5, 17, 0, 0),
                                          'date_calibration_base': None, 'date_calibration_offset': None, 'pka': 7.063,
                                          'slope': 1.039, 'dphi_ref': 56.21, 'pka_t': -0.01,
                                          'dyn_t': -0.0, 'bottom_t': -0.0, 'slope_t': 0.0, 'f': 0.04,
                                          'lambda_std': 623.0, 'pka_is1': 1.0, 'pka_is2': 0.3, 'bkgdAmpl': 0.577,
                                          'bkgdDphi': 0.0, 'offset': 0.0, 'dphi1': 23.116, 'pH1': 4.012, 'temp1': 23.0,
                                          'salinity1': 2.0, 'ldev1': 626.428, 'dphi2': 50.333,
                                          'pH2': 14.0, 'temp2': 20.0, 'salinity2': 7.5, 'ldev2': 623.0, 'Aon': 0.0,
                                          'Aoff': 0.0}, }, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['pH', 'dphi', 'signal_intensity', 'ambient_light', 'ldev', 'status'], list(df.columns))
        self.assertEqual(37020, len(df))

    def test_load_f4(self):
        file1 = 'Firesting Pro (4 Channels)_(A Ch.3)_pH.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'Ecoli_AllSensors_FireStingPro',
                          'experiment_description': '1905171\nDO2\npH3\nTemp\n\n',
                          'software_version': 'Workbench V1.0.20', 'device': 'FireSting pro [A] FSPLUS-4',
                          'device_serial': '', 'uid': '2466C2065AC97E6E',
                          'firmware': '4.01:007', 'channel': 2, 'sensor_code': 'SAF7-319-933',
                          'settings': {'duration': '64 ms', 'intensity': '60%', 'amp': '400x',

                                       'frequency': 3000, 'crc_enable': False, 'write_lock': False,
                                       'auto_flash_duration': True, 'auto_amp': True, 'analyte': 'pH',
                                       'fiber_type': '1 mm',
                                       'temperature': 'external sensor', 'pressure': 'internal sensor',
                                       'salinity': 10.0},
                          'calibration': {'date_calibration_acid': datetime.datetime(2019, 5, 17, 0, 0),
                                          'date_calibration_base': None, 'date_calibration_offset': None, 'pka': 7.063,
                                          'slope': 1.039, 'dphi_ref': 56.21, 'pka_t': -0.01,
                                          'dyn_t': -0.0, 'bottom_t': -0.0, 'slope_t': 0.0, 'f': 0.04,
                                          'lambda_std': 623.0, 'pka_is1': 1.0, 'pka_is2': 0.3, 'bkgdAmpl': 0.577,
                                          'bkgdDphi': 0.0, 'offset': 0.0, 'dphi1': 23.116, 'pH1': 4.012, 'temp1': 23.0,
                                          'salinity1': 2.0, 'ldev1': 626.428, 'dphi2': 50.333,
                                          'pH2': 14.0, 'temp2': 20.0, 'salinity2': 7.5, 'ldev2': 623.0, 'Aon': 0.0,
                                          'Aoff': 0.0}, },
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['pH', 'dphi', 'signal_intensity', 'ambient_light', 'ldev', 'status'], list(df.columns))
        self.assertEqual(37020, len(df))


class TestWorkbench_1_0_24(unittest.TestCase):
    directory = script_dir + '/testdata/workbench_V1.0.24/'

    def test_load_f1(self):
        file1 = 'Firesting Pro (4 Channels)_(A Ch.1)_pH.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': '20190521_Klimaschrank_PK7',
                          'experiment_description': 'Neuer Klimaschrank Test mit neuen Firestings von Aachen. Firesting A, C und D  sind mit eigener lamda steigung. B ist mti 0.15nm/K, pH 6.5 puffer phosphat. 2 punkt kalibriert zuvor (acetat, kapsel), Klimaschrank von 40 grad auf 5 grad und wieder rauf\n',
                          'software_version': 'Workbench V1.0.24', 'device': 'FireSting pro [A] FSPLUS-4',
                          'device_serial': '', 'uid': '249BC3015AC980E1',
                          'firmware': '4.01:007', 'channel': 1, 'sensor_code': 'SAD7-255-050',
                          'settings': {'duration': '64 ms', 'intensity': '30%',
                                       'amp': '400x', 'frequency': 3000, 'crc_enable': False, 'write_lock': False,
                                       'auto_flash_duration': True, 'auto_amp': True,
                                       'analyte': 'pH', 'fiber_type': '1 mm', 'temperature': 'external sensor',
                                       'pressure': 'internal sensor', 'salinity': 9.0},
                          'calibration': {'date_calibration_acid': datetime.datetime(2019, 5, 21, 0, 0),
                                          'date_calibration_base': datetime.datetime(2019, 5, 21, 0, 0),
                                          'date_calibration_offset': None, 'pka': 7.051, 'slope': 1.039,
                                          'dphi_ref': 56.21, 'pka_t': -0.01, 'dyn_t': -0.0,
                                          'bottom_t': -0.0, 'slope_t': 0.0, 'f': 0.04, 'lambda_std': 623.0,
                                          'pka_is1': 1.0, 'pka_is2': 0.3, 'bkgdAmpl': 0.811, 'bkgdDphi': 0.0,
                                          'offset': 0.0, 'dphi1': 18.225, 'pH1': 4.05, 'temp1': 25.183,
                                          'salinity1': 9.0, 'ldev1': 627.961, 'dphi2': 53.009,
                                          'pH2': 10.023, 'temp2': 24.422, 'salinity2': 6.5, 'ldev2': 627.985,
                                          'Aon': 1.656, 'Aoff': 0.068}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['pH', 'dphi', 'signal_intensity', 'ambient_light', 'ldev', 'status'], list(df.columns))
        self.assertEqual(1356, len(df))


class TestWorkbench_1_0_28(unittest.TestCase):
    directory = script_dir + '/testdata/workbench_V1.0.28/'

    def test_load_f1(self):
        file1 = 'Firesting Pro (4 Channels)_(A Ch.1)_pH.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'KK393_pyroscience_Ferm_DX_py_1',
                          'experiment_description': '\n', 'software_version': 'Workbench V1.0.28',
                          'device': 'FireSting pro [A] FSPLUS-4',
                          'device_serial': '', 'uid': '2466C2065AC97E4B', 'firmware': '4.01:008', 'channel': 1,
                          'sensor_code': 'SAG7-319-933',
                          'settings': {'duration': '64 ms', 'intensity': '80%', 'amp': '400x', 'frequency': 3000,
                                       'crc_enable': False, 'write_lock': False,
                                       'auto_flash_duration': True, 'auto_amp': True, 'analyte': 'pH',
                                       'fiber_type': '1 mm', 'temperature': 37.0, 'pressure': 'internal sensor',
                                       'salinity': 9.0},
                          'calibration': {'date_calibration_acid': datetime.datetime(2019, 4, 6, 0, 0),
                                          'date_calibration_base': datetime.datetime(2019, 4, 6, 0, 0),
                                          'date_calibration_offset': datetime.datetime(2019, 5, 6, 0, 0),
                                          'pka': 7.063, 'slope': 1.039, 'dphi_ref': 56.21, 'pka_t': -0.01,
                                          'dyn_t': -0.0, 'bottom_t': -0.0, 'slope_t': 0.0,
                                          'f': 0.04, 'lambda_std': 623.0, 'pka_is1': 1.0, 'pka_is2': 0.3,
                                          'bkgdAmpl': 0.577, 'bkgdDphi': 0.0, 'offset': -0.273,
                                          'dphi1': 24.121, 'pH1': 4.017, 'temp1': 26.082, 'salinity1': 2.0,
                                          'ldev1': 624.64, 'dphi2': 52.283, 'pH2': 10.011,
                                          'temp2': 25.778, 'salinity2': 6.5, 'ldev2': 624.673, 'Aon': 0.0,
                                          'Aoff': 0.0}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['pH', 'dphi', 'signal_intensity', 'ambient_light', 'ldev', 'status'],
                         list(df.columns))
        self.assertEqual(23101, len(df))


class TestWorkbench_1_0_1_808(unittest.TestCase):
    directory = script_dir + '/testdata/workbench_V1.0.1.808/ChannelData/'

    def test_load_f1(self):
        file1 = 'Firesting Pro (4 Channels)_(A Ch.1)_pH.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'testlog',
                          'experiment_description': '\n', 'software_version': 'Workbench V1.0.1.808',
                          'device': 'FireSting pro [A] FSPLUS-4', 'device_serial': '',
                          'uid': '2466C2065AC9A991', 'firmware': '4.02:002', 'channel': 1,
                          'sensor_code': 'SAG7-505-050', 'settings': {'duration': '16 ms', 'intensity': '40%',
                                                                      'amp': '400x', 'frequency': 3000,
                                                                      'crc_enable': False, 'write_lock': False,
                                                                      'auto_flash_duration': True, 'auto_amp': True,
                                                                      'analyte': 'pH', 'fiber_type': '1 mm',
                                                                      'temperature': 'internal sensor',
                                                                      'pressure': 'internal sensor', 'salinity': 7.0},
                          'calibration': {'date_calibration_acid': None, 'date_calibration_base': None,
                                          'date_calibration_offset': None,
                                          'pka': 7.101, 'slope': 1.037, 'dphi_ref': 57.8, 'pka_t': -0.01,
                                          'dyn_t': -0.001, 'bottom_t': -0.001, 'slope_t': 0.0,
                                          'f': 0.04, 'lambda_std': 623.0, 'pka_is1': 2.33, 'pka_is2': 0.25,
                                          'bkgdAmpl': 0.811, 'bkgdDphi': 0.0,
                                          'offset': 0.0, 'dphi1': 16.534, 'pH1': 4.0, 'temp1': 31.0, 'salinity1': 7.5,
                                          'ldev1': 624.912,
                                          'dphi2': 41.81, 'pH2': 11.0, 'temp2': 31.0, 'salinity2': 7.5,
                                          'ldev2': 624.909, 'Aon': 2.212, 'Aoff': 0.42}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['time_s', 'pH', 'dphi', 'signal_intensity', 'ambient_light', 'ldev',
                          'status', 'case_temperature'],
                         list(df.columns))
        self.assertEqual(41, len(df))

    def test_load_f2(self):
        file1 = 'Firesting Pro (4 Channels)_(A Ch.2)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual(
            {'experiment_name': 'testlog', 'experiment_description': '\n', 'software_version': 'Workbench V1.0.1.808',
             'device': 'FireSting pro [A] FSPLUS-4', 'device_serial': '', 'uid': '2466C2065AC9A991',
             'firmware': '4.02:002', 'channel': 2,
             'sensor_code': 'SB7-500-200',
             'settings': {'duration': '16 ms', 'intensity': '15%', 'amp': '400x', 'frequency': 4000,
                          'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True, 'auto_amp': True,
                          'analyte': 'oxygen', 'fiber_type': '1 mm',
                          'temperature': 'external sensor', 'pressure': 'internal sensor', 'salinity': 0.0},
             'calibration': {'date_calibration_high': None,
                             'date_calibration_zero': None, 'dphi100': 20.0, 'dphi0': 50.0, 'f': 0.804, 'm': 0.122,
                             'freq': 4000.0, 'tt': -0.00056,
                             'kt': 0.00969, 'bkgdAmpl': 0.577, 'bkgdDphi': 0.0, 'mt': -0.0, 'pressure': 1013.0,
                             'temp100': 20.0, 'humidity': 0.0,
                             'temp0': 20.0, 'percentO2': 20.95}}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['time_s', 'oxygen_µM', 'oxygen_hPa', 'oxygen_%airsat', 'oxygen_%O2',
                          'dphi', 'signal_intensity', 'ambient_light', 'status', 'sample_temperature', 'pressure'],
                         list(df.columns))
        self.assertEqual(41, len(df))


class TestWorkbench_1_0_2_830(unittest.TestCase):
    directory = script_dir + '/testdata/workbench_V1.0.2.830/'

    def test_load_f1(self):
        file1 = 'Firesting Pro (4 Channels)_(A Ch.1)_pH.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'KK399_PyroSci pH Eval 3rd pH4',
                          'experiment_description': '\n', 'software_version': 'Workbench V1.0.2.830',
                          'device': 'FireSting pro [A] FSPLUS-4',
                          'device_serial': '', 'uid': '2466C2065AC97E4B', 'firmware': '4.02:002', 'channel': 1,
                          'sensor_code': 'SAG7-350-000',
                          'settings': {'duration': '64 ms', 'intensity': '80%', 'amp': '400x', 'frequency': 3000,
                                       'crc_enable': False,
                                       'write_lock': False, 'auto_flash_duration': True, 'auto_amp': True,
                                       'analyte': 'pH', 'fiber_type': '1 mm',
                                       'temperature': 'external sensor', 'pressure': 'internal sensor',
                                       'salinity': 10.0},
                          'calibration': {'date_calibration_acid': datetime.datetime(2019, 11, 28, 0, 0),
                                          'date_calibration_base': datetime.datetime(2019, 11, 28, 0, 0),
                                          'date_calibration_offset': datetime.datetime(2001, 1, 1, 0, 0),
                                          'pka': 7.071, 'slope': 1.037, 'dphi_ref': 57.8, 'pka_t': -0.01,
                                          'dyn_t': -0.001, 'bottom_t': -0.001, 'slope_t': 0.0,
                                          'f': 0.04, 'lambda_std': 623.0, 'pka_is1': 2.33, 'pka_is2': 0.25,
                                          'bkgdAmpl': 0.0, 'bkgdDphi': 0.0,
                                          'offset': 0.0, 'dphi1': 18.891, 'pH1': 4.013, 'temp1': 23.67,
                                          'salinity1': 2.0, 'ldev1': 624.793, 'dphi2': 50.115,
                                          'pH2': 10.029, 'temp2': 23.783, 'salinity2': 6.5, 'ldev2': 624.571,
                                          'Aon': 0.0, 'Aoff': 0.0}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['time_s', 'pH', 'dphi', 'signal_intensity', 'ambient_light', 'ldev', 'status',
                          'sample_temperature'],
                         list(df.columns))
        self.assertEqual(5, len(df))


class TestWorkbench_1_2_0_1289(unittest.TestCase):
    directory = script_dir + '/testdata/workbench_V1.2.0.1289/'

    def test_load_f1(self):
        file1 = 'APHOX-LX_(A Ch.1)_pH.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': '2020-11-04 ApHOx PK8T Precisio',
                          'experiment_description': 'Es werden auf 2 APHOX Logger 2 Kappen mit PK8T Material gegeben. \nDie Kappen wurden für >48h eingelegt in Meerwasser und dann in PHCAL2 und PHCAL10 kalibriert bei RT. \nDaraufhin werden die Logger in thermostatisierte Bechergläser gegeben (ca. 3/4 untergetaucht) und bei 25°C und 15°C pH gemessen mit Referenzmessungen vom Spektrophotometer\nAuf APHOX8 ist die gelbe Kappe (gelbe Kappe kurz vor der Messung angebracht)\nAuf APHOX20 ist die schwarze Kappe (wurde so bereits 48h eingelegt)\n',
                          'software_version': 'Workbench V1.2.0.1289', 'device': 'AquapHOx-LX Nr8 [A] APHOX-LX',
                          'device_serial': '', 'uid': '24967102575BA4F1', 'firmware': '4.03:004',
                          'channel': 1, 'sensor_code': 'FCB7-390-783',
                          'settings': {'duration': '16 ms', 'intensity': '15%', 'amp': '400x', 'frequency': 3000,
                                       'crc_enable': False, 'write_lock': False, 'auto_flash_duration': False,
                                       'auto_amp': True, 'analyte': 'pH', 'fiber_type': '1 mm',
                                       'temperature': 'external sensor', 'pressure': 'internal sensor',
                                       'salinity': 35.0},
                          'calibration': {'date_calibration_acid': datetime.datetime(2020, 11, 5, 0, 0),
                                          'date_calibration_base': datetime.datetime(2020, 11, 5, 0, 0),
                                          'date_calibration_offset': None, 'pka': 8.008788, 'slope': 1.033,
                                          'dphi_ref': 57.8, 'pka_t': -0.0163, 'dyn_t': -0.000521,
                                          'bottom_t': -0.001255, 'slope_t': 0.0, 'f': 0.0325, 'lambda_std': 623.0,
                                          'pka_is1': 0.9697, 'pka_is2': 0.1263,
                                          'bkgdAmpl': 0.343, 'bkgdDphi': 0.0, 'offset': 0.0, 'dphi1': 17.391199,
                                          'pH1': 2.254986, 'temp1': 26.24085,
                                          'salinity1': 2.0, 'ldev1': 623.50354, 'dphi2': 54.445751, 'pH2': 10.003114,
                                          'temp2': 26.606449, 'salinity2': 6.5, 'ldev2': 623.559448,
                                          'Aon': 0.0, 'Aoff': 0.0}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['time_s', 'pH', 'dphi', 'signal_intensity', 'ambient_light', 'ldev',
                          'status', 'sample_temperature'],
                         list(df.columns))
        self.assertEqual(3872, len(df))


class TestWorkbench_1_2_3_1406(unittest.TestCase):
    directory = script_dir + '/testdata/workbench_V1.2.3.1406/'

    def test_load_f1(self):
        file1 = 'APHOX-LX_(A Ch.1)_pH.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'f334 1 und 2',
                          'experiment_description': '1 in pH 7,9\n2 in pH 8,3\n',
                          'software_version': 'Workbench V1.2.3.1406',
                          'device': 'AquapHOx-LX-5 [A] APHOX-LX',
                          'device_serial': '',
                          'uid': '24C53408575BA6B9',
                          'firmware': '4.05:003',
                          'channel': 1,
                          'sensor_code': 'FCD7-392-881',
                          'settings': {'duration': '16 ms',
                                       'intensity': '30%',
                                       'amp': '400x',
                                       'frequency': 3000,
                                       'crc_enable': False,
                                       'write_lock': False,
                                       'auto_flash_duration': False,
                                       'auto_amp': True,
                                       'analyte': 'pH',
                                       'fiber_type': '1 mm',
                                       'temperature': 'external sensor',
                                       'pressure': 'internal sensor',
                                       'salinity': 35.0},
                          'calibration': {'date_calibration_acid': datetime.datetime(2021, 7, 7, 0, 0),
                                          'date_calibration_base': datetime.datetime(2021, 7, 7, 0, 0),
                                          'date_calibration_offset': None, 'pka': 8.009, 'slope': 1.033,
                                          'dphi_ref': 57.8, 'pka_t': -0.0163, 'dyn_t': -0.000521,
                                          'bottom_t': -0.001255, 'slope_t': 0.0, 'f': 0.0325, 'lambda_std': 623.0,
                                          'pka_is1': 0.9697, 'pka_is2': 0.1263, 'bkgdAmpl': 0.0,
                                          'bkgdDphi': 0.0, 'offset': 0.0, 'dphi1': 16.193, 'pH1': 2.246,
                                          'temp1': 27.355, 'salinity1': 2.0, 'ldev1': 623.435,
                                          'dphi2': 55.319653, 'pH2': 11.265946, 'temp2': 27.327301, 'salinity2': 6.0,
                                          'ldev2': 623.555481, 'Aon': 2.362855,
                                          'Aoff': 0.055633}}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['time_s', 'pH', 'dphi', 'signal_intensity', 'ambient_light', 'ldev',
                          'status', 'sample_temperature'], list(df.columns))
        self.assertEqual(71, len(df))


class TestWorkbench_1_4_3_2196(unittest.TestCase):
    directory = script_dir + '/testdata/workbench_V1.4.3.2196/'

    def test_load_f1(self):
        file1 = 'A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'Glycerintest',
                          'experiment_description': 'Test für Kunde\nMacht 1% Glycerin probleme?\n',
                          'software_version': 'Workbench V1.4.3.2196',
                          'device': 'FSP20 [A] FSPRO-4', 'device_serial': '', 'uid': '247AA5035D64A770',
                          'firmware': '4.10:003', 'channel': 1,
                          'sensor_code': 'SA7-500-200',
                          'settings': {'duration': '16 ms', 'intensity': '10%', 'amp': '400x', 'frequency': 4000,
                                       'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True,
                                       'auto_amp': True, 'analyte': 'oxygen',
                                       'fiber_type': '1 mm', 'temperature': 'external sensor',
                                       'pressure': 'internal sensor', 'salinity': 7.5, 'fiber_length_mm': 1000},
                          'calibration': {'date_calibration_high': datetime.datetime(2022, 11, 16, 0, 0),
                                          'date_calibration_zero': datetime.datetime(2022, 11, 16, 0, 0),
                                          'dphi100': 20.741066, 'dphi0': 54.271927, 'f': 0.804, 'm': 0.122,
                                          'freq': 4000.0, 'tt': -0.00056, 'kt': 0.00969,
                                          'bkgdAmpl': 0.584349, 'bkgdDphi': 0.0, 'mt': -0.000303,
                                          'pressure': 962.791016, 'temp100': 23.974867,
                                          'humidity': 35.911999, 'temp0': 22.914398, 'percentO2': 20.95}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['time_s', 'oxygen_%O2', 'dphi', 'signal_intensity', 'ambient_light',
                          'status', 'sample_temperature', 'pressure'], list(df.columns))
        self.assertEqual(1437, len(df))


class TestWorkbench_1_4_7_2305(unittest.TestCase):
    directory = script_dir + '/testdata/workbench_V1.4.7.2305/'

    def test_load_f1(self):
        file1 = 'A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'Startmessung in Sulfit',
                          'experiment_description': 'ch1+2: referenz f404\nch3+4: neues tio2 f440\n',
                          'software_version': 'Workbench V1.4.7.2305', 'device': 'FireSting-PRO [A] FSPRO-4',
                          'device_serial': '',
                          'uid': '24EB9B03596FD090', 'firmware': '4.11:001', 'channel': 1, 'sensor_code': 'SA6-500-200',
                          'settings': {'duration': '8 ms',
                                       'intensity': '10%', 'amp': '200x', 'frequency': 4000, 'crc_enable': False,
                                       'write_lock': False, 'auto_flash_duration': True,
                                       'auto_amp': True, 'analyte': 'oxygen', 'fiber_type': '1 mm', 'temperature': 20.0,
                                       'pressure': 'internal sensor',
                                       'salinity': 7.5, 'fiber_length_mm': 1000},
                          'calibration': {'date_calibration_high': None, 'date_calibration_zero': None,
                                          'dphi100': 20.0, 'dphi0': 50.0, 'f': 0.804, 'm': 0.122, 'freq': 4000.0,
                                          'tt': -0.00056, 'kt': 0.00969,
                                          'bkgdAmpl': 0.584349, 'bkgdDphi': 0.0, 'mt': -0.000303, 'pressure': 1013.0,
                                          'temp100': 20.0,
                                          'humidity': 0.0, 'temp0': 20.0, 'percentO2': 20.95}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['time_s', 'oxygen_%O2', 'dphi', 'signal_intensity', 'ambient_light',
                          'status', 'fixed_temperature', 'pressure'], list(df.columns))
        self.assertEqual(93, len(df))


class TestWorkbench_1_4_8_2380(unittest.TestCase):
    directory = script_dir + '/testdata/workbench_V1.4.8.2380/1/ChannelData/'

    def test_load_f1(self):
        file1 = 'A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'getcomplexlogfiles',
                          'experiment_description': 'ein versuch möglichst komplizierte logfiles \nzu \ngenerieren\num meinen parser zu Verbessern!!\n',
                          'software_version': 'Workbench V1.4.8.2380', 'device': 'FSP39 [A] FSPRO-4',
                          'device_serial': '24110021',
                          'uid': '24EB9B03596FC737', 'firmware': '4.11:001', 'channel': 1, 'sensor_code': 'SB7-530-200',
                          'settings': {'duration': '16 ms', 'intensity': '15%', 'amp': '400x', 'frequency': 4000,
                                       'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True,
                                       'auto_amp': True, 'analyte': 'oxygen',
                                       'fiber_type': '1 mm', 'fiber_length_mm': 1000, 'temperature': 'external sensor',
                                       'pressure': 1013.000000, 'salinity': 7.500000},
                          'calibration': {'bkgdAmpl': 0.584349, 'bkgdDphi': 0.0,
                                          'date_calibration_high': None, 'date_calibration_zero': None,
                                          'dphi0': 53.0, 'dphi100': 20.0, 'f': 0.804, 'freq': 4000.0, 'humidity': 0.0,
                                          'kt': 0.00969,
                                          'm': 0.122, 'mt': -0.000303, 'percentO2': 20.95, 'pressure': 1013.0,
                                          'temp0': 20.0, 'temp100': 20.0,
                                          'tt': -5.6e-04}}, {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['time_s', 'oxygen_%O2', 'dphi', 'signal_intensity', 'ambient_light', 'status',
                          'sample_temperature', 'pressure'], list(df.columns))
        self.assertEqual(50, len(df))

    def test_load_f2(self):
        file1 = 'A_Firesting Pro (4 Channels)_(A Ch.2)_pH.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'calibration': {'R1': 1.6, 'R2': 0.1, 'attenuation_coefficient': 0.0339,
                                          'bkgdAmpl': 0.04411, 'bkgdDphi': 0.0, 'bottom_t': -0.001108,
                                          'dphi_ref': 57.8, 'date_calibration_acid': None,
                                          'date_calibration_base': None,
                                          'date_calibration_offset': None, 'dsf_dye': 0.9047, 'dtf_dye': -0.00567,
                                          'offset': 0.0, 'pH1': 0.0, 'pH2': 14.0, 'pka': 8.03101,
                                          'pka_is1': 0.9697, 'pka_is2': 0.1263, 'pka_t': -0.01628, 'salinity1': 7.5,
                                          'salinity2': 7.5, 'slope': 1.034, 'slope_t': 0.0, 'temp1': 20.0,
                                          'temp2': 20.0, 'top_t': -0.000803}, 'channel': 2,
                          'device': 'FSP39 [A] FSPRO-4',
                          'device_serial': '24110021',
                          'experiment_description': 'ein versuch möglichst komplizierte logfiles \nzu \n'
                                                    'generieren\num meinen parser zu Verbessern!!\n',
                          'experiment_name': 'getcomplexlogfiles', 'firmware': '4.11:001',
                          'sensor_code': 'SIF7-505-050',
                          'settings': {'amp': '400x', 'analyte': 'pH', 'auto_amp': True,
                                       'auto_flash_duration': False, 'crc_enable': False, 'duration': '16 ms',
                                       'fiber_length_mm': 0, 'fiber_type': '1 mm', 'frequency': 3000,
                                       'intensity': '60%', 'pressure': 'internal sensor', 'salinity': 7.500000,
                                       'temperature': 'external sensor', 'write_lock': False},
                          'software_version': 'Workbench V1.4.8.2380', 'uid': '24EB9B03596FC737'},
                         {k: v for k, v in m.items() if k != 'parser_version'})

        self.assertEqual(['time_s', 'pH', 'dphi', 'signal_intensity', 'ambient_light', 'R', 'status',
                          'sample_temperature'], list(df.columns))
        self.assertEqual(2, len(df))

    def test_load_f3(self):
        file1 = 'A_Firesting Pro (4 Channels)_(A Ch.3)_OpticalTemp.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'channel': 3, 'device': 'FSP39 [A] FSPRO-4',
                          'device_serial': '24110021',
                          'experiment_description': 'ein versuch möglichst komplizierte logfiles \n'
                                                    'zu \ngenerieren\num meinen parser zu Verbessern!!\n',
                          'experiment_name': 'getcomplexlogfiles', 'firmware': '4.11:001',
                          'sensor_code': 'DF7-400-500',
                          'software_version': 'Workbench V1.4.8.2380', 'uid': '24EB9B03596FC737',
                          'settings': {'amp': '400x', 'analyte': 'temperature', 'auto_amp': True,
                                       'auto_flash_duration': True, 'crc_enable': False, 'duration': '128 ms',
                                       'fiber_length_mm': 1000, 'fiber_type': '1 mm', 'frequency': 970,
                                       'intensity': '60%', 'pressure': 'internal sensor', 'salinity': 0.000000,
                                       'temperature': 'external sensor', 'write_lock': False},
                          'calibration': {'C': 0.097,
                                          'M': 400.0,
                                          'N': 500.0,
                                          'temp_offset': 0.0,
                                          'bkgdAmpl': 0.584349,
                                          'bkgdDphi': 0.0,
                                          'date_calibration_offset': None},
                          }, {k: v for k, v in m.items() if k != 'parser_version'})

        self.assertEqual(['time_s', 'optical_temperature', 'dphi', 'signal_intensity',
                          'ambient_light', 'status'], list(df.columns))
        self.assertEqual(49, len(df))

    def test_load_f4(self):
        file1 = 'A_Firesting Pro (4 Channels)_(A Ch.4)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'calibration': {
            'bkgdAmpl': 0.584349, 'bkgdDphi': 0.0, 'date_calibration_high': None,
            'date_calibration_zero': None, 'dphi0': 53.0, 'dphi100': 20.0, 'f': 0.804,
            'freq': 4000.0, 'humidity': 0.0, 'kt': 0.00969, 'm': 0.122,
            'mt': -0.000303, 'percentO2': 20.95, 'pressure': 1013.0, 'temp0': 20.0,
            'temp100': 20.0, 'tt': -0.00056},
            'channel': 4,
            'device': 'FSP39 [A] FSPRO-4',
            'device_serial': '24110021',
            'experiment_description': 'ein versuch möglichst komplizierte logfiles \n'
                                      'zu \n'
                                      'generieren\n'
                                      'um meinen parser zu Verbessern!!\n',
            'experiment_name': 'getcomplexlogfiles',
            'firmware': '4.11:001',
            'sensor_code': 'SC7-530-200',
            'settings': {'amp': '400x', 'analyte': 'oxygen', 'auto_amp': True,
                         'auto_flash_duration': True,
                         'crc_enable': False, 'duration': '16 ms', 'fiber_length_mm': 1000,
                         'fiber_type': '1 mm',
                         'frequency': 4000, 'intensity': '20%', 'pressure': 'internal sensor',
                         'salinity': 7.500000, 'temperature': 'Optical Temperature Sensor on Channel 3',
                         'write_lock': False},
            'software_version': 'Workbench V1.4.8.2380',
            'uid': '24EB9B03596FC737'}
            , {k: v for k, v in m.items() if k != 'parser_version'})

        self.assertEqual(['time_s', 'oxygen_%airsat', 'dphi', 'signal_intensity', 'ambient_light', 'status',
                          'optical_temperature', 'pressure'], list(df.columns))
        self.assertEqual(50, len(df))


class TestWorkbench_1_5_0_2415(unittest.TestCase):
    directory = script_dir + '/testdata/workbench_V1.5.0.2415/'

    def test_load_f1(self):
        file1 = 'A_Firesting Pro (4 Channels)_(A Ch.1)_pH.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual(
            {'experiment_name': '100µlmin pH MFTC', 'experiment_description': 'pH 6.5, pH 7, pH7.5, pH8, pH6\n',
             'software_version': 'Workbench V1.5.0.2415', 'device': 'FSP1 [A] FSPRO-4', 'device_serial': '0',
             'uid': '243B1F055AC97A89',
             'firmware': '4.11:001', 'channel': 1, 'sensor_code': 'SGE7-527-445',
             'settings': {'duration': '16 ms', 'intensity': '40%',
                          'amp': '400x', 'frequency': 3000, 'crc_enable': False, 'write_lock': False,
                          'auto_flash_duration': False, 'auto_amp': True,
                          'analyte': 'pH', 'fiber_type': '1 mm', 'temperature': 'external sensor',
                          'pressure': 'internal sensor',
                          'salinity': 7.5, 'fiber_length_mm': 1000},
             'calibration': {'date_calibration_acid': datetime.datetime(2024, 8, 1, 0, 0),
                             'date_calibration_base': datetime.datetime(2024, 8, 1, 0, 0),
                             'date_calibration_offset': None, 'R1': 1.772314, 'pH1': 2.265742, 'temp1': 24.978352,
                             'salinity1': 2.0, 'R2': 0.091797,
                             'pH2': 11.205455, 'temp2': 24.6374, 'salinity2': 6.0, 'offset': 0.0, 'dphi_ref': 57.8,
                             'attenuation_coefficient': 0.03593,
                             'bkgdAmpl': 0.584349, 'bkgdDphi': 0.0, 'dsf_dye': 0.9904, 'dtf_dye': -0.006321,
                             'pka': 7.055051, 'slope': 1.048,
                             'bottom_t': -0.007805, 'top_t': -0.00154, 'slope_t': 0.0, 'pka_t': -0.008985,
                             'pka_is1': 2.33, 'pka_is2': 0.25}},
            {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['time_s', 'pH', 'dphi', 'signal_intensity', 'ambient_light', 'R',
                          'status', 'sample_temperature'], list(df.columns))
        self.assertEqual(564, len(df))

    def test_load_f3(self):
        file1 = 'A_Firesting Pro (4 Channels)_(A Ch.3)_OpticalTemp.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual(
            {'experiment_name': '100µlmin pH MFTC', 'experiment_description': 'pH 6.5, pH 7, pH7.5, pH8, pH6\n',
             'software_version': 'Workbench V1.5.0.2415', 'device': 'FSP1 [A] FSPRO-4', 'device_serial': '0',
             'uid': '243B1F055AC97A89',
             'firmware': '4.11:001', 'channel': 3, 'sensor_code': 'DF7-273-522',
             'settings': {'duration': '128 ms', 'intensity': '60%',
                          'amp': '400x', 'frequency': 970, 'crc_enable': False, 'write_lock': False,
                          'auto_flash_duration': True, 'auto_amp': True,
                          'analyte': 'temperature', 'fiber_type': '1 mm', 'temperature': 'external sensor',
                          'pressure': 'internal sensor', 'salinity': 0.0,
                          'fiber_length_mm': 1000},
             'calibration': {'date_calibration_offset': datetime.datetime(2024, 8, 1, 0, 0),
                             'M': 273.0, 'N': 522.0, 'C': 0.097, 'temp_offset': 0.583533, 'bkgdAmpl': 0.584,
                             'bkgdDphi': 0.0}},
            {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['time_s', 'optical_temperature', 'dphi', 'signal_intensity', 'ambient_light', 'status'],
                         list(df.columns))
        self.assertEqual(565, len(df))


class TestWorkbench_1_5_3_2466(unittest.TestCase):
    directory = script_dir + '/testdata/workbench_V1.5.3.2466/'

    def test_load_f1(self):
        file1 = '2024-09-03_170952_air_percentO2/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'air_percentO2', 'experiment_description': '\n',
                          'software_version': 'Workbench V1.5.3.2466',
                          'device': 'FSP23 [A] FSPRO-4', 'device_serial': '20460041', 'uid': '249BC3015AC9AE27',
                          'firmware': '4.11:001',
                          'channel': 1, 'sensor_code': 'SA6-530-210',
                          'settings': {'duration': '16 ms', 'intensity': '10%', 'amp': '200x',
                                       'frequency': 4000, 'crc_enable': False, 'write_lock': False,
                                       'auto_flash_duration': True, 'auto_amp': True,
                                       'analyte': 'oxygen', 'fiber_type': '1 mm', 'temperature': 'external sensor',
                                       'pressure': 'internal sensor', 'salinity': 7.5,
                                       'fiber_length_mm': 1000},
                          'calibration': {'date_calibration_high': datetime.datetime(2024, 9, 3, 0, 0),
                                          'date_calibration_zero': None, 'dphi100': 21.024534, 'dphi0': 53.0,
                                          'f': 0.804, 'm': 0.122, 'freq': 4000.0, 'tt': -0.00056,
                                          'kt': 0.00969, 'bkgdAmpl': 0.584349, 'bkgdDphi': 0.0, 'mt': -0.000303,
                                          'pressure': 974.02301, 'temp100': 25.5126,
                                          'humidity': 34.004002, 'temp0': 20.0, 'percentO2': 20.95}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['time_s', 'oxygen_%O2', 'dphi', 'signal_intensity', 'ambient_light', 'status',
                          'sample_temperature', 'pressure'], list(df.columns))
        self.assertEqual(8, len(df))
        self.assertDictEqual({'time_s': 1.031, 'oxygen_%O2': 20.712, 'dphi': 21.024, 'signal_intensity': 321.0,
                              'ambient_light': 0.0, 'status': 0.0, 'sample_temperature': 25.526, 'pressure': 974.0},
                             {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})

    def test_load_f2(self):
        file1 = '2024-09-03_171034_air_hpa/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual(
            {'experiment_name': 'air_hpa', 'experiment_description': '\n', 'software_version': 'Workbench V1.5.3.2466',
             'device': 'FSP23 [A] FSPRO-4', 'device_serial': '20460041', 'uid': '249BC3015AC9AE27',
             'firmware': '4.11:001', 'channel': 1,
             'sensor_code': 'SA6-530-210',
             'settings': {'duration': '16 ms', 'intensity': '10%', 'amp': '200x', 'frequency': 4000,
                          'crc_enable': False, 'write_lock': False,
                          'auto_flash_duration': True, 'auto_amp': True, 'analyte': 'oxygen', 'fiber_type': '1 mm',
                          'temperature': 20.0, 'pressure': 'internal sensor',
                          'salinity': 7.5, 'fiber_length_mm': 1000},
             'calibration': {'date_calibration_high': datetime.datetime(2024, 9, 3, 0, 0),
                             'date_calibration_zero': None, 'dphi100': 21.024534, 'dphi0': 53.0, 'f': 0.804, 'm': 0.122,
                             'freq': 4000.0, 'tt': -0.00056,
                             'kt': 0.00969, 'bkgdAmpl': 0.584349, 'bkgdDphi': 0.0, 'mt': -0.000303,
                             'pressure': 974.02301, 'temp100': 25.5126, 'humidity': 34.004002, 'temp0': 20.0,
                             'percentO2': 20.95}},
            {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['time_s', 'oxygen_hPa', 'dphi', 'signal_intensity', 'ambient_light', 'status',
                          'fixed_temperature', 'pressure'], list(df.columns))
        self.assertEqual(7, len(df))
        self.assertDictEqual(
            {'time_s': 1.606, 'oxygen_hPa': 212.712, 'dphi': 21.034, 'signal_intensity': 321.0, 'ambient_light': 0.0,
             'status': 0.0, 'fixed_temperature': 20.0, 'pressure': 974.0},
            {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})

    def test_load_f3(self):
        self.maxDiff = None
        file1 = '2024-09-03_171110_air_torr/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'air_torr', 'experiment_description': '\n',
                          'software_version': 'Workbench V1.5.3.2466', 'device': 'FSP23 [A] FSPRO-4',
                          'device_serial': '20460041', 'uid': '249BC3015AC9AE27', 'firmware': '4.11:001', 'channel': 1,
                          'sensor_code': 'SA6-530-210',
                          'settings': {'duration': '16 ms', 'intensity': '10%', 'amp': '200x', 'frequency': 4000,
                                       'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True,
                                       'auto_amp': True, 'analyte': 'oxygen', 'fiber_type': '1 mm',
                                       'temperature': 'external sensor', 'pressure': 'internal sensor', 'salinity': 7.5,
                                       'fiber_length_mm': 1000},
                          'calibration': {'date_calibration_high': datetime.datetime(2024, 9, 3, 0, 0),
                                          'date_calibration_zero': None, 'dphi100': 21.024534, 'dphi0': 53.0,
                                          'f': 0.804, 'm': 0.122, 'freq': 4000.0, 'tt': -0.00056, 'kt': 0.00969,
                                          'bkgdAmpl': 0.584349, 'bkgdDphi': 0.0, 'mt': -0.000303, 'pressure': 974.02301,
                                          'temp100': 25.5126, 'humidity': 34.004002, 'temp0': 20.0,
                                          'percentO2': 20.95}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(
            ['time_s', 'oxygen_torr', 'dphi', 'signal_intensity', 'ambient_light', 'status', 'sample_temperature',
             'pressure'], list(df.columns))
        self.assertEqual(8, len(df))
        self.assertDictEqual(
            {'time_s': 1.098, 'oxygen_torr': 151.015, 'dphi': 21.044, 'signal_intensity': 321.0, 'ambient_light': 0.0,
             'status': 0.0, 'sample_temperature': 25.542, 'pressure': 974.0},
            {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})

    def test_load_f4(self):
        file1 = '2024-09-03_171217_water_airsat/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'water_airsat', 'experiment_description': '\n',
                          'software_version': 'Workbench V1.5.3.2466', 'device': 'FSP23 [A] FSPRO-4',
                          'device_serial': '20460041', 'uid': '249BC3015AC9AE27', 'firmware': '4.11:001', 'channel': 1,
                          'sensor_code': 'SA6-530-210',
                          'settings': {'duration': '16 ms', 'intensity': '10%', 'amp': '200x', 'frequency': 4000,
                                       'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True,
                                       'auto_amp': True, 'analyte': 'oxygen', 'fiber_type': '1 mm', 'temperature': 20.0,
                                       'pressure': 1013.0, 'salinity': 7.5, 'fiber_length_mm': 1000},
                          'calibration': {'date_calibration_high': datetime.datetime(2024, 9, 3, 0, 0),
                                          'date_calibration_zero': None, 'dphi100': 21.061666, 'dphi0': 53.0,
                                          'f': 0.804, 'm': 0.122, 'freq': 4000.0, 'tt': -0.00056, 'kt': 0.00969,
                                          'bkgdAmpl': 0.584349, 'bkgdDphi': 0.0, 'mt': -0.000303,
                                          'pressure': 973.979004, 'temp100': 20.0, 'humidity': 33.727001, 'temp0': 20.0,
                                          'percentO2': 20.95}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(
            ['time_s', 'oxygen_%airsat', 'dphi', 'signal_intensity', 'ambient_light', 'status', 'fixed_temperature',
             'pressure']
            , list(df.columns))
        self.assertEqual(6, len(df))
        self.assertDictEqual(
            {'time_s': 1.148, 'oxygen_%airsat': 97.665, 'dphi': 21.057, 'signal_intensity': 321.0, 'ambient_light': 0.0,
             'status': 0.0, 'fixed_temperature': 20.0, 'pressure': 1013.0},
            {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})

    def test_load_f5(self):
        file1 = '2024-09-03_171810_water_mLL/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'water_mLL', 'experiment_description': '\n',
                          'software_version': 'Workbench V1.5.3.2466', 'device': 'FSP23 [A] FSPRO-4',
                          'device_serial': '20460041', 'uid': '249BC3015AC9AE27', 'firmware': '4.11:001',
                          'channel': 1, 'sensor_code': 'SA6-530-210',
                          'settings': {'duration': '16 ms', 'intensity': '10%', 'amp': '200x', 'frequency': 4000,
                                       'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True,
                                       'auto_amp': True, 'analyte': 'oxygen', 'fiber_type': '1 mm',
                                       'temperature': 'external sensor', 'pressure': 1013.0, 'salinity': 4.0,
                                       'fiber_length_mm': 1000},
                          'calibration': {'date_calibration_high': datetime.datetime(2024, 9, 3, 0, 0),
                                          'date_calibration_zero': None, 'dphi100': 21.061666, 'dphi0': 53.0,
                                          'f': 0.804, 'm': 0.122, 'freq': 4000.0, 'tt': -0.00056, 'kt': 0.00969,
                                          'bkgdAmpl': 0.584349, 'bkgdDphi': 0.0, 'mt': -0.000303,
                                          'pressure': 973.979004, 'temp100': 20.0, 'humidity': 33.727001,
                                          'temp0': 20.0, 'percentO2': 20.95}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(
            ['time_s', 'oxygen_mL/L', 'dphi', 'signal_intensity', 'ambient_light', 'status', 'sample_temperature',
             'pressure'], list(df.columns))
        self.assertEqual(7, len(df))
        self.assertDictEqual(
            {'time_s': 1.274, 'oxygen_mL/L': 5.206, 'dphi': 21.082, 'signal_intensity': 321.0, 'ambient_light': 0.0,
             'status': 0.0, 'sample_temperature': 25.575, 'pressure': 1013.0},
            {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})

    def test_load_f6(self):
        file1 = '2024-09-03_171911_water_uM/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'water_uM', 'experiment_description': '\n',
                          'software_version': 'Workbench V1.5.3.2466', 'device': 'FSP23 [A] FSPRO-4',
                          'device_serial': '20460041', 'uid': '249BC3015AC9AE27', 'firmware': '4.11:001',
                          'channel': 1, 'sensor_code': 'SA6-530-210',
                          'settings': {'duration': '16 ms', 'intensity': '10%', 'amp': '200x', 'frequency': 4000,
                                       'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True,
                                       'auto_amp': True, 'analyte': 'oxygen', 'fiber_type': '1 mm',
                                       'temperature': 'external sensor', 'pressure': 1013.0, 'salinity': 10.0,
                                       'fiber_length_mm': 1000},
                          'calibration': {'date_calibration_high': datetime.datetime(2024, 9, 3, 0, 0),
                                          'date_calibration_zero': None, 'dphi100': 21.061666, 'dphi0': 53.0,
                                          'f': 0.804, 'm': 0.122, 'freq': 4000.0, 'tt': -0.00056, 'kt': 0.00969,
                                          'bkgdAmpl': 0.584349, 'bkgdDphi': 0.0, 'mt': -0.000303,
                                          'pressure': 973.979004, 'temp100': 20.0, 'humidity': 33.727001,
                                          'temp0': 20.0, 'percentO2': 20.95}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['time_s', 'oxygen_µM', 'dphi', 'signal_intensity', 'ambient_light', 'status',
                          'sample_temperature', 'pressure'], list(df.columns))
        self.assertEqual(26, len(df))
        self.assertDictEqual(
            {'time_s': 1.327, 'oxygen_µM': 224.348, 'dphi': 21.088, 'signal_intensity': 321.0,
             'ambient_light': 1.0, 'status': 0.0, 'sample_temperature': 25.585, 'pressure': 1013.0},
            {k: np.nan if np.isnan(v) else v for k, v in df.iloc[1].to_dict().items()})

    def test_load_f7(self):
        file1 = '2024-09-03_172041_water_mgL/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'water_mgL', 'experiment_description': '\n',
                          'software_version': 'Workbench V1.5.3.2466', 'device': 'FSP23 [A] FSPRO-4',
                          'device_serial': '20460041', 'uid': '249BC3015AC9AE27', 'firmware': '4.11:001',
                          'channel': 1, 'sensor_code': 'SA6-530-210',
                          'settings': {'duration': '16 ms', 'intensity': '10%', 'amp': '200x', 'frequency': 4000,
                                       'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True,
                                       'auto_amp': True, 'analyte': 'oxygen', 'fiber_type': '1 mm',
                                       'temperature': 'external sensor', 'pressure': 1013.0, 'salinity': 10.0,
                                       'fiber_length_mm': 1000},
                          'calibration': {'date_calibration_high': datetime.datetime(2024, 9, 3, 0, 0),
                                          'date_calibration_zero': None, 'dphi100': 21.061666, 'dphi0': 53.0,
                                          'f': 0.804, 'm': 0.122, 'freq': 4000.0, 'tt': -0.00056, 'kt': 0.00969,
                                          'bkgdAmpl': 0.584349, 'bkgdDphi': 0.0, 'mt': -0.000303,
                                          'pressure': 973.979004, 'temp100': 20.0, 'humidity': 33.727001,
                                          'temp0': 20.0, 'percentO2': 20.95}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(
            ['time_s', 'oxygen_mg/L', 'dphi', 'signal_intensity', 'ambient_light', 'status', 'sample_temperature',
             'pressure'], list(df.columns))
        self.assertEqual(8, len(df))
        self.assertDictEqual(
            {'time_s': 1.309, 'oxygen_mg/L': 7.175, 'dphi': 21.094, 'signal_intensity': 321.0, 'ambient_light': 0.0,
             'status': 0.0, 'sample_temperature': 25.587, 'pressure': 1013.0},
            {k: np.nan if np.isnan(v) else v for k, v in
             df.iloc[1].to_dict().items()})

    def test_load_f8(self):
        file1 = '2024-09-03_172113_water_ugL/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'water_ugL', 'experiment_description': '\n',
                          'software_version': 'Workbench V1.5.3.2466', 'device': 'FSP23 [A] FSPRO-4',
                          'device_serial': '20460041', 'uid': '249BC3015AC9AE27', 'firmware': '4.11:001',
                          'channel': 1, 'sensor_code': 'SA6-530-210',
                          'settings': {'duration': '16 ms', 'intensity': '10%', 'amp': '200x', 'frequency': 4000,
                                       'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True,
                                       'auto_amp': True, 'analyte': 'oxygen', 'fiber_type': '1 mm',
                                       'temperature': 'external sensor', 'pressure': 1013.0, 'salinity': 10.0,
                                       'fiber_length_mm': 1000},
                          'calibration': {'date_calibration_high': datetime.datetime(2024, 9, 3, 0, 0),
                                          'date_calibration_zero': None, 'dphi100': 21.061666, 'dphi0': 53.0,
                                          'f': 0.804, 'm': 0.122, 'freq': 4000.0, 'tt': -0.00056, 'kt': 0.00969,
                                          'bkgdAmpl': 0.584349, 'bkgdDphi': 0.0, 'mt': -0.000303,
                                          'pressure': 973.979004, 'temp100': 20.0, 'humidity': 33.727001,
                                          'temp0': 20.0, 'percentO2': 20.95}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(
            ['time_s', 'oxygen_µg/L', 'dphi', 'signal_intensity', 'ambient_light', 'status', 'sample_temperature',
             'pressure'], list(df.columns))
        self.assertEqual(10, len(df))
        self.assertDictEqual({'time_s': 1.94, 'oxygen_µg/L': 7181.952, 'dphi': 21.081, 'signal_intensity': 321.0,
                              'ambient_light': 0.0, 'status': 0.0, 'sample_temperature': 25.594,
                              'pressure': 1013.0}, {k: np.nan if np.isnan(v) else v for k, v in
                                                    df.iloc[1].to_dict().items()})

    def test_load_f9(self):
        file1 = '2024-09-03_172218_water_airsat2/ChannelData/A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt'
        df, m = read_workbench(self.directory + file1)
        self.assertEqual({'experiment_name': 'water_airsat2', 'experiment_description': '\n',
                          'software_version': 'Workbench V1.5.3.2466', 'device': 'FSP23 [A] FSPRO-4',
                          'device_serial': '20460041', 'uid': '249BC3015AC9AE27', 'firmware': '4.11:001',
                          'channel': 1, 'sensor_code': 'SA6-530-210',
                          'settings': {'duration': '16 ms', 'intensity': '10%', 'amp': '200x', 'frequency': 4000,
                                       'crc_enable': False, 'write_lock': False, 'auto_flash_duration': True,
                                       'auto_amp': True, 'analyte': 'oxygen', 'fiber_type': '1 mm',
                                       'temperature': 'external sensor', 'pressure': 'internal sensor',
                                       'salinity': 10.0, 'fiber_length_mm': 1000},
                          'calibration': {'date_calibration_high': datetime.datetime(2024, 9, 3, 0, 0),
                                          'date_calibration_zero': None, 'dphi100': 21.061666, 'dphi0': 53.0,
                                          'f': 0.804, 'm': 0.122, 'freq': 4000.0, 'tt': -0.00056, 'kt': 0.00969,
                                          'bkgdAmpl': 0.584349, 'bkgdDphi': 0.0, 'mt': -0.000303,
                                          'pressure': 973.979004, 'temp100': 20.0, 'humidity': 33.727001,
                                          'temp0': 20.0, 'percentO2': 20.95}},
                         {k: v for k, v in m.items() if k != 'parser_version'})
        self.assertEqual(['time_s', 'oxygen_%airsat', 'dphi', 'signal_intensity', 'ambient_light', 'status',
                          'sample_temperature', 'pressure'], list(df.columns))
        self.assertEqual(13, len(df))
        self.assertDictEqual({'time_s': 1.28, 'oxygen_%airsat': 96.942, 'dphi': 21.091, 'signal_intensity': 321.0,
                              'ambient_light': 0.0, 'status': 0.0, 'sample_temperature': 25.592, 'pressure': 974.0},
                             {k: np.nan if np.isnan(v) else v for k, v in
                              df.iloc[1].to_dict().items()})


if __name__ == '__main__':
    unittest.main()
