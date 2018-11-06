from simulator.states import *
from simulator.simulator_constants import *


class PropOps:
    def __init__(self):
        self.logger = logging.getLogger(GROUND_SYSTEM_LOG)

    def check_all_engine_heaters_off(self):
        self.action.log_message(banner('Checking All Heaters Are Off', "+"))
        for engine_id in range(NUM_ENGINES):
            off = OnOff.OFF
            self.check_engine_heater_power_state(off, engine_id)

    def check_all_engine_heaters_disabled(self):
        self.action.log_message(banner('Checking All Heaters Are Disabled', "+"))
        for engine_id in range(NUM_ENGINES):
            disabled = EnabledDisabled.DISABLED
            self.check_engine_heater_enable_state(disabled, engine_id)

    def set_engine_heater_enable_state(self, enable_disable, engine_id):
        msg = "Setting Engine Heater %s to %s" % (engine_id, enable_disable)
        self.action.log_message(msg)
        self.sc.set_enable_of_engine_heater(enable_disable, engine_id)

    def check_engine_heater_enable_state(self, enable_disable, engine_id):
        condition = self.sc.engine_heater_enable_status(engine_id) == enable_disable
        pass_msg = "Engine Heater %s: %s" % (engine_id, enable_disable)
        fail_msg = "Engine Heater %s NOT %s" % (engine_id, enable_disable)
        params = {'condition': condition, 'pass_msg': pass_msg, 'fail_msg': fail_msg}
        rez = self.action.execute(**params)
        return rez

    def set_engine_heater_power_state(self, on_off, engine_id):
        msg = "Setting Engine Heater %s to %s" % (engine_id, on_off)
        self.action.log_message(msg)
        self.sc.set_power_of_engine_heater(on_off, engine_id)

    def check_engine_heater_power_state(self, on_off, engine_id):
        condition = self.sc.engine_heater_power_status(engine_id) == on_off
        pass_msg = "Engine Heater %s: %s" % (engine_id, on_off)
        fail_msg = "Engine Heater %s NOT %s" % (engine_id, on_off)
        params = {'condition': condition, 'pass_msg': pass_msg, 'fail_msg': fail_msg}
        rez = self.action.execute(**params)
        return rez

    def get_engine_temp(self, engine_id):
        temperature = self.sc.engine_temp(engine_id)
        msg = "Engine %s Temperature is %s %s" % (engine_id, temperature, "C")
        self.action.log_message(msg)
        return temperature
