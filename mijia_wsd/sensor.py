# The domain of your component. Equal to the filename of your component.
"""Platform for sensor integration."""
from homeassistant.const import TEMP_CELSIUS, PERCENTAGE
from homeassistant.helpers.entity import Entity

import logging
from bluepy import btle
from threading import Timer
import re
import time
_LOGGER = logging.getLogger(__name__)

# DOMAIN = "mijia_wsd"


class XiomiHygroThermoDelegate(object):
    def __init__(self):
        self.temperature = None
        self.humidity = None
        self.received = False
        self.count = 0

    def handleNotification(self, cHandle, raw):
        # print(cHandle, raw.hex())
        data = list(raw)
        self.temperature = (data[0]+data[1]*255)/100.0
        self.humidity = data[2]
        self.received = True


'''
def get_data():
    address = "A4:C1:38:06:C0:33"
    p = btle.Peripheral(address, btle.ADDR_TYPE_PUBLIC)
    delegate = XiomiHygroThermoDelegate()
    p.withDelegate(delegate)
    p.writeCharacteristic(0x38, bytearray([1, 0]), True)
    while not delegate.received:
        p.waitForNotifications(30.0)

    temperature = delegate.temperature
    humidity = delegate.humidity
    print("温度：", temperature, "  湿度：", humidity, "%")
'''


def poll_data(address):
    try:
        p = btle.Peripheral(address, btle.ADDR_TYPE_PUBLIC)
        delegate = XiomiHygroThermoDelegate()
        p.withDelegate(delegate)
        p.writeCharacteristic(0x38, bytearray([1, 0]), True)
        while not delegate.received:
            p.waitForNotifications(30.0)
        temperature = delegate.temperature
        humidity = delegate.humidity
        _LOGGER.info("温度：", temperature, "  湿度：", humidity, "%")
        print("温度：", temperature, "  湿度：", humidity, "%")
        return (temperature, humidity)
    except Exception as e:
        print(e)
        return None


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    print(config)
    mac = config['address']
    thermo = ThermoSensor()
    hygro = HygroSensor()

    def update():
        data = poll_data(mac)
        if data is not None:
            thermo._state = data[0]
            hygro._state = data[1]
            if thermo.hass is not None:
                # True will call the update method
                thermo.schedule_update_ha_state(force_refresh=False)
                hygro.schedule_update_ha_state(force_refresh=False)
        Timer(45, update).start()
    update()
    add_entities([thermo, hygro])


class ThermoSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def should_poll(self):
        return False

    @property
    def name(self):
        """Return the name of the sensor."""
        return '温度'

    @property
    def unique_id(self):
        """Return the unique_id of the sensor."""
        return 'sensor.mijia_wendu'

    @property
    def state(self):
        """Return the state of the sensor."""
        print('called state', self.name)
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        print('called update', self.name)
        # self._state = 23


class HygroSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def should_poll(self):
        return False

    @property
    def name(self):
        """Return the name of the sensor."""
        return '湿度'

    @property
    def unique_id(self):
        """Return the unique_id of the sensor."""
        return 'sensor.mijia_shidu'

    @property
    def state(self):
        """Return the state of the sensor."""
        print('called state', self.name)
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return PERCENTAGE

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        print('called update', self.name)
        # self._state = 23
