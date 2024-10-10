#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import time
import sys
from uiautomation import WindowControl, MenuControl,ListItemControl
from tools import find_wechat_window, send_message
from pynput import mouse

def get_reply(message, name=None, **kwargs):
    """
    根据输入的消息获取回复内容
    
    :param message: 输入的消息文本
    :param name: 发送者的名字(可选)
    :param kwargs: 其他可能的参数
    :return: 回复的文本
    """
    # 通过pd读取数据，指定列名
    df = pd.read_csv('reply.csv', encoding='utf-8', sep='\\', names=['序号', '关键词', '回复内容'])
    
    # 寻找匹配的关键词并获取对应的回复内容
    for _, row in df.iterrows():
        if row['关键词'] in message:
            reply = row['回复内容']
            # 如果提供了名字,可以进行个性化定制
            if name:
                reply = reply.replace('你', name)
            return reply
    
    # 如果没有找到匹配的关键词,返回None
    return None

def on_move(x, y):
    global mouse_moved
    mouse_moved = True

def mouse_listener():
    global mouse_moved
    with mouse.Listener(on_move=on_move) as listener:
        listener.join()

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

    print('正在监听微信窗口ing')


    while True:

        hw = wx.ListControl(Name='会话')

        # 获取所有ListItemControl元素
        list_items = hw.GetChildren()
        unread_items = []

        # 筛选出未读消息
        for item in list_items:
            if isinstance(item, ListItemControl) and item.Name.endswith('条新消息'):
                unread_items.append(item)

        if len(unread_items) > 0:
            print(f"找到 {len(unread_items)} 条未读消息")

        # 处理未读消息
        for unread_item in unread_items:
            # 点击未读消息
            unread_item.Click() #click之后其Name属性会随之改变

            # 读取最后一条消息内容
            message_control = wx.ListControl(Name="消息")
            last_message = message_control.GetChildren()[-1].Name
            
            # 获取发送者名称
            sender_name = unread_item.Name
            
            # 使用get_reply函数获取回复内容
            message_to_send = get_reply(last_message)
            
            # 只有在找到匹配的回复时才发送消息
            if message_to_send is not None:
                send_message(wx, sender_name, message_to_send)

        # 添加适当的延时，避免过于频繁地检查
        time.sleep(1)  # 减少延迟以提高响应速度
