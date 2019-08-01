# import required libraries
import unittest  # unittests themselves
import pandas as pd   # pandas for dataframe
import importlib  # update loaded classes implicitely
import sleep_parameters
importlib.reload(sleep_parameters)   # reload class
import math

# Definition of testvalues
hypnogram_case_a = pd.DataFrame({'AASM': ['L', 'L', 'W', 'A', 'W', 'N1', 'W', 'N3', 'L', 'L', 'L']})
hypnogram_case_b = pd.DataFrame({'AASM': ['W', 'A', 'W', 'N1', 'W', 'N3']})


# lights_off = 2 (3rd epoch)
    # lights_on = 8 (9th epoch)
    # sleep_onset_epoch = 5 (6th epoch)
    # sleep_onset_latency = 1.5 min
    # final_awakening_epoch = 8 (9th epoch)
    # sleep_period_time = 1.5 min
    # total_sleep_time = 1 min
    # wake_after_sleep_onset = 0.5 min
    # sleep_efficiency = 2/6*100


# Initialization of the testcase, the class to be tested is here in self.results_case_a
class SleepParametersTestCase(unittest.TestCase):
    """Tests for `sn_sleep_parameters_class.py`."""
    def setUp(self):
        self.results_case_a = sleep_parameters.SleepAnalysis(hypnogram_case_a)
        self.results_case_b = sleep_parameters.SleepAnalysis(hypnogram_case_b)

# Here the actual tests begin
class TestInit(SleepParametersTestCase):

    def test_if_lights_off_is_two(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.lights.off, 2)

    def test_if_lights_on_is_seven(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.lights.on, 8)

    def test_if_total_recording_time_is_three(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.total_recording_time, 3)

    def test_if_sleep_onset_epoch_is_five(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.sleep_epochs.sleep_onset, 5)

    def test_if_final_awakening_epoch_is_eight(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.sleep_epochs.final_awakening, 8)

    def test_if_sleep_onset_latency_is_onehalfminutes(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.sleep_onset_latency, 1.5)

    def test_if_sleep_period_time_is_onehalfminutes(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.sleep_period_time, 1.5)

    def test_if_total_sleep_time_is_oneminute(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.total_sleep_time, 1)

    def test_if_wake_after_sleep_onset_is_halfminute(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.wake_after_sleep_onset, 0.5)

    def test_if_sleep_efficiency_is_forty(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.sleep_efficiency, 2/6*100)

    def test_if_sleep_R_is_zero(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.sleep_stage_epochs.R, 0)

    def test_if_sleep_N1_is_one(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.sleep_stage_epochs.N1, 1)

    def test_if_sleep_N2_is_zero(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.sleep_stage_epochs.N2, 0)

    def test_if_sleep_N3_is_one(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.sleep_stage_epochs.N3, 1)

    def test_if_sleep_N3_is_halfminute(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.sleep_time_per_stage.N3, 0.5)

    def test_if_sleep_N3_is_50(self):
        """is the total recording time 3 minutes?"""
        self.assertEqual(self.results_case_a.relative_sleep_time_per_stage.N3, 50)

    def test_if_R_onset_latency_is_nan(self):
        """is the total recording time 3 minutes?"""
        self.assertTrue(math.isnan(self.results_case_a.onset_latency.R))

# Edge Case b: lights off and on are zero
    def test_if_lights_off_is_zero(self):
        """is lights_off zero (immediate start of the recording)?"""
        print(self.results_case_b.lights.off)
        self.assertEqual(self.results_case_b.lights.off, 0)


    def test_if_lights_on_is_six(self):
        """Are there 6 epochs before lights on?"""
        self.assertEqual(self.results_case_b.lights.on, 6)


if __name__ == '__main__':
    unittest.main()