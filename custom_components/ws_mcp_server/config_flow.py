import voluptuous as vol
from typing import Any
import logging
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_LLM_HASS_API
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import llm,selector
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    TextSelector
)

from .const import DOMAIN

CONF_CLIENT_ENDPOINT = "client_endpoint"
CONF_MODE = "control_mode"
MORE_INFO_URL = "https://www.home-assistant.io/integrations/mcp_server/#configuration"
DEFAULT_NAME = "WebSocket MCP Server"
_LOGGER = logging.getLogger(__name__)



class WsMCPServerConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MCP Server."""
    VERSION = 1


    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        _LOGGER.error("mcp  LLM APIs available: %s",  llm.async_get_apis(self.hass))
        llm_apis = {api.id: api.name for api in llm.async_get_apis(self.hass)}
        #llm_apis = {api.id: api.name for api in await llm.async_get_apis(self.hass)}
        if user_input is not None:
            return self.async_create_entry(
                title=llm_apis[user_input[CONF_LLM_HASS_API]],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    #vol.Required(CONF_CLIENT_ENDPOINT): TextSelector(),
                    vol.Required(CONF_CLIENT_ENDPOINT): selector.TextSelector(),
                    vol.Optional(
                        CONF_LLM_HASS_API,          # llm_hass_api
                        default=llm.LLM_API_ASSIST, # assist
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=[
                                SelectOptionDict(
                                    label=name,
                                    value=llm_api_id,
                                )
                                for llm_api_id, name in llm_apis.items()
                            ]
                        )
                    ),
                }
            ),
            description_placeholders={"more_info_url": "https://example.com/mcp-server-docs"},
        )




