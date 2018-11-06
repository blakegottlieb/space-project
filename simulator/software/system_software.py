from simulator.simulator_constants import *
from simulator.component import Component
from simulator.states import *


class SoftwareSystem(Component):
    def __init__(self, id_):
        Component.__init__(self, id_)
        self._operational_mode = SoftwareOperationalMode()
        self._safemode_triggered = FalseTrue()

    def spacecraft_operational_mode(self):
        return self._operational_mode

    # def set_spacecraft_operational_mode(self, mode):
    #     self._operational_mode = mode

    def safemode_triggered(self):
        return self._safemode_triggered

    def acknowledge_safemode(self):
        self._safemode_triggered = FalseTrue.FALSE
