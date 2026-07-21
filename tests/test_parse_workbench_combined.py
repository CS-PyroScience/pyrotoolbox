import os
import glob
import unittest

import pandas as pd

from pyrotoolbox.parsers import read_combined_workbench, read_workbench, parse

script_dir = os.path.dirname(__file__)


def _find_channel_file(channel_dir, channel_id):
    """Return the per-channel logfile matching a channel id like "A Ch.1" or "A T1"."""
    matches = glob.glob(os.path.join(channel_dir, f"*({channel_id})_*.txt"))
    if len(matches) != 1:
        raise AssertionError(f"expected exactly one per-channel file for {channel_id!r}, found {matches}")
    return matches[0]


class _CombinedParityMixin:
    """Shared assertions comparing a combined file against the individual per-channel logfiles.

    Subclasses set ``combined`` (path to the combined logfile) and ``channel_dir`` (the
    "ChannelData"/"MeasurementData" folder). ``head_rows`` limits parity to the first N rows of the
    per-channel file (needed when the per-channel files are longer than the combined file).
    """

    combined = None
    channel_dir = None
    head_rows = None

    def assert_channel_parity(self, result, channel_id):
        df_c, m_c = result[channel_id]
        df_s, m_s = read_workbench(_find_channel_file(self.channel_dir, channel_id))
        if self.head_rows is not None:
            df_s = df_s.head(self.head_rows)
        # the combined reader adds a "comment" column that the per-channel file does not have
        pd.testing.assert_frame_equal(df_c.drop(columns="comment"), df_s)
        self.assertEqual(m_c, m_s)

    def test_all_channels_parity(self):
        result = read_combined_workbench(self.combined)
        for channel_id in result:
            with self.subTest(channel=channel_id):
                self.assert_channel_parity(result, channel_id)


class TestCombinedWorkbench_1_0_1_808(_CombinedParityMixin, unittest.TestCase):
    directory = script_dir + "/testdata/workbench_V1.0.1.808/"
    combined = directory + "2020-08-18_090215_testlog.txt"
    channel_dir = directory + "ChannelData/"

    def test_keys(self):
        result = read_combined_workbench(self.combined)
        self.assertEqual(["A Ch.1", "A Ch.2", "A Ch.3", "A Ch.4", "A T1"], list(result))

    def test_row_count(self):
        result = read_combined_workbench(self.combined)
        for channel_id in result:
            self.assertEqual(41, len(result[channel_id][0]))

    def test_no_comments(self):
        result = read_combined_workbench(self.combined)
        df = result["A Ch.1"][0]
        self.assertIn("comment", df.columns)
        self.assertTrue(df["comment"].isna().all())


class TestCombinedWorkbench_1_4_8_2380(_CombinedParityMixin, unittest.TestCase):
    directory = script_dir + "/testdata/workbench_V1.4.8.2380/1/"
    combined = directory + "2024-07-01_133831_getcomplexlogfiles.txt"
    channel_dir = directory + "ChannelData/"

    def test_keys(self):
        result = read_combined_workbench(self.combined)
        self.assertEqual(["A Ch.1", "A Ch.2", "A Ch.3", "A Ch.4", "A T1"], list(result))

    def test_row_counts(self):
        result = read_combined_workbench(self.combined)
        # each channel logs at its own interval - the sparse pH channel (Ch.2) has only 2 rows
        self.assertEqual([50, 2, 49, 50, 48], [len(result[c][0]) for c in result])

    def test_sparse_ph_channel_sentinels(self):
        result = read_combined_workbench(self.combined)
        df = result["A Ch.2"][0]
        self.assertEqual(2, len(df))
        # the ">9.5" over-range sentinels are parsed to NaN
        self.assertTrue(df["pH"].isna().all())

    def test_full_metadata_ph_channel(self):
        result = read_combined_workbench(self.combined)
        df, m = result["A Ch.2"]
        self.assertEqual(
            {
                "calibration": {
                    "R1": 1.6,
                    "R2": 0.1,
                    "attenuation_coefficient": 0.0339,
                    "bkgdAmpl": 0.04411,
                    "bkgdDphi": 0.0,
                    "bottom_t": -0.001108,
                    "dphi_ref": 57.8,
                    "date_calibration_acid": None,
                    "date_calibration_base": None,
                    "date_calibration_offset": None,
                    "dsf_dye": 0.9047,
                    "dtf_dye": -0.00567,
                    "offset": 0.0,
                    "pH1": 0.0,
                    "pH2": 14.0,
                    "pka": 8.03101,
                    "pka_is1": 0.9697,
                    "pka_is2": 0.1263,
                    "pka_t": -0.01628,
                    "salinity1": 7.5,
                    "salinity2": 7.5,
                    "slope": 1.034,
                    "slope_t": 0.0,
                    "temp1": 20.0,
                    "temp2": 20.0,
                    "top_t": -0.000803,
                },
                "channel": 2,
                "device": "FSP39 [A] FSPRO-4",
                "device_serial": "24110021",
                "experiment_description": "ein versuch möglichst komplizierte logfiles \nzu \n"
                "generieren\num meinen parser zu Verbessern!!\n",
                "experiment_name": "getcomplexlogfiles",
                "firmware": "4.11:001",
                "sensor_code": "SIF7-505-050",
                "settings": {
                    "amp": "400x",
                    "analyte": "pH",
                    "auto_amp": True,
                    "auto_flash_duration": False,
                    "crc_enable": False,
                    "duration": "16 ms",
                    "fiber_length_mm": 0,
                    "fiber_type": "1 mm",
                    "frequency": 3000,
                    "intensity": "60%",
                    "pressure": "internal sensor",
                    "salinity": 7.500000,
                    "temperature": "external sensor",
                    "write_lock": False,
                },
                "software_version": "Workbench V1.4.8.2380",
                "uid": "24EB9B03596FC737",
            },
            {k: v for k, v in m.items() if k != "parser_version"},
        )


