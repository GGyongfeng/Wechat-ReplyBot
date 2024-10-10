#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import time
import sys
from uiautomation import WindowControl, MenuControl, ListItemControl
from tools import find_wechat_window, save_element_image

if __name__ == '__main__':
    try:
        print("正在查找微信窗口...")
        wx = find_wechat_window()
        if wx:
            print("找到微信窗口，正在切换...")
            wx.SwitchToThisWindow()
        else:
            print("未找到微信窗口，请确保微信已经打开")
            sys.exit(0)  # 程序退出
    except Exception as e:
        print("发生错误:", str(e))
        sys.exit(1)  # 使用非零退出码表示程序异常退出
    
    hw = wx.ListControl(Name='会话')
    print("开始从",hw.Name,"查找未读消息...")

    # 获取所有ListItemControl元素
    list_items = hw.GetChildren()
    unread_items = []

    # 筛选出未读消息
    for item in list_items:
        if isinstance(item, ListItemControl) and item.Name.endswith('条新消息'):
            unread_items.append(item)

    print(f"找到 {len(unread_items)} 条未读消息")

    # 保存未读消息的图片
    for index, item in enumerate(unread_items):
        try:
            save_element_image(item, f"unread_message_{index}.png")
            print(f"已保存第 {index+1} 条未读消息的图片")
        except Exception as e:
            print(f"保存第 {index+1} 条未读消息图片时出错: {str(e)}")

    print("处理完成")