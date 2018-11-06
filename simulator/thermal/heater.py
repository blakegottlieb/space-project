from simulator.component import PoweredComponent, ComponentsSet


class Heater(PoweredComponent):
    def __init__(self, id_, properties):
        PoweredComponent.__init__(self, id_, properties)
        self.thermal_contribution_deg_C = properties['thermal_contribution_deg_C']
        self._nearby_thermistors = ComponentsSet()

    def link_thermistor(self, thermistor):
        self._nearby_thermistors.add(thermistor)

    @property
    def nearby_thermistors(self):
        return self._nearby_thermistors


class CatBedHeater(Heater):
    def __init__(self, id_, properties):
        Heater.__init__(self, id_, properties)
