import unittest
from condor.condor_log import CondorLog
from condor.condor_states import CondorStates

__author__ = 'med-pvo'


class TestCondorLog(unittest.TestCase):
    def setUp(self):
        log_dir = "TestData"
        self.running_log = CondorLog("condor_log_running", log_dir)
        self.error_log = CondorLog("condor_log_error", log_dir)
        self.hold_log = CondorLog("condor_log_hold", log_dir)  # not implemented yet
        self.idle_log = CondorLog("condor_log_idle", log_dir)

    def test_if_returns_correct_state_for_idle_log(self):
        self.assertEqual(self.idle_log.get_job_state(), CondorStates.Idle)

    def test_if_returns_correct_state_for_error_log(self):
        self.assertEqual(self.error_log.get_job_state(), CondorStates.Error)

    def test_if_returns_correct_state_for_running_log(self):
        self.assertEqual(self.running_log.get_job_state(), CondorStates.Running)