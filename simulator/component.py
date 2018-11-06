import functools
from characteristics import Electrical
from states import *
import logging

SIMPLE_TLM_TYPE = (int, float, bool, str)


class Component:
    def __init__(self, id_):
        self._id = id_
        self.logger = logging.getLogger(SIM_LOG)
        self.logger.info('Initializing Sim Component %s %i' % (self.__class__.__name__, self._id))

    def log_all_properties(self, sys_depth=0, max_depth=MAX_DEPTH):
        if max_depth < sys_depth:
            return

        # Recursively print all properties to console
        properties_queue = []
        properties = vars(self)
        self.logger.debug("%s----------------------" % (indent(sys_depth)))
        self.logger.debug("%s%s %i: " % (indent(sys_depth), self.__class__.__name__, self._id))

        for name, item in properties.iteritems():
            if isinstance(item, SIMPLE_TLM_TYPE):
                # Simple tlm: Just print as is.
                self.logger.debug(" %s%s: %s" % (indent(sys_depth), name, item))
            elif isinstance(item, list):
                # List: Enqueue all for processing at next level.
                properties_queue.extend(item)
            elif isinstance(item, Component):
                # Enqueue component for processing at next level.
                properties_queue.append(item)
            elif isinstance(item, State):
                # Just print as is.
                # item.print_all_properties(sys_depth, max_depth)
                self.logger.debug(" %s%s: %s" % (indent(sys_depth), item.__class__.__name__, item.state))

        # Handle all remaining in queue
        for item in properties_queue:
            # List of components: Iterate through all at next level.
                item.log_all_properties(sys_depth + 1, max_depth)
        if sys_depth == 0:
            self.logger.debug("=============================")

    # def print_all_properties(self, sys_depth=0, max_depth=MAX_DEPTH):
    #     if max_depth < sys_depth:
    #         return
    #
    #     # Recursively print all properties to console
    #     properties_queue = []
    #     properties = vars(self)
    #     print "%s----------------------" % (indent(sys_depth))
    #     print "%s%s %i: " % (indent(sys_depth), self.__class__.__name__, self._id)
    #
    #     for name, item in properties.iteritems():
    #         if isinstance(item, SIMPLE_TLM_TYPE):
    #             # Simple tlm: Just print as is.
    #             print " %s%s: %s" % (indent(sys_depth), name, item)
    #         elif isinstance(item, list):
    #             # List: Enqueue all for processing at next level.
    #             properties_queue.extend(item)
    #         elif isinstance(item, Component):
    #             # Enqueue component for processing at next level.
    #             properties_queue.append(item)
    #         elif isinstance(item, State):
    #             # Just print as is.
    #             # item.print_all_properties(sys_depth, max_depth)
    #             item.print_state(sys_depth, max_depth)
    #
    #     # Handle all remaining in queue
    #     for item in properties_queue:
    #         # List of components: Iterate through all at next level.
    #             item.print_all_properties(sys_depth + 1, max_depth)
    #     if sys_depth == 0:
    #         print "============================="

    def get_all_components_of_type(self, type_):
        # Get all unique subcomponents of a specific type, recursively

        components = ComponentsSet()
        unique_subcomponents = ComponentsSet()

        # Place all subcomponents in queue for subsequent checkout
        for name, item in vars(self).iteritems():
            if isinstance(item, list):
                unique_subcomponents |= ComponentsSet(item)
            elif isinstance(item, Component):
                unique_subcomponents |= ComponentsSet({item})

        # Accumulate all queued items' subcomponents of desired type
        for item in unique_subcomponents:
            components |= item.get_all_components_of_type(type_)

        # Append the parent item to the running list, if component is of desired type
        if isinstance(self, type_):
            components |= ComponentsSet({self})

        # Finally, pass the unique list back up
        return components


class EnabledComponent(Component, EnabledDisabled):
    def __init__(self, id_, properties):
        Component.__init__(self, id_)
        EnabledDisabled.__init__(self)


class OnOffComponent(Component, OnOff):
    def __init__(self, id_, properties):
        Component.__init__(self, id_)
        OnOff.__init__(self)


class PoweredComponent(Electrical, Component, EnabledDisabled, OnOff):
    def __init__(self, id_, properties):
        Component.__init__(self, id_)
        Electrical.__init__(self)
        EnabledDisabled.__init__(self)
        OnOff.__init__(self)

        self._on_voltage_impact = properties.get('on_voltage_impact_volts')
        self._on_current_draw_amps = properties.get('on_current_draw_amps')

    def _update_power(power_func):
        @functools.wraps(power_func)
        def wrapper(self):
            power_func(self)
            if self.on and self.enabled:
                self.voltage_impact_volts = self._on_voltage_impact
                self.current_draw_amps = self._on_current_draw_amps
            else:
                self.voltage_impact_volts = 0.0
                self.current_draw_amps = 0.0
        return wrapper

    @_update_power
    def turn_off(self):
        OnOff.turn_off(self)

    @_update_power
    def turn_on(self):
        OnOff.turn_on(self)

    @_update_power
    def disable(self):
        EnabledDisabled.disable(self)

    @_update_power
    def enable(self):
        EnabledDisabled.enable(self)


class ComponentsSet(set):
    def __init__(self, *args, **kwargs):
        set.__init__(self, *args, **kwargs)
