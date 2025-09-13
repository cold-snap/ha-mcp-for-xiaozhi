## ha-mcp-for-xiaozhi

![GitHub Repo stars](https://img.shields.io/github/stars/c1pher-cn/ha-mcp-for-xiaozhi?style=for-the-badge&label=Stars&color=green)
![GitHub forks](https://img.shields.io/github/forks/c1pher-cn/ha-mcp-for-xiaozhi?style=for-the-badge&label=Forks&color=green)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/c1pher-cn/ha-mcp-for-xiaozhi?style=for-the-badge&color=green)
![GitHub release (latest by date)](https://img.shields.io/github/downloads/c1pher-cn/ha-mcp-for-xiaozhi/latest/total?style=for-the-badge&color=green)

- [English](README.en.md)
- [中文](README.md)




<p align="center">
  <img src="https://raw.githubusercontent.com/c1pher-cn/brands/refs/heads/master/custom_integrations/ws_mcp_server/icon.png" alt="Alt Text" align="center">
</p>  

<p align="center"> 
Homeassistant MCP server for 小智AI，直连小智AI官方服务器。
</p>


[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=c1pher-cn&repository=ha-mcp-for-xiaozhi&category=integration)

### 插件能力介绍
#### 1.HomeAssistant自身作为mcp server 以websocket协议直接对接虾哥服务器，无需中转
#### 2.在一个实体里同时选择多个API组（HomeAssistant自带控制API、用户自己配置的MCPServer）并将它们一起代理给小智
#### 3.支持同时配置多个实体
#### 4.支持配置domain黑名单，过滤不需要的设备类型，减小prompt大小

---
### 功能演示（为爱发电不易，有币投投币、没币点点赞、刷几个弹幕也行）

<a href="https://www.bilibili.com/video/BV1XdjJzeEwe" > 接入演示视频 </a>

<a href="https://www.bilibili.com/video/BV18DM8zuEYV" > 控制电视演示（通过自定义script实现）</a>

<a href="https://www.bilibili.com/video/BV1SruXzqEW5" > HomeAssistant、LLM、MCP、小智的进阶教程 </a>

---
 
### 安装方法：

确保Home Assistant中已安装HACS

1.打开HACS, 搜索 xiaozhi 或 ha-mcp-for-xiaozhi

<img width="2316" height="238" alt="image" src="https://github.com/user-attachments/assets/fa49ee7c-b503-49fa-ad63-512499fa3885" />


2.下载插件

<img width="748" height="580" alt="image" src="https://github.com/user-attachments/assets/1ee75d6f-e1b0-4073-a2c7-ee0d72d002ca" />


3.重启Home Assistant.


### 配置方法：

[设置 > 设备与服务 > 添加集成] > 搜索“Mcp” >找到MCP Server for Xiaozhi

<img width="888" height="478" alt="image" src="https://github.com/user-attachments/assets/07a70fe1-8c6e-4679-84df-1ea05114b271" />



下一步 > 请填写小智MCP接入点地址、选择需要的MCP > 提交。

注意llm_hass_api 复选框里  Assist 就是ha自带的function，其他选项是你在HomeAssistant里接入的其他mcp server（可以在这里直接代理给小智）

<img width="774" height="632" alt="image" src="https://github.com/user-attachments/assets/38e98fde-8a6c-4434-932c-840c25dc6e28" />

配置选项说明：
- **客户端端点**：小智MCP接入点地址
- **LLM API**：选择需要的MCP，Assist是HA自带的function，其他选项是你在HomeAssistant里接入的其他mcp server
- **设备信息检查**：启用后，会在AI提示中添加获取设备信息的说明，提醒AI在控制设备前先获取设备信息，避免因设备名称不匹配导致的控制失败

### 关于设备信息检查功能

对于已有安装，更新后默认该选项为关闭状态，需要手动开启。

**注意**：开启后，在AI提示中会添加获取设备信息的说明，提醒AI在控制设备前先获取设备信息，避免因设备名称不匹配导致的控制失败，可能会导致耗时增加。

如需修改此设置：
1. 进入Home Assistant
2. 转到 [设置 > 设备与服务]
3. 找到并点击"MCP Server for Xiaozhi"集成
4. 点击"配置"按钮
5. 勾选或取消勾选"设备信息检查"选项
6. 点击"提交"保存设置

配置完成！！！稍等一分钟后到小智的接入点页面点击刷新，检查状态。

![bd06b555b9e5c24fbf819c43397c97ee](https://github.com/user-attachments/assets/ace79a44-6197-4e94-8c49-ab9048ed4502)



---

### 调试说明

 1.暴露的工具取决于你公开给Homeassistant语音助手的实体的种类
 
    设置 -> 语音助手 -> 公开
   
 2.尽量使用最新版本的homeassistant，单单看5月版本跟3月版本提供的工具就有明显差异

 3.调试时未达到预期，优先看小智的聊天记录，看看小智对这句指令如何处理的，是否有调用homeassistant的工具。目前已知比较大的问题是灯光控制和音乐控制会和内置的屏幕控制、音乐控制逻辑冲突，需要等下个月虾哥服务器支持内置工具选择后可解。

 4.如果流程正确的调用了ha内置的function，可以打开本插件的调试日志再去观测实际的执行情况。
 
---
<a href="https://buymeacoffee.com/c1pher_cn" target="_blank" rel="noreferrer noopener">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee">
</a>

<a href="https://star-history.com/#c1pher-cn/ha-mcp-for-xiaozhi&Date"></a>

 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=c1pher-cn/ha-mcp-for-xiaozhi&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=c1pher-cn/ha-mcp-for-xiaozhi&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=c1pher-cn/ha-mcp-for-xiaozhi&type=Date" />
 </picture>
</a>


 
 

