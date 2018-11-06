from simulator.component import Component, ComponentsSet
from simulator.simulator_constants import *


class Thermistor(Component):

    def __init__(self, id_):
        Component.__init__(self, id_)
        self.temp_C = INITIAL_AMBIENT_TEMP_C
        self._nearby_heaters = ComponentsSet()

    def set_temp_c(self, temp_c):
        self.temp_C = temp_c

    @property
    def nearby_heaters(self):
        return self._nearby_heaters

    def add_nearby_heaters(self, heaters_set):
        self._nearby_heaters |= heaters_set

    def get_nearby_heaters(self):
        return self._nearby_heaters
