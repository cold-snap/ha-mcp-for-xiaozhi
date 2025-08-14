## ha-mcp-for-xiaozhi
- [English](README.en.md)
- [中文](README.md)


[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=c1pher-cn&repository=ha-mcp-for-xiaozhi&category=integration)

<p align="center">
  <img src="https://raw.githubusercontent.com/c1pher-cn/brands/refs/heads/master/custom_integrations/ws_mcp_server/icon.png" alt="Alt Text" align="center">
</p>  

<p align="center"> 
Homeassistant MCP server for XiaoZhi AI，directly connect to Xiaozhi AI official server.
</p>



### Capabilities
#### 1.HomeAssistant itself acts as an MCP server and connects directly to the XiaoZhi server via the websocket protocol without the need for a proxy.
#### 2.Select multiple API groups (HomeAssistant's build in Intent APIs and user-configured MCPServer) in one entity and proxy them to Xiaozhi
#### 3.Support configuring multiple entities at the same time

---
### Function demonstration（please like it for support, or post a few comments）

<a href="https://www.bilibili.com/video/BV1FMFyejExX" > Access demonstration video </a>

<a href="https://www.bilibili.com/video/BV18DM8zuEYV" > Control TV presentation (via custom script)</a>

<a href="https://www.bilibili.com/video/BV1SruXzqEW5" > HomeAssistant、LLM、MCP、XiaoZhi AI advanced tutorials </a>

---
 
### Installation：

Make sure HACS is installed in Home Assistant

1.Open HACS and search for xiaozhi or ha-mcp-for-xiaozhi

<img width="2316" height="238" alt="image" src="https://github.com/user-attachments/assets/fa49ee7c-b503-49fa-ad63-512499fa3885" />


2.Download the component

<img width="748" height="580" alt="image" src="https://github.com/user-attachments/assets/1ee75d6f-e1b0-4073-a2c7-ee0d72d002ca" />


3.Restart Home Assistant.


### Configuration：

[Settings > Devices & Services > Add Integration] > Search for "Mcp" > Find MCP Server for Xiaozhi

<img width="888" height="478" alt="image" src="https://github.com/user-attachments/assets/07a70fe1-8c6e-4679-84df-1ea05114b271" />



Next > Please fill in the Xiaozhi MCP access point address, select the required MCP > Submit. 

Note that the Assist in the llm_hass_api checkbox is the HA built-in function, 
and the other options are other MCP servers you had connected in HomeAssistant (you can directly proxy to Xiaozhi here)

<img width="774" height="632" alt="image" src="https://github.com/user-attachments/assets/38e98fde-8a6c-4434-932c-840c25dc6e28" />


Configuration is complete! Wait a minute and go to Xiaozhi's access point page and click refresh to check the

![bd06b555b9e5c24fbf819c43397c97ee](https://github.com/user-attachments/assets/ace79a44-6197-4e94-8c49-ab9048ed4502)



---

### 调试说明

 1.The tools exposed depend on the type of entity you expose to the HomeAssistant voice assistant
   
 2.Try to use the latest version of HomeAssistant. There are obvious differences in the tools provided by the May version and the March version.

 3.If debugging doesn't work as expected, first check Xiaozhi's chat log to see how he handles the command and whether he has a tool that calls HomeAssist. Currently, a major known issue is that lighting and music control can conflict with the built-in screen and music control logic. This will be resolved after the XiaGe server supports built-in tool selection next month.
 
 4.If the process correctly calls the built-in function of HA, you can open the debug log of this plug-in to observe the actual execution status.
 
---

<a href="https://star-history.com/#c1pher-cn/ha-mcp-for-xiaozhi&Date"></a>

 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=c1pher-cn/ha-mcp-for-xiaozhi&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=c1pher-cn/ha-mcp-for-xiaozhi&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=c1pher-cn/ha-mcp-for-xiaozhi&type=Date" />
 </picture>
</a>


 
 

