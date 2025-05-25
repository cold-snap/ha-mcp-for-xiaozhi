## ha-mcp-for-xiaozhi


Homeassistant MCP server for 小智AI，homeassistant 内置mcpserver通过websocket直连小智AI官方服务器。

原理：实现了mcp over websocket，省去了虾哥mcp代理部分的额外开销，不需要填任何token，只需要一个虾哥提供的mcp接入点地址

---

<a href="https://www.bilibili.com/video/BV1FMFyejExX" >接入演示视频</a>

---
 
### 安装方法：

确保Home Assistant中已安装HACS

1.打开HACS, 点击[Custom repositories], Repository 输入本项目地址: https://github.com/c1pher-cn/ha-mcp-for-xiaozhi

2.Category 选择 [Integration]

![5e1048c4fbd23d3385c09985fd09b50e](https://github.com/user-attachments/assets/db5431c6-35cf-49b4-bd0e-f2c2296df641)

3.下载插件
![d20fa7d2367fecc35bd8914b1f508ea6](https://github.com/user-attachments/assets/a8447eb4-7659-4c3e-98b1-4dbe5a6d4b30)

4.重启Home Assistant.


### 配置方法：

[设置 > 设备与服务 > 添加集成] > 搜索“Mcp” >找到MCP Server for Xiaozhi
![8ca5334a2d15f59325f3d5acb12083c8](https://github.com/user-attachments/assets/89212647-d572-45d2-98f2-60ba59203b04)


下一步 > 请填写小智MCP接入点地址 > 提交。
![6f4b22e8bd8190d4f0faeaba731481f9](https://github.com/user-attachments/assets/2f70b30c-7ced-4505-ac80-00d1a6a8280e)

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

<a href="https://star-history.com/#c1pher-cn/ha-mcp-for-xiaozhi&Date"></a>

 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=c1pher-cn/ha-mcp-for-xiaozhi&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=c1pher-cn/ha-mcp-for-xiaozhi&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=c1pher-cn/ha-mcp-for-xiaozhi&type=Date" />
 </picture>
</a>


 
 

