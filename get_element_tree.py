#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import time
import sys
from tools import find_wechat_window
import uiautomation as auto

def output_element_tree(control, file, level=0):
    indent = '  ' * level
    control_info = get_control_info(control)
    file.write(f"{indent}{control_info}\n")
    for child in control.GetChildren():
        output_element_tree(child, file, level + 1)

def get_control_info(control):
    info = {
        'type': control.ControlTypeName,
        'name': control.Name,
        'automation_id': control.AutomationId,
        'class_name': control.ClassName,
    }
    
    if control.ControlTypeName == 'ListItemControl':
        # 获取所有子元素
        children = control.GetChildren()
        
        # 判断是否为群聊
        text_controls = [child for child in children if child.ControlTypeName == 'TextControl']
        pane_controls = [child for child in children if child.ControlTypeName == 'PaneControl']
        
        is_group = len(text_controls) >= 3 or len(pane_controls) >= 2
        info['is_group'] = is_group
        
        # 判断是否有未读消息
        # 通过检查name中是否包含“条新消息”来判断
        info['has_unread'] = '条新消息' in control.Name
        
        # 获取最后一条消息内容和时间
        if len(text_controls) >= 2:
            info['last_message'] = text_controls[-1].Name
            info['last_time'] = text_controls[-2].Name
        
        # 获取头像信息
        avatar = next((child for child in children if child.ControlTypeName == 'ImageControl'), None)
        if avatar:
            info['has_avatar'] = True
            info['avatar_class'] = avatar.ClassName
        else:
            info['has_avatar'] = False
    
    return info

if __name__ == '__main__':
    try:
        print("正在查找微信窗口...")
        wx = find_wechat_window()
        if wx:
            print("找到微信窗口，正在切换...")
            wx.SwitchToThisWindow()
            
            print("正在输出元素树...")
            with open('wechat_element_tree.txt', 'w', encoding='utf-8') as f:
                output_element_tree(wx, f)
            print("元素树已输出到 wechat_element_tree.txt 文件")
        else:
            print("未找到微信窗口，请确保微信已经打开")
            sys.exit(0)  # 程序退出
    except Exception as e:
        print("发生错误:", str(e))
        sys.exit(1)  # 使用非零退出码表示程序异常退出