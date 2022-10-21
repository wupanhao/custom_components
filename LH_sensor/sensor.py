# The domain of your component. Equal to the filename of your component.
"""Platform for sensor integration."""
from homeassistant.const import TEMP_CELSIUS, PERCENTAGE, STATE_UNKNOWN
from homeassistant.helpers.entity import Entity

import logging
import time
_LOGGER = logging.getLogger(__name__)

# DOMAIN = "LH_sensor"
from .ssensor import SSensor

sensor = None

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    global sensor
    _LOGGER.warning(config)
    print(config)
    port = config['port']
    id = config['id']
    if sensor is None:
        sensor = SSensor(port)
    hygro = HygroSensor(id)
    add_entities([hygro])



class HygroSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self,id):
        """Initialize the sensor."""
        self._id = id
        self._state = STATE_UNKNOWN
        self.update()

    @property
    def should_poll(self):
        return True

    @property
    def name(self):
        """Return the name of the sensor."""
        return '土壤湿度传感器'

    @property
    def unique_id(self):
        """Return the unique_id of the sensor."""
        return 'sensor.LH_shidu_'+str(self._id)

    @property
    def state(self):
        """Return the state of the sensor."""
        print('called state', self.unique_id)
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return PERCENTAGE

    @property
    def native_value(self):
        """Return the state of the device."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        print('called update', self.unique_id)
        self._state = sensor.get_humidity(self._id)
        self._attr_native_value = self._state
        # self._state = 23
