"""The Model Context Protocol Server implementation.

The Model Context Protocol python sdk defines a Server API that provides the
MCP message handling logic and error handling. The server implementation provided
here is independent of the lower level transport protocol.

See https://modelcontextprotocol.io/docs/concepts/architecture#implementation-example
"""

from collections.abc import Callable, Sequence
import json
import logging
from typing import Any

from mcp import types
from mcp.server import Server
import voluptuous as vol
from voluptuous_openapi import convert

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import llm

from .const import STATELESS_LLM_API, CONF_CHECK_DEVICE_INFO

_LOGGER = logging.getLogger(__name__)


def _format_tool(
    tool: llm.Tool, custom_serializer: Callable[[Any], Any] | None
) -> types.Tool:
    """Format tool specification."""
    input_schema = convert(tool.parameters, custom_serializer=custom_serializer)
    return types.Tool(
        name=tool.name,
        description=tool.description or "",
        inputSchema={
            "type": "object",
            "properties": input_schema["properties"],
        },
    )


async def create_server(
    hass: HomeAssistant, llm_api_id: str | list[str], llm_context: llm.LLMContext, config: dict = None
) -> Server:
    """Create a new Model Context Protocol Server.

    A Model Context Protocol Server object is associated with a single session.
    The MCP SDK handles the details of the protocol.
    """
    #_LOGGER.error("mcp create server, llm_api_id:%s , llm_context:%s)",llm_api_id ,llm_context)
    #_LOGGER.error("mcp create server, STATELESS_LLM_API:%s )",STATELESS_LLM_API)
    #_LOGGER.error("mcp create server, llm.LLM_API_ASSIST:%s )",llm.LLM_API_ASSIST)
    if llm_api_id == STATELESS_LLM_API:
        llm_api_id = llm.LLM_API_ASSIST

    server = Server("home-assistant")
    #server = Server[Any]("home-assistant")

    async def get_api_instance() -> llm.APIInstance:
        """Get the LLM API selected."""
        # Backwards compatibility with old MCP Server config
        return await llm.async_get_api(hass, llm_api_id, llm_context)

    @server.list_prompts()  # type: ignore[no-untyped-call, misc]
    async def handle_list_prompts() -> list[types.Prompt]:
        llm_api = await get_api_instance()
        return [
            types.Prompt(
                name=llm_api.api.name,
                description=f"Default prompt for Home Assistant {llm_api.api.name} API",
            )
        ]

    @server.get_prompt()  # type: ignore[no-untyped-call, misc]
    async def handle_get_prompt(
        name: str, arguments: dict[str, str] | None
    ) -> types.GetPromptResult:
        llm_api = await get_api_instance()
        if name != llm_api.api.name:
            raise ValueError(f"Unknown prompt: {name}")

        # 获取原始prompt
        api_prompt = llm_api.api_prompt
        
        # 如果启用了设备信息检查
        if config and config.get(CONF_CHECK_DEVICE_INFO, False):
            # 添加设备信息获取说明
            device_info_instruction = (
                "\n\n重要提示：在控制设备前，请先使用GetLiveContext或类似函数获取设备信息，"
                "确认设备的确切名称和状态，然后再使用HassTurnOn等控制函数。"
                "这样可以避免因设备名称不匹配导致的控制失败。\n"
            )
            api_prompt = api_prompt + device_info_instruction

        return types.GetPromptResult(
            description=f"Default prompt for Home Assistant {llm_api.api.name} API",
            messages=[
                types.PromptMessage(
                    role="assistant",
                    content=types.TextContent(
                        type="text",
                        text=api_prompt,
                    ),
                )
            ],
        )

    @server.list_tools()  # type: ignore[no-untyped-call, misc]
    async def list_tools() -> list[types.Tool]:
        """List available time tools."""
        llm_api = await get_api_instance()
        _LOGGER.error("mcp list tools:%s )",llm_api.tools)
        return [_format_tool(tool, llm_api.custom_serializer) for tool in llm_api.tools]

    @server.call_tool()  # type: ignore[no-untyped-call, misc]
    async def call_tool(name: str, arguments: dict) -> Sequence[types.TextContent]:
        """Handle calling tools."""
        llm_api = await get_api_instance()
        tool_input = llm.ToolInput(tool_name=name, tool_args=arguments)
        _LOGGER.error("Tool call: %s(%s)", tool_input.tool_name, tool_input.tool_args)

        try:
            tool_response = await llm_api.async_call_tool(tool_input)
        except (HomeAssistantError, vol.Invalid) as e:
            raise HomeAssistantError(f"Error calling tool: {e}") from e
        return [
            types.TextContent(
                type="text",
                text=json.dumps(tool_response),
            )
        ]

    return server

