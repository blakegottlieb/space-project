from ops.testing.test_constants import *
from ops.testing.suites.propulsion.propulsion import PropHeaterTest, PropSystemTest

from simulator.simulator import SpacecraftSim

from log.logger_factory import *

StandardLogger(GROUND_SYSTEM_LOG)
logger = logging.getLogger(GROUND_SYSTEM_LOG)

SC_ID = 1

if DEV_MODE:
    test_name = PROPULSION_HEATERS
    logger.debug('(Test Debug Message)')
    logger.info('(Test Info Message)')
    logger.warn('(Test Warning Message)')
    sc = SpacecraftSim(SC_ID)
    sc.log_all_properties()
    if test_name == PROPULSION_HEATERS:
        with PropHeaterTest(sc) as test:
            test.run()
    elif test_name == PROPULSION_SYSTEM_TEST:
        with PropSystemTest(sc) as test:
            test.run()
