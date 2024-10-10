# 微信自动回复机器人

这是一个基于Python的微信自动回复机器人项目。它能够自动检测并回复微信中的未读消息,根据预设的回复规则进行回应。

## 主要文件

### main.py

这是项目的主要运行文件。执行此脚本可以启动自动回复功能。

功能:
- 自动检测微信窗口中的未读消息
- 根据reply.csv中预设的规则进行回复

注意: 使用时请保持微信窗口处于打开状态

### tools.py

这个文件包含了一些必要的辅助函数:

- `find_wechat_window()`: 查找并返回微信窗口对象
- `send_message()`: 向指定联系人发送消息
- `save_element_image()`: 保存UI元素的截图

### 辅助脚本

以下脚本用于学习和分析微信的UI元素结构:

#### find_item.py

用于在微信窗口中查找并保存特定UI元素的图像。

#### find_unread.py

专门用于查找并保存未读消息元素的图像。

#### get_element_tree.py

生成并输出微信窗口的完整UI元素树结构,有助于理解微信界面的层次关系。

## 使用方法

1. 确保已安装所有必要的Python库
2. 打开微信客户端并保持登录状态
3. 运行 `main.py` 脚本开始自动回复

## 注意事项

- 请遵守微信使用条款和相关法律法规
- 过度使用自动回复可能会影响您的账号安全,请谨慎使用

