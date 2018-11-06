from ops.testing.test_utils import *
from simulator.states import *
from simulator.simulator_constants import *


class ElecOps:
    def __init__(self):
        self.logger = logging.getLogger(GROUND_SYSTEM_LOG)

    def get_sc_power(self):
        voltage = self.sc.main_power_volts()
        current = self.sc.main_power_current_amps()
        msg = "Spacecraft Main Power Voltage is %s %s" % (voltage, "V")
        self.action.log_message(msg)
        msg = "Spacecraft Main Power Current is %s %s" % (current, "A")
        self.action.log_message(msg)
        return {VOLTAGE: voltage,
                CURRENT: current}

    def check_sc_current_delta(self, initial_power, expected_delta, tol=0):
        characteristic = "SC Current"
        final_power = self.get_sc_power()
        final = final_power[CURRENT]
        initial = initial_power[CURRENT]
        params = delta_check(characteristic, initial, final, expected_delta, tol)
        rez = self.action.execute(**params)
        return rez
