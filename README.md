# ha-mcp-for-xiaozhi

Homeassistant MCP server for 小智AI，homeassistant 内置mcpserver通过websocket直连小智AI官方服务器。

原理：实现了mcp over websocket，省去了虾哥mcp代理部分的额外开销，不需要填任何token，只需要一个虾哥提供的mcp接入点地址

安装方法：

确保Home Assistant中已安装HACS

1.打开HACS, 点击[Custom repositories], Repository 输入本项目地址: https://github.com/c1pher-cn/ha-mcp-for-xiaozhi

2.Category 选择 [Integration]

![5e1048c4fbd23d3385c09985fd09b50e](https://github.com/user-attachments/assets/db5431c6-35cf-49b4-bd0e-f2c2296df641)

3.下载插件
![d20fa7d2367fecc35bd8914b1f508ea6](https://github.com/user-attachments/assets/a8447eb4-7659-4c3e-98b1-4dbe5a6d4b30)

4.重启Home Assistant.


配置方法：

[设置 > 设备与服务 > 添加集成] > 搜索“Mcp” >找到MCP Server for Xiaozhi
![8ca5334a2d15f59325f3d5acb12083c8](https://github.com/user-attachments/assets/89212647-d572-45d2-98f2-60ba59203b04)


下一步 > 请填写小智MCP接入点地址 > 提交。
![6f4b22e8bd8190d4f0faeaba731481f9](https://github.com/user-attachments/assets/2f70b30c-7ced-4505-ac80-00d1a6a8280e)

配置完成！！！稍等一分钟后到小智的接入点页面点击刷新，检查状态。
![bd06b555b9e5c24fbf819c43397c97ee](https://github.com/user-attachments/assets/ace79a44-6197-4e94-8c49-ab9048ed4502)



插件刚刚发布，可能会有各种问题，欢迎反馈，反馈时请务必一起带上你的ha日志和小智官方对话的聊天记录。
