"""Support for VRF GAteway."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.climate import (
    ATTR_HVAC_MODE,
    PLATFORM_SCHEMA,
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.const import (
    ATTR_TEMPERATURE,
    CONF_HOST,
    CONF_PORT,
    EVENT_HOMEASSISTANT_STOP,
    TEMP_CELSIUS,
)

from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN
from .sgateway import SGateway

_LOGGER = logging.getLogger(__name__)
gateway = None

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the ZhongHong HVAC platform."""

    global gateway
    """Set up the Awesome switch platform."""
    data = hass.data[DOMAIN]
    _LOGGER.info(data)
    port = data['port']
    gateway = SGateway(port)
    numbers = gateway.get_numbers()

    # Add devices
    add_entities(GeneralClimate(i+1) for i in range(numbers))


class GeneralClimate(ClimateEntity):
    """Representation of a general climate."""

    _attr_hvac_modes = [
        HVACMode.COOL,
        HVACMode.HEAT,
        HVACMode.DRY,
        HVACMode.FAN_ONLY,
        HVACMode.OFF,
    ]
    _attr_should_poll = False
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.FAN_MODE
    )
    _attr_temperature_unit = TEMP_CELSIUS

    def __init__(self, id):
        """Set up the ZhongHong climate devices."""
        self._id = id
        self._target_temperature = 18
        self._current_operation = HVACMode.COOL
        self._attr_hvac_modes = HVACMode.COOL
        state = gateway.get_climate_state(id)
        if state is not None:
            self._state = state
        else:
            self._state = [0,0,0,0]

    @property
    def name(self):
        """Return the name of the thermostat, if any."""
        return self.unique_id

    @property
    def unique_id(self):
        """Return the unique ID of the HVAC."""
        return f"vrf_climate_{self._id}"

    @property
    def hvac_mode(self) -> HVACMode:
        """Return current operation ie. heat, cool, idle."""
        if self.is_on:
            return self._current_operation
        return HVACMode.OFF

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._state[2]

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return 1

    @property
    def is_on(self):
        """Return true if on."""
        return self._state[0] == 1

    @property
    def fan_mode(self):
        """Return the fan setting."""
        return self._state[3]

    @property
    def fan_modes(self):
        """Return the list of available fan modes."""
        return [0,1,2,3,4]

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return 16

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return 40

    def turn_on(self) -> None:
        """Turn on ac."""
        pass
        # return self._device.turn_on()

    def turn_off(self) -> None:
        """Turn off ac."""
        pass
        # return self._device.turn_off()

    def set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is not None:
            pass

        if (operation_mode := kwargs.get(ATTR_HVAC_MODE)) is not None:
            self.set_hvac_mode(operation_mode)

    def set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target operation mode."""
        if hvac_mode == HVACMode.OFF:
            if self.is_on:
                self.turn_off()
            return

        if not self.is_on:
            self.turn_on()

        # self._device.set_operation_mode(hvac_mode.upper())

    def set_fan_mode(self, fan_mode: str) -> None:
        """Set new target fan mode."""
        pass
        # self._device.set_fan_mode(fan_mode)