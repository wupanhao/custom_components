"""
Example Load Platform integration.

zm_switch:
  port: /dev/ttyAMA2
  ids: 1,2,4

"""
from __future__ import annotations

import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = 'zm_switch'

_LOGGER = logging.getLogger(__name__)

def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Your controller/hub specific code."""
    # Data that you want to share with your platforms
    hass.data[DOMAIN] = {
        'port': config[DOMAIN]['port'],
        'ids': config[DOMAIN]['ids'],
    }

    _LOGGER.warning(config[DOMAIN])

    hass.helpers.discovery.load_platform('switch', DOMAIN, {}, config)

    return True