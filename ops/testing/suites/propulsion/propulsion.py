from ops.testing.suites.test_suite import TestSuite
from ops.testing.test_utils import *
from simulator.states import *
from simulator.simulator_constants import *
from ops.electrical import ElecOps
from ops.propulsion import PropOps


class PropSystemTest(TestSuite, PropOps, ElecOps):
    def __init__(self, sc):
        test_suite_name = PropHeaterTest.PROPULSION_HEATERS
        self.sc = sc
        TestSuite.__init__(self, test_suite_name)

    def run(self):
        self._prop_system_test()

    def set_up_scenario(self):
        # Can use this to inject specific testing scenarios
        self.sc.update_all_subsystems()

    # Prop operations and procedures go here:
    def check_prerequisites(self):
        # TODO: Add checks for ground station functionality and config?
        # TODO: Add checks for basic S/C health
        self.action.log_message(banner('Checking Prerequisites', "+"))
        if not IN_TVAC:
            self.check_all_engine_heaters_off()
            self.check_all_engine_heaters_disabled()

    def _prop_system_test(self):
        pass


class PropHeaterTest(TestSuite, PropOps, ElecOps):
    PROPULSION_HEATERS = 'Propulsion Heaters'

    def __init__(self, sc):
        test_suite_name = PropHeaterTest.PROPULSION_HEATERS
        self.sc = sc
        TestSuite.__init__(self, test_suite_name)

    def run(self):
        self._prop_heater_test()

    def set_up_scenario(self):
        # Can use this to inject specific testing scenarios
        self.sc.update_all_subsystems()

    # Prop operations and procedures go here:
    def check_prerequisites(self):
        self.action.log_message(banner('Checking Prerequisites', "+"))
        if not IN_TVAC:
            self.check_all_engine_heaters_off()
            self.check_all_engine_heaters_disabled()

    def _prop_heater_test(self):
        self.set_up_scenario()
        self.sc.log_all_properties()

        # Test Each Engine Heater:

        enabled = EnabledDisabled.ENABLED
        on = OnOff.ON

        for engine_id in range(NUM_ENGINES):
            initial_power = self.get_sc_power()
            initial_temp = self.get_engine_temp(engine_id)
            self.test_engine_heater_enable(enabled, engine_id)
            self.test_engine_heater_power(engine_id, on)
            self.verify_engine_heater_current(engine_id, on, initial_power)
            self.verify_engine_temp_delta(engine_id, initial_temp)
            self.sc.log_all_properties()

    def test_engine_heater_power(self, engine_id, on_off):
        test_case_name = "Engine Heater %s %s" % (engine_id, on_off)
        with self.new_test_case(test_case_name, self) as self.action:
            self.set_engine_heater_power_state(on_off, engine_id)
            self.check_engine_heater_power_state(on_off, engine_id)

    def test_engine_heater_enable(self, enabled_disabled, engine_id):
        test_case_name = "Engine Heater %s %s" % (engine_id, enabled_disabled)
        with self.new_test_case(test_case_name, self) as self.action:
            self.set_engine_heater_enable_state(enabled_disabled, engine_id)
            self.check_engine_heater_enable_state(enabled_disabled, engine_id)

    def verify_engine_heater_current(self, engine_id, on_off, initial_power):
        if on_off == OnOff.ON:
            power_factor = 1.0
        else:
            power_factor = -1.0
        engine_heater_current_amps = power_factor * COMPONENT_PROPERTIES[HEATER][CURRENT]
        tolerance = 0.1
        test_case_name = "Engine Heater %s %s-Current" % (engine_id, on_off)
        with self.new_test_case(test_case_name, self) as self.action:
            self.check_sc_current_delta(initial_power, engine_heater_current_amps, tolerance)

    def verify_engine_temp_delta(self, engine_id, initial_t):
        tolerance = 1.0
        test_case_name = "Engine Heater %s Temperature Contribution" % (engine_id)
        with self.new_test_case(test_case_name, self) as self.action:
            self.check_engine_temp_delta(initial_t, engine_id, tolerance)

    def check_engine_temp_delta(self, initial_t, engine_id, tol=0):
        characteristic = "Engine %s Temperature" % engine_id
        final_t = self.get_engine_temp(engine_id)
        expected_delta = THERMAL_CONTRIBUTION_DEG_C[HEATER]
        params = delta_check(characteristic, initial_t, final_t, expected_delta, tol)
        rez = self.action.execute(**params)
        return rez

    def clean_up_from_test(self):
        self.action.log_message(banner('Cleaning Up From Test', "+"))
        if not IN_TVAC:
            self.action.log_message(banner('Turning Off and Disabling All Heaters', "+"))
            for engine_id in range(NUM_ENGINES):
                disabled = EnabledDisabled.DISABLED
                off = OnOff.OFF
                self.set_engine_heater_enable_state(disabled, engine_id)
                self.check_engine_heater_enable_state(disabled, engine_id)
                self.set_engine_heater_power_state(off, engine_id)
                self.check_engine_heater_power_state(off, engine_id)

            self.check_all_engine_heaters_off()
            self.check_all_engine_heaters_disabled()
        self.sc.log_all_properties()