class TestCombinedWorkbench_1_5_3_2466_single(_CombinedParityMixin, unittest.TestCase):
    directory = script_dir + "/testdata/workbench_V1.5.3.2466/2024-09-03_170952_air_percentO2/"
    combined = directory + "2024-09-03_170952_air_percentO2.txt"
    channel_dir = directory + "ChannelData/"

    def test_single_channel(self):
        result = read_combined_workbench(self.combined)
        self.assertEqual(["A Ch.1"], list(result))
        # padding rows are dropped - the measurement itself is only 8 rows
        self.assertEqual(8, len(result["A Ch.1"][0]))


class TestCombinedWorkbench_1_5_3_2466_three_devices(_CombinedParityMixin, unittest.TestCase):
    directory = script_dir + "/testdata/workbench_V1.5.3.2466/2024-12-11 Messung mit Good Puffern/"
    combined = directory + "2024-12-11_083104.txt"
    channel_dir = directory + "ChannelData/"
    # the per-channel files here are much longer than the combined file - compare only the overlap
    head_rows = 4850

    def test_keys_order(self):
        result = read_combined_workbench(self.combined)
        expected = [f"{d} Ch.{n}" for d in "ABC" for n in range(1, 5)]
        # each device also has a PT100 channel between its groups
        self.assertEqual(15, len(result))
        for cid in expected:
            self.assertIn(cid, result)

    def test_all_channels_parity(self):
        # only spot-check a few channels here - the per-channel files are hundreds of MB
        result = read_combined_workbench(self.combined)
        for channel_id in ["A Ch.1", "B T1", "C Ch.4"]:
            with self.subTest(channel=channel_id):
                self.assert_channel_parity(result, channel_id)

    def test_no_experiment_section(self):
        result = read_combined_workbench(self.combined)
        self.assertNotIn("experiment_name", result["A Ch.1"][1])


class TestCombinedWorkbench_1_5_4_2482(_CombinedParityMixin, unittest.TestCase):
    directory = script_dir + "/testdata/workbench_V1.5.4.2482/2025-03-24_154458_Test_WB1452482/"
    combined = directory + "2025-03-24_154458_Test_WB1452482.txt"
    channel_dir = directory + "MeasurementData/"

    def test_keys(self):
        result = read_combined_workbench(self.combined)
        self.assertEqual(
            ["A Ch.1", "A Ch.2", "A Ch.3", "A Ch.4", "A T1", "B Ch.1", "B T1", "C Ch.1", "C T1", "D Ch.1"],
            list(result),
        )

    def test_fixed_temperature_channel(self):
        # the Pico-O2 (device D) uses a fixed temperature compensation
        result = read_combined_workbench(self.combined)
        df = result["D Ch.1"][0]
        self.assertIn("fixed_temperature", df.columns)
        self.assertEqual(24.0, df["fixed_temperature"].iloc[0])

    def test_comments(self):
        result = read_combined_workbench(self.combined)
        expected = [
            "ist das anstrengend",
            "wenn wir glucose hinbekommen, dauert das kalibrieren noch länger",
        ]
        # the same comments are attached as a "comment" column to every channel of the file
        for cid in ["A Ch.1", "D Ch.1"]:
            df = result[cid][0]
            self.assertIn("comment", df.columns)
            self.assertEqual(expected, df["comment"].dropna().tolist())


class TestCombinedDispatch(unittest.TestCase):
    testdata = script_dir + "/testdata/"
    combined = testdata + "workbench_V1.5.4.2482/2025-03-24_154458_Test_WB1452482/2025-03-24_154458_Test_WB1452482.txt"
    channel_file = (
        testdata + "workbench_V1.5.4.2482/2025-03-24_154458_Test_WB1452482/MeasurementData/"
        "A_Firesting Pro (4 Channels)_(A Ch.1)_Oxygen.txt"
    )
    fireplate_combined = (
        testdata + "workbench_V1.5.4.2482/2025-03-25_092456_WB1542482_FP96_O2/2025-03-25_092456_WB1542482_FP96_O2.txt"
    )
    fireplate_group = (
        testdata + "workbench_V1.5.4.2482/2025-03-25_092456_WB1542482_FP96_O2/MeasurementData/"
        "A_FirePlate-O2_(A Gr.1)_Oxygen.txt"
    )

    def test_parse_combined_returns_dict(self):
        result = parse(self.combined)
        self.assertIsInstance(result, dict)
        self.assertEqual(10, len(result))

    def test_parse_single_channel_returns_tuple(self):
        result = parse(self.channel_file)
        self.assertIsInstance(result, tuple)
        self.assertEqual(2, len(result))

    def test_read_workbench_rejects_combined(self):
        with self.assertRaises(ValueError):
            read_workbench(self.combined)

    def test_read_combined_rejects_single_channel(self):
        with self.assertRaises(ValueError):
            read_combined_workbench(self.channel_file)

    def test_read_combined_rejects_fireplate(self):
        with self.assertRaises(ValueError):
            read_combined_workbench(self.fireplate_combined)

    def test_parse_rejects_fireplate_combined(self):
        with self.assertRaises(ValueError):
            parse(self.fireplate_combined)

    def test_parse_fireplate_group_still_works(self):
        # a per-group FirePlate file must still parse as before (single wide DataFrame)
        df, m = parse(self.fireplate_group)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("group", m)


if __name__ == "__main__":
    unittest.main()
