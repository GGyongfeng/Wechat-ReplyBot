#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import sys
from tools import find_wechat_window, save_element_image 

def find_and_save_elements(element, target_elements, depth=0):
    if depth > 15:
        return
    
    try:
        # 获取元素名称
        element_type = element.ControlTypeName
        element_name = element.Name if element.Name else ""
        full_name = f"{element_type}(Name='{element_name}')"
        
        # 检查当前元素是否匹配目标元素之一
        for target in target_elements:
            if (target.get('type') == element_type and
                (not target.get('name') or target['name'] in element_name)):
                print(f"找到目标元素: {full_name}")
                # 调用tools.py中的save_element_image函数保存元素图像
                save_element_image(element, full_name)  # 调用方法
                break

        else:
            # 递归处理所有子元素
            for child in element.GetChildren():
                find_and_save_elements(child, target_elements, depth=depth + 1)
    except Exception as e:
        print(f"处理元素时出错: {str(e)}")



if __name__ == '__main__':
    try:
        print("正在查找微信窗口...")
        wx = find_wechat_window()
        #寻找会话控件绑定

        if wx:
            print("找到微信窗口，正在切换...")
            wx.SwitchToThisWindow()

            hw = wx.ListControl(Name='会话')
            print("开始从",hw.Name,"查找指定元素...")
            
            # 定义要查找的目标元素
            target_elements = [
                {'type': 'ListItemControl', 'name': ''},  # 指定会话
            ]
            
            find_and_save_elements(hw, target_elements)
        else:
            print("未找到微信窗口，请确保微信已经打开")
            sys.exit(0)  # 程序退出
    except Exception as e:
        print("发生错误:", str(e))
        sys.exit(1)  # 使用非零退出码表示程序异常退出