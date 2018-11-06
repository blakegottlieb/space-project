from simulator.component import Component, ComponentsSet
from simulator.simulator_constants import INITIAL_AMBIENT_TEMP_C


class ThermalSystem(Component):
    def __init__(self, id_):
        Component.__init__(self, id_)
        self._heaters = ComponentsSet()
        self._thermistors = ComponentsSet()
        self.nearby_heaters_assigned = False

    def assign_heaters_set(self, heaters):
        self._heaters = heaters

    @property
    def heaters(self):
        return self._heaters

    def assign_thermistors_set(self, thermistors):
        self._thermistors = thermistors

    @property
    def thermistors(self):
        return self._thermistors

    def assign_nearby_heaters(self):
        # This should get run once during spacecraft sim
        # initialization following discover of all thermal components
        # This basically generates a reverse mapping of heaters to each thermistor
        # based on the initial mapping of thermistors to each heater
        if not self.nearby_heaters_assigned:
            for thermistor in self._thermistors:
                nearby_heaters = ComponentsSet()
                for heater in self._heaters:
                    if thermistor in heater.nearby_thermistors:
                        nearby_heaters.add(heater)
                thermistor.add_nearby_heaters(nearby_heaters)
            self.nearby_heaters_assigned = True

    @staticmethod
    def get_active_heaters(heaters):
        active_heaters = ComponentsSet()
        for heater in heaters:
            if heater.on and heater.enabled:
                active_heaters.add(heater)
        return active_heaters

    def compute_temp_boost_c(self, heaters):
        boost = 0.0
        active_heaters = self.get_active_heaters(heaters)
        for heater in active_heaters:
            boost += heater.thermal_contribution_deg_C
        return boost

    def compute_thermistor_temps(self):
        baseline_temp_c = INITIAL_AMBIENT_TEMP_C
        for thermistor in self._thermistors:
            nearby_heaters = thermistor.get_nearby_heaters()
            temp_boost_c = self.compute_temp_boost_c(nearby_heaters)
            temp_c = baseline_temp_c + temp_boost_c
            thermistor.set_temp_c(temp_c)


