"""Platform for zm_switch integration."""
from __future__ import annotations

import logging

import voluptuous as vol

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import (SwitchEntity,PLATFORM_SCHEMA)
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN
from .sswitch import SSwitch

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required('ids'): cv.string,
    vol.Optional('port', default='admin'): cv.string,
})

_LOGGER = logging.getLogger(__name__)

switch = None

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    global switch
    """Set up the Awesome switch platform."""
    data = hass.data[DOMAIN]
    _LOGGER.info(data)
    port = data['port']
    ids = [int(i) for i in data['ids'].split(',')] 
    switch = SSwitch(port)

    # Add devices
    add_entities(ZMSwitch(i) for i in ids)

class ZMSwitch(SwitchEntity):
    """Representation of a ZM Switch."""

    def __init__(self, id) -> None:
        """Initialize a ZM Switch."""
        self._addr = id
        self._name = "switch.zm_switch_%2d" % id
        self._state = switch.get_switch_state(self._addr)
        _LOGGER.info("ZM Switch with id %d added" % id)

    @property
    def name(self) -> str:
        """Return the display name of this switch."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique_id of the switch."""
        return self._name

    @property
    def is_on(self) -> bool | None:
        """Return true if switch is on."""
        return self._state

    def turn_on(self, **kwargs: Any) -> None:
        """Instruct the switch to turn on.
        You can skip the brightness part if your switch does not support
        brightness control.
        """
        switch.switch_on(self._addr)
        self._state = True
        # self.update()

    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the switch to turn off."""
        switch.switch_off(self._addr)
        self._state = False
        # self.update()

    def update(self) -> None:
        """Fetch new state data for this switch.
        This is the only method that should fetch new data for Home Assistant.
        """
        pass
        # self._state = switch.get_switch_state(self._addr)