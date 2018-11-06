from collections import Counter

from log.logger_factory import *
from ops.operation import Operation, Result
from ops.testing.test_case import TestCase


class TestSuite:
    def __init__(self, test_suite_name, **kwargs):
        self.test_suite_name = test_suite_name
        self.logger = logging.getLogger(GROUND_SYSTEM_LOG)
        msg = "***** Starting %s Test Suite *****" % (self.test_suite_name)
        self.logger.info(banner(msg, "="))
        self.test_cases = []
        self.action = Operation()  # Assign a TestCase when for keeps, else a disposable Operation()

    def __enter__(self):
        self.log_test_env()
        self.check_prerequisites()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clean_up_from_test()
        self.log_summary()

    def log_test_env(self):
        # SC ID
        # Test Version
        # FSW Version
        pass

    def add_test_case(self, test_case):
        self.test_cases.append(test_case)

    def new_test_case(self, test_case_name, test_suite=None):
        test_case = TestCase(test_case_name, test_suite)
        self.add_test_case(test_case)
        return test_case

    def clear_action(self):
        self.action = Operation()

    def log_summary(self):
        msg = "TEST SUITE '%s' SUMMARY:" % (self.test_suite_name)
        self.logger.info((banner(msg, "x")))
        for test_case in self.test_cases:
            test_case.log_summary()

        results = [test_case.result.result for test_case in self.test_cases]
        counts = Counter(results)
        for outcome in Result.OUTCOMES:
            self.logger.info("%s Test Cases %s" % (counts[outcome], outcome))

        msg = "TEST SUITE '%s' SUMMARY COMPLETE" % (self.test_suite_name)
        self.logger.info((banner(msg, "x")))
