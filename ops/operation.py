from log.logger_factory import *


class Operation:
    def __init__(self, test_suite=None):
        self.test_suite = test_suite
        self.logger = logging.getLogger(GROUND_SYSTEM_LOG)
        self.result = Result()

    def log_message(self, msg):
        self.logger.info(msg)

    def _log_op_success(self):
        msg = self.result.pass_msg or self.result.msg
        self.logger.info("%s" % (msg))

    def _log_op_failure(self):
        tag = "OPERATION FAILED"
        msg = self.result.fail_msg or self.result.msg
        self.logger.error(banner("%s: %s" % (tag, msg), "!"))

    def log_result(self):
        if self.result.passed:
            self._log_op_success()
        else:
            self._log_op_failure()

    def define_all(self, **kwargs):
        condition = kwargs.get('condition')
        pass_msg = kwargs.get('pass_msg')
        fail_msg = kwargs.get('fail_msg')
        msg = kwargs.get('msg')

        if pass_msg:
            self.result.pass_msg = pass_msg
        if fail_msg:
            self.result.fail_msg = fail_msg
        if msg:
            self.result.msg = msg
        if condition is not None:
            self.result.condition = condition

    def execute(self, **kwargs):
        self.define_all(**kwargs)
        self.result.evaluate()
        self.log_result()
        return self.result


class Result:
    PASSED = "Passed"
    FAILED = "Failed"
    UNKNOWN = "Unknown"
    OUTCOMES = [PASSED, FAILED, UNKNOWN]

    def __init__(self, condition=None, **kwargs):
        self.msg = kwargs.get('msg', "")
        self.pass_msg = kwargs.get('pass_msg', "")
        self.fail_msg = kwargs.get('fail_msg', "")
        self.result = self.UNKNOWN
        self.condition = condition
        self.evaluate()

    def evaluate(self):
        if self.condition is not None:
            if self.condition is True:
                self.mark_passed()
            else:
                self.mark_failed()

    def mark_passed(self):
        self.result = self.PASSED

    def mark_failed(self):
        self.result = self.FAILED

    @property
    def passed(self):
        return self.result == self.PASSED

    @property
    def failed(self):
        return self.result == self.FAILED

    @property
    def unknown(self):
        return self.result == self.UNKNOWN
