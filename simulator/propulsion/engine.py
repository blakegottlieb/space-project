from simulator.simulator_constants import *
from simulator.component import Component
from simulator.states import *

from simulator.thermal.heater import Heater
from simulator.thermal.thermistor import Thermistor


class Engine(Component):
    def __init__(self, id):
        Component.__init__(self, id)
        self._thermistor = Thermistor(0)

        # TODO: Break out into a global properties file, where each component
        # simply has tags such as 'heater' that can guide
        # assignment of all internals such as voltage_draw
        # at instantiation
        heater_properties = {'on_voltage_impact_volts': ON_VOLTAGE_IMPACT_VOLTS[HEATER],
                             'on_current_draw_amps': ON_CURRENT_DRAW_AMPS[HEATER],
                             'thermal_contribution_deg_C': THERMAL_CONTRIBUTION_DEG_C[HEATER]
        }
        self._heater = Heater(0, heater_properties)
        self._heater.turn_off()
        self._heater.link_thermistor(self._thermistor)

    def set_power_of_heater(self, on_off):
        if OnOff.ON == on_off:
            self._heater.turn_on()
        elif OnOff.OFF == on_off:
            self._heater.turn_off()

    def set_enable_of_heater(self, enable_disable):
        if EnabledDisabled.ENABLED == enable_disable:
            self._heater.enable()
        elif EnabledDisabled.DISABLED == enable_disable:
            self._heater.disable()

    @property
    def heater(self):
        return self._heater

    @property
    def thermistor(self):
        return self._thermistor
