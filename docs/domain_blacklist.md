# Domain 黑名单功能

## 概述

Domain 黑名单功能允许您排除特定设备类型（domain），使其不包含在发送给 LLM 的提示中。当您有大量某种类型的设备不希望通过语音命令访问，或者想通过排除不太重要的设备类型来减小提示大小时，这个功能非常有用。

## 配置方法

使用 Domain 黑名单功能的步骤：

1. 打开您的 Home Assistant 实例
2. 进入**设置** > **设备与服务**
3. 找到 **WebSocket Model Context Protocol Server** 集成并点击
4. 点击**配置**
5. 在配置表单中，您会看到一个 **domain_blacklist** 文本字段
6. 输入您想要加入黑名单的 domain，用逗号分隔（例如：`switch,light,sensor`）
7. 点击**提交**保存您的配置

## 工作原理

当集成处理要发送给 LLM 的提示时：

1. 它会检查是否配置了 domain 黑名单
2. 如果存在黑名单，它会解析提示中的 Static Context 部分
3. 任何 domain 匹配黑名单中条目的设备都会从提示中移除
4. 然后将过滤后的提示发送给 LLM

## 示例

如果您的原始提示包含：

```
Static Context: An overview of the areas and the devices in this smart home:
- names: Living Room Light
  domain: light
  areas: Living Room
- names: Kitchen Switch
  domain: switch
  areas: Kitchen
- names: Bedroom Thermostat
  domain: climate
  areas: Bedroom
```

如果您将 `switch,light` 加入黑名单，过滤后的提示将包含：

```
Static Context: An overview of the areas and the devices in this smart home:
- names: Bedroom Thermostat
  domain: climate
  areas: Bedroom
```

## 日志记录

集成会记录有关 domain 黑名单处理的信息：

- 当启用 domain 黑名单时
- 哪些设备被过滤掉
- 过滤后的最终提示

您可以在 Home Assistant 日志中使用过滤器 `custom_components.ws_mcp_server` 查看这些日志。

## 注意事项

- domain 黑名单仅影响提示的 Static Context 部分
- 它不会阻止通过其他方式控制设备
- 对黑名单的更改需要重启 Home Assistant 才能生效