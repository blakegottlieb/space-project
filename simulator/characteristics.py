

class Characteristics:
    def __init__(self):
        pass


class Electrical(Characteristics):

    def __init__(self):
        Characteristics.__init__(self)
        self.voltage_impact_volts = 0.0
        self.current_draw_amps = 0.0
