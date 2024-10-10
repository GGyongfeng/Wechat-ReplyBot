import time
from uiautomation import WindowControl
import os
from mss import mss
from PIL import Image, ImageDraw, ImageFont

def find_wechat_window(timeout=1):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            win = WindowControl(Name='微信')
            if win.Exists(0, 0):
                return win
        except Exception:
            pass
        time.sleep(1)
    return None


# 添加新的 send_message 函数
def send_message(wx, recipient_name, message):
    """
    发送消息给指定联系人
    
    :param wx: 微信窗口对象
    :param recipient_name: 接收者名称
    :param message: 要发送的消息
    :return: 布尔值，表示消息是否成功发送
    """
    try:
        # 从会话列表中寻找指定联系人
        hw = wx.ListControl(Name='会话')
        recipient = hw.ListItemControl(Name=recipient_name)
        
        if recipient.Exists():
            recipient.Click()
            time.sleep(1)  # 等待聊天窗口加载
            
            edit_control = wx.EditControl(Name=recipient_name)
            if edit_control.Exists():
                edit_control.SetFocus()
                edit_control.SendKeys(message)
                
                wx.ButtonControl(Name="发送(S)").Click()
                print(f"消息已发送给 {recipient_name}")
                return True
            else:
                print("未找到输入框")
        else:
            print(f"未找到{recipient_name}，请确保它在会话列表中可见")
    except Exception as e:
        print(f"发送消息时出错：{str(e)}")
    
    return False

def save_element_image(element, name, img_dir='./item-finded'):
    # 确保图片保存目录存在
    os.makedirs(img_dir, exist_ok=True)
    
    # 获取元素的位置和大小
    rect = element.BoundingRectangle
    left, top, right, bottom = rect.left, rect.top, rect.right, rect.bottom
    
    # 截取屏幕
    with mss() as sct:
        # 扩大截图区域
        padding = 50  # 增加padding以确保有足够空间显示标签
        monitor = {
            "top": max(0, top - padding),
            "left": max(0, left - padding),
            "width": right - left + 2 * padding,
            "height": bottom - top + 2 * padding
        }
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
    
    # 创建一个可以绘图的对象
    draw = ImageDraw.Draw(img)
    
    # 在图像上绘制红色框，考虑新的padding
    draw.rectangle([padding, padding, right-left+padding, bottom-top+padding], outline=(255, 0, 0), width=2)
    
    # 添加元素名称
    try:
        font = ImageFont.truetype("simhei.ttf", 20)  # 使用黑体字体，如果系统中没有，请替换为其他中文字体
    except IOError:
        font = ImageFont.load_default()
    
    # 将文本绘制位置移到左上角
    draw.text((5, 5), name, fill=(255, 0, 0), font=font)
    
    # 保存图像
    safe_name = "".join([c if c.isalnum() else "_" for c in name])
    file_name = f"{safe_name}_{int(time.time())}.png"
    img.save(os.path.join(img_dir, file_name))