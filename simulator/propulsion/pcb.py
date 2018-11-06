from simulator.simulator_constants import *
from simulator.component import Component, OnOffComponent

from simulator.thermal.thermistor import Thermistor


class PrintedCircuitBoard(OnOffComponent):
    def __init__(self, id):
        Component.__init__(self, id)
        self._thermistor = Thermistor(0)
