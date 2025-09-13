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

from .const import STATELESS_LLM_API, CONF_CHECK_DEVICE_INFO, CONF_DOMAIN_BLACKLIST

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
    _LOGGER.warning("Creating MCP Server：config=%s", config)
    if config:
        _LOGGER.warning("check_device_info=%s", config.get(CONF_CHECK_DEVICE_INFO, False))
    
    if llm_api_id == STATELESS_LLM_API:
        llm_api_id = llm.LLM_API_ASSIST
    _LOGGER.warning("LLM API ID: %s", llm_api_id)

    server = Server("home-assistant")
    #server = Server[Any]("home-assistant")

    async def get_api_instance() -> llm.APIInstance:
        """Get the LLM API selected."""
        _LOGGER.warning("LLM API Instance，llm_api_id: %s", llm_api_id)
        # Backwards compatibility with old MCP Server config
        api_instance = await llm.async_get_api(hass, llm_api_id, llm_context)
        api_instance.api_prompt = await modify_prompt_with_device_check(api_instance.api_prompt)
        _LOGGER.warning("Got API Inatance，api_name: %s, prompt : %s", 
                     api_instance.api.name, 
                     api_instance.api_prompt)
        return api_instance

    @server.list_prompts()  # type: ignore[no-untyped-call, misc]
    async def handle_list_prompts() -> list[types.Prompt]:
        _LOGGER.warning("handle_list_prompts called")
        llm_api = await get_api_instance()
        # 确保prompt已经被修改
        llm_api.api_prompt = await modify_prompt_with_device_check(llm_api.api_prompt)
        _LOGGER.warning("handle_list_prompts: api_prompt modified")
        prompts = [
            types.Prompt(
                name=llm_api.api.name,
                description=f"Default prompt for Home Assistant {llm_api.api.name} API",
            )
        ]
        _LOGGER.warning("handle_list_prompts: returning prompts=%s", prompts)
        return prompts

    # 修改prompt的函数
    async def modify_prompt_with_device_check(original_prompt):
        if not original_prompt:
            return original_prompt
            
        # 处理domain黑名单
        domain_blacklist = []
        if config and CONF_DOMAIN_BLACKLIST in config and config[CONF_DOMAIN_BLACKLIST]:
            # 解析黑名单配置，将字符串转换为列表
            blacklist_str = config[CONF_DOMAIN_BLACKLIST]
            domain_blacklist = [domain.strip() for domain in blacklist_str.split(',') if domain.strip()]
            _LOGGER.warning("Domain blacklist enabled: %s", domain_blacklist)
            
            # 如果有黑名单，过滤掉黑名单中的设备
            if domain_blacklist and original_prompt:
                # 查找静态上下文部分
                static_context_start = original_prompt.find("Static Context:")
                if static_context_start != -1:
                    # 分割prompt为前半部分和静态上下文部分
                    pre_context = original_prompt[:static_context_start]
                    static_context = original_prompt[static_context_start:]
                    
                    try:
                        # 将静态上下文部分转换为YAML格式
                        # 找到第一个设备定义的开始（以names开头的行）
                        context_lines = static_context.split('\n')
                        start_idx = -1
                        for i, line in enumerate(context_lines):
                            if line.strip().startswith('- names:'):
                                start_idx = i
                                break
                        
                        if start_idx == -1:
                            _LOGGER.warning("No device definitions found in static context")
                            return original_prompt
                            
                        # 只处理从第一个设备定义开始的行
                        device_lines = []
                        for line in context_lines[start_idx:]:
                            if line.strip():
                                if line.strip().startswith('- names:'):
                                    device_lines.append('  ' + line.strip())
                                else:
                                    device_lines.append('    ' + line.strip())
                        yaml_str = "devices:\n" + '\n'.join(device_lines)
                        import yaml
                        devices_data = yaml.safe_load(yaml_str)
                        
                        # 过滤掉黑名单中的设备
                        filtered_devices = []
                        for device in devices_data.get('devices', []):
                            if device.get('domain') not in domain_blacklist:
                                filtered_devices.append(device)
                        
                        # 将过滤后的设备转换回YAML格式
                        filtered_yaml = yaml.dump(filtered_devices, allow_unicode=True, sort_keys=False, default_flow_style=False)
                        # 调整缩进格式
                        formatted_lines = []
                        for line in filtered_yaml.split('\n'):
                            if line.strip():
                                if line.startswith('- '):
                                    formatted_lines.append('  ' + line)
                                else:
                                    formatted_lines.append('    ' + line)
                        
                        # 重建静态上下文
                        filtered_static_context = "Static Context: An overview of the areas and the devices in this smart home:\n" + '\n'.join(formatted_lines)
                        original_prompt = pre_context + filtered_static_context
                        _LOGGER.warning("Prompt filtered by domain blacklist using YAML parsing")
                    except yaml.YAMLError as e:
                        _LOGGER.error("Error parsing YAML: %s", e)
                        # 如果YAML解析失败，保持原始prompt不变
                        _LOGGER.warning("Falling back to original prompt due to YAML parsing error")
        
        # 如果启用了设备信息检查
        if config and config.get(CONF_CHECK_DEVICE_INFO, False):
            _LOGGER.warning("Device info check enabled, modifying prompt")
            # 添加设备信息获取说明（强制要求）- 英文版
            device_info_instruction = (
                "\n\n## MANDATORY INSTRUCTION: Device information must be obtained before control\n"
                "Before calling any device control functions (HassTurnOn, HassTurnOff, HassSetPosition, etc.), "
                "you **MUST** first call the GetLiveContext function to obtain accurate device information.\n\n"
                "### Required Workflow:\n"
                "1. First call GetLiveContext to get the status and accurate names of all available devices\n"
                "2. Confirm the exact name of the device to be controlled based on the returned device information\n"
                "3. Only then call the appropriate control function\n\n"
                "### Consequences of violating this rule:\n"
                "- Device control may fail\n"
                "- Wrong devices may be controlled\n"
                "- Poor user experience\n\n"
                "**Note: This is a mandatory requirement, not a suggestion!**\n"
            )
            original_prompt = original_prompt + device_info_instruction
            _LOGGER.warning("Prompt modification completed, device info check instruction added")
        
        _LOGGER.warning("Final api_prompt: %s", original_prompt)
        return original_prompt
    
    @server.get_prompt()  # type: ignore[no-untyped-call, misc]
    async def handle_get_prompt(
        name: str, arguments: dict[str, str] | None
    ) -> types.GetPromptResult:
        _LOGGER.warning("handle_get_prompt called, name: %s", name)
        llm_api = await get_api_instance()
        if name != llm_api.api.name:
            raise ValueError(f"Unknown prompt: {name}")

        # 获取原始prompt
        api_prompt = llm_api.api_prompt
        _LOGGER.warning("Original api_prompt: %s", api_prompt)
        
        # 检查配置状态
        _LOGGER.warning("Current config status: config=%s, check_device_info=%s", 
                     config is not None, 
                     config.get(CONF_CHECK_DEVICE_INFO, False) if config else False)
        
        # 修改prompt
        api_prompt = await modify_prompt_with_device_check(api_prompt)

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
        _LOGGER.warning("list_tools called, checking if before get_prompt")
        llm_api = await get_api_instance()
        
        # 修改prompt
        llm_api.api_prompt = await modify_prompt_with_device_check(llm_api.api_prompt)
        _LOGGER.warning("Modified api_prompt in list_tools: %s", llm_api.api_prompt)
        
        _LOGGER.warning("Current config status in list_tools: config=%s, check_device_info=%s", 
                     config is not None, 
                     config.get(CONF_CHECK_DEVICE_INFO, False) if config else False)
        _LOGGER.error("mcp list tools:%s )",llm_api.tools)
        return [_format_tool(tool, llm_api.custom_serializer) for tool in llm_api.tools]

    @server.call_tool()  # type: ignore[no-untyped-call, misc]
    async def call_tool(name: str, arguments: dict) -> Sequence[types.TextContent]:
        """Handle calling tools."""
        llm_api = await get_api_instance()
        
        # 确保prompt已经被修改
        llm_api.api_prompt = await modify_prompt_with_device_check(llm_api.api_prompt)
        
        tool_input = llm.ToolInput(tool_name=name, tool_args=arguments)
        _LOGGER.error("Tool call: %s(%s)", tool_input.tool_name, tool_input.tool_args)
        
        # 如果启用了设备信息检查，记录控制函数调用
        if config and config.get(CONF_CHECK_DEVICE_INFO, False):
            control_tools = ['HassTurnOn', 'HassTurnOff', 'HassSetPosition', 'HassClimateSetTemperature', 
                           'HassFanSetSpeed', 'HassLightSet', 'HassSetVolume', 'HassSetVolumeRelative']
            if name in control_tools:
                _LOGGER.error("WARNING: Direct call to device control function %s while device info check is enabled!", name)

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

