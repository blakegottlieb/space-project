from log.logger_factory import *
from ops.operation import Operation


class TestCase(Operation):
    def __init__(self, test_case_name, test_suite=None):
        Operation.__init__(self, test_suite)
        self.test_case_name = test_case_name
        self._log_test_case_name()
        self.prior_test_case = None

    def _log_test_case_name(self):
        msg = "*** Test Case '%s' ***" % (self.test_case_name)
        self.logger.info(banner(msg))

    def _log_test_success(self):
        tag = "SUCCESS"
        msg = self.result.pass_msg or self.result.msg
        self.logger.info("%s: %s" % (tag, msg))

    def _log_test_failure(self):
        tag = "TEST FAILURE"
        msg = self.result.fail_msg or self.result.msg
        self.logger.error(banner("%s: %s" % (tag, msg), "!"))

    def _log_test_unknown(self):
        tag = "TEST INCONCLUSIVE"
        msg = self.result.msg
        self.logger.warn(banner("%s: %s" % (tag, msg), "?"))

    def log_result(self):
        if self.result.passed:
            self._log_test_success()
        elif self.result.failed:
            self._log_test_failure()
        elif self.result.unknown:
            self._log_test_unknown()

    def assign_result(self, test_result):
        self.result = test_result

    def log_summary(self):
        tag = self.result.result
        self.logger.info("Test %s: '%s'" % (tag, self.test_case_name))

    # Context Management
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.result.evaluate()
        if self.test_suite:
            self.test_suite.clear_action()
