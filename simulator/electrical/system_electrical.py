from collections import defaultdict

from simulator.simulator_constants import *
from simulator.component import Component, ComponentsSet
from simulator.characteristics import Electrical


class ElectricalSystem(Electrical, Component):
    def __init__(self, id_):
        Component.__init__(self, id_)
        Electrical.__init__(self)
        self.voltage_impact_volts = INITIAL_SPACECRAFT_MAIN_POWER_VOLTS
        self.current_draw_amps = INITIAL_SPACECRAFT_MAIN_POWER_CURRENT_AMPS
        self._main_power_volts = INITIAL_SPACECRAFT_MAIN_POWER_VOLTS
        self._main_power_current_amps = INITIAL_SPACECRAFT_MAIN_POWER_CURRENT_AMPS
        self._unique_components = ComponentsSet()

    def set_unique_components(self, unique_components):
        self._unique_components = unique_components

    def unique_components(self):
        return self._unique_components

    def compute_total_power(self):
        power = defaultdict(lambda: 0.0)
        for measurement in MAIN_POWER_MEASUREMENTS:
            power[measurement] = 0.0
        for component in self._unique_components:
            vars_ = vars(component)
            for measurement in MAIN_POWER_MEASUREMENTS:
                power[measurement] += vars_[measurement]
        self.logger.debug("Updating power to: %s" % (power.items()))
        self._main_power_volts = power[VOLTAGE]
        self._main_power_current_amps = power[CURRENT]

    @property
    def main_power_volts(self):
        return self._main_power_volts

    @property
    def main_power_current_amps(self):
        return self._main_power_current_amps
