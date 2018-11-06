
from simulator_constants import *
from component import Component, ComponentsSet
from thermal.thermistor import Thermistor
from thermal.heater import Heater

from propulsion.system_propulsion import PropulsionSystem
from electrical.system_electrical import ElectricalSystem
from software.system_software import SoftwareSystem
from thermal.system_thermal import ThermalSystem

from characteristics import Electrical

from log.logger_factory import StandardLogger
import logging
import functools


class SpacecraftSim(Electrical, Component):
    def __init__(self, id_):
        StandardLogger(SIM_LOG)
        self.logger = logging.getLogger(SIM_LOG)
        self.logger.info('Initializing Spacecraft Simulator')

        Component.__init__(self, id_)
        Electrical.__init__(self)

        self._propulsion_system = PropulsionSystem(0)
        self._electrical_system = ElectricalSystem(0)
        self._software_system = SoftwareSystem(0)
        self._thermal_system = ThermalSystem(0)

        self._electrical_system.set_unique_components(ComponentsSet(self.get_all_components_of_type(Electrical)))
        self._thermal_system.assign_heaters_set(ComponentsSet(self.get_all_components_of_type(Heater)))
        self._thermal_system.assign_thermistors_set(ComponentsSet(self.get_all_components_of_type(Thermistor)))

        self._thermal_system.assign_nearby_heaters()

    def update_electrical_subsystem(self):
        self._electrical_system.compute_total_power()

    def update_thermal_subsystem(self):
        self._thermal_system.compute_thermistor_temps()

    def update_software_subsystem(self):
        pass

    def update_propulsion_subsystem(self):
        pass

    def update_all_subsystems(self):
        self.update_electrical_subsystem()
        self.update_propulsion_subsystem()
        self.update_software_subsystem()
        self.update_thermal_subsystem()

    def _update_sim_after(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.update_all_subsystems()

        return wrapper

    # For expedience, let's pretend these methods are actual commands:
    @_update_sim_after
    def set_enable_of_engine_heater(self, enable_disable, engine_id):
        self._propulsion_system.set_enable_of_engine_heater(enable_disable, engine_id)

    @_update_sim_after
    def set_power_of_engine_heater(self, on_off, engine_id):
        self._propulsion_system.set_power_of_engine_heater(on_off, engine_id)

    # For expedience, let's pretend these methods are actual telemetry:
    def main_power_current_amps(self):
        return self._electrical_system.main_power_current_amps

    def main_power_volts(self):
        return self._electrical_system.main_power_volts

    def engine_heater_enable_status(self, engine_id):
        return self._propulsion_system.engines[engine_id].heater.enabled_status

    def engine_heater_power_status(self, engine_id):
        return self._propulsion_system.engines[engine_id].heater.on_off_status

    def engine_temp(self, engine_id):
        return self._propulsion_system.engines[engine_id].thermistor.temp_C