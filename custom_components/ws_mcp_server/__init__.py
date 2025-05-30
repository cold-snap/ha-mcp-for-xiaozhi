
"""The Model Context Protocol Server integration."""

from __future__ import annotations
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
import logging
from .websocket_transport import _connect_to_client
from . import websocket_transport
from .const import DOMAIN
from .session import SessionManager
from .types import WsMCPServerConfigEntry
_LOGGER = logging.getLogger(__name__)

__all__ = [
    "CONFIG_SCHEMA",
    "DOMAIN",
    "async_setup",
    "async_setup_entry",
    "async_unload_entry",
]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Model Context Protocol component."""
    #websocket_transport.async_register(hass)
    return True


#async def async_setup_entry(hass: HomeAssistant, entry: WsMCPServerConfigEntry) -> bool:
#    """Set up Model Context Protocol Server from a config entry."""
#    entry.runtime_data = SessionManager()
#    await websocket_transport.async_setup_entry(hass,entry)
#    return True
    
async def async_setup_entry(hass: HomeAssistant, entry: WsMCPServerConfigEntry) -> bool:
    """Set up Model Context Protocol Server from a config entry."""
    async def _system_started(event):
        entry.runtime_data = SessionManager()
        await websocket_transport.async_setup_entry(hass,entry)

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _system_started)
    return True
    


async def async_unload_entry(hass: HomeAssistant, entry: WsMCPServerConfigEntry) -> bool:
    """Unload a config entry."""
    session_manager = entry.runtime_data
    session_manager.close()
    return True

