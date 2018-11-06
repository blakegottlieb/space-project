from simulator.simulator_constants import *
from simulator.component import Component

from simulator.propulsion.engine import Engine
from simulator.propulsion.pcb import PrintedCircuitBoard

from simulator.characteristics import Electrical


class PropulsionSystem(Electrical, Component):
    def __init__(self, id_):
        Component.__init__(self, id_)
        Electrical.__init__(self)
        self._engines = []
        self._initialize_engines()

    def _initialize_engines(self):
        for i in range(NUM_ENGINES):
            self._engines.append(Engine(i))

    def set_power_of_engine_heater(self, on_off, engine_id):
        self._engines[engine_id].set_power_of_heater(on_off)

    def set_enable_of_engine_heater(self, enable_disable, engine_id):
        self._engines[engine_id].set_enable_of_heater(enable_disable)

    @property
    def engines(self):
        return self._engines
