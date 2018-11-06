from log.logger_factory import *
from main_constants import *


class State:
    def __init__(self):
        self.state = None

    def print_state(self, sys_depth=0, max_depth=MAX_DEPTH):
        if max_depth < sys_depth:
            return

        print " %s%s: %s" % (indent(sys_depth), self.__class__.__name__, self.state)

    def print_all_properties(self, sys_depth=0, max_depth=MAX_DEPTH):
        # TODO: Update this to just print state.
        # Probably do not need to print all properties here.
        if max_depth < sys_depth:
            return

        # Recursively print all properties to console
        properties = vars(self)

        for name, item in properties.iteritems():
            if type(item) in [str, int, float, bool]:
                # Simple tlm: Just print as is.
                print " %s%s: %s" % (indent(sys_depth), name, item)
            else:
                # Just print as is.
                print " %s%s: %s" % (indent(sys_depth), name, item)


class FalseTrue(State):
    FALSE = False
    TRUE = True
    STATES = [FALSE, TRUE]

    def __init__(self, initial_state=FALSE):
        self.false_true_status = initial_state

    @property
    def state(self):
        return self.false_true_status

    @property
    def true(self):
        return self.TRUE == self.false_true_status

    @property
    def false(self):
        return self.FALSE == self.false_true_status


class TrueFalse(State):
    TRUE = True
    FALSE = False
    STATES = [TRUE, FALSE]

    def __init__(self, initial_state=TRUE):
        self.true_false_status = initial_state

    @property
    def state(self):
        return self.true_false_status

    @property
    def true(self):
        return self.TRUE == self.true_false_status

    @property
    def false(self):
        return self.FALSE == self.true_false_status


class OnOff(State):
    OFF = 'OFF'
    ON = 'ON'
    STATES = [OFF, ON]

    def __init__(self, initial_state=OFF):
        self.on_off_status = initial_state

    @property
    def state(self):
        return self.on_off_status

    def turn_off(self):
        old_state = self.on_off_status
        new_state = self.OFF
        if old_state != new_state:
            self.on_off_status = new_state

    def turn_on(self):
        old_state = self.on_off_status
        new_state = self.ON
        if old_state != new_state:
            self.on_off_status = new_state

    @property
    def on(self):
        return self.ON == self.on_off_status

    @property
    def off(self):
        return self.OFF == self.on_off_status


class EnabledDisabled(State):
    DISABLED = 'DISABLED'
    ENABLED = 'ENABLED'
    STATES = [DISABLED, ENABLED]

    def __init__(self, initial_state=DISABLED):
        self.enabled_status = initial_state

    @property
    def state(self):
        return self.enabled_status

    def disable(self):
        old_state = self.enabled_status
        new_state = self.DISABLED
        if old_state != new_state:
            self.enabled_status = new_state

    def enable(self):
        old_state = self.enabled_status
        new_state = self.ENABLED
        if old_state != new_state:
            self.enabled_status = new_state

    @property
    def enabled(self):
        return self.ENABLED == self.enabled_status

    @property
    def disabled(self):
        return self.DISABLED == self.enabled_status


class SoftwareOperationalMode(State):
    NOMINAL_EARTH_POINTING = 'NOMINAL_EARTH_POINTING'
    SAFE_MODE = 'SAFE_MODE'
    STATES = [NOMINAL_EARTH_POINTING, SAFE_MODE]

    def __init__(self, initial_state=NOMINAL_EARTH_POINTING):
        self.mode = initial_state

    @property
    def state(self):
        return self.mode
