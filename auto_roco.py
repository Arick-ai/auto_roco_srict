# -*- coding: utf-8 -*-
import os
import pyautogui
import webbrowser
import time
import subprocess
import psutil
import fnmatch
import tkinter as tk
from tkinter import messagebox

from pywinauto import Desktop

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import re

debug = 0
personal_path = r"C:\Users\19508\Desktop\封包"  ## fz location

pets = {
    "虫王": {
        "身高": 1.8,
        "体重": 46,
        "属性": ["虫"],
        "性别": "雌",
        "kj打法": "虫王打法",
        "携带坐标": (2048, 1616),
        "打法坐标": (594, 1484),
        "哨兵打法坐标": (850, 1503),
        "七曜打法坐标": (1024, 1503)
    },
    "苍羽": {
        "身高": 1.8,
        "体重": 68,
        "属性": ["龙", "翼"],
        "性别": "雄",
        "kj打法": "苍羽打法",
        "携带坐标": (2048, 1648),
        "打法坐标": (594, 1541),
        "哨兵打法坐标": (850, 1558),
        "七曜打法坐标": (1024, 1558)
    },
    "立冬": {
        "身高": 1.6,
        "体重": 65,
        "属性": ["冰", "机械"],
        "性别": "雌",
        "kj打法": "立冬打法",
        "携带坐标": (2048, 1583),
        "打法坐标": (594, 1567),
        "哨兵打法坐标": (850, 1583),
        "七曜打法坐标": (1024, 1583)
    },
    "魔武": {
        "身高": 2.2,
        "体重": 128,
        "属性": ["恶魔", "武"],
        "性别": "雄",
        "kj打法": "魔武打法",
        "携带坐标": (2048, 1552),
        "打法坐标": (594, 1595),
        "哨兵打法坐标": (850, 1617),
        "七曜打法坐标": (1024, 1617)
    },
    "碧水": {
        "身高": 1.5,
        "体重": 34.9,
        "属性": ["水"],
        "性别": "雌",
        "kj打法": "碧水灵兽打法",
        "携带坐标": (2048, 1681), #select_pos
        "打法坐标": (594, 1636),   #pick_pos
        "哨兵打法坐标": (850, 1648),
        "七曜打法坐标": (1024, 1648)
    },
    "伊莱娜": {
        "身高": 1.66,
        "体重": 66.88,
        "属性": ["机械"],
        "性别": "雌",
        "kj打法": "伊莱娜打法",
        "携带坐标": (2048, 0),
        "打法坐标": (0, 0),
        "哨兵打法坐标": (850, 1678),
        "七曜打法坐标": (1024, 1678)
    },
    "龙王": {
        "身高": 10.5,
        "体重": 998,
        "属性": ["龙"],
        "性别": "雄",
        "kj打法": "龙王打法",
        "携带坐标": (2048, 1498),
        "打法坐标": (594, 1699),
        "哨兵打法坐标": (850, 1700),
        "七曜打法坐标": (1024, 1700)
    },
    "青琼灵犬": {
        "身高": 0.9,
        "体重": 29,
        "属性": ["火"],
        "性别": "雄",
        "kj打法": "自定义",
        "携带坐标": (2048, 1542),
        "打法坐标": (594, 1699),
        "哨兵打法坐标": (850, 1739),
        "七曜打法坐标": (1024, 0)
    }
}

def test_get_top_window_txt():
    # 获取当前最前面的窗口
    print("start to try")
    windows = Desktop(backend="uia").windows()
    top_window = None
    three_star_txt = None
    # 打印每个窗口的标题和控件信息
    for window in windows:
        if debug == 1: print(f"窗口标题: {window.window_text()}")
        if '悟空' in window.window_text():
            for ctrl in window.children():
                if debug == 1: print(f"控件类型: {ctrl.element_info.control_type}, 控件名称: {ctrl.window_text()}")
                if '更新公告' in ctrl.window_text():
                    top_window = ctrl.children()
                    if top_window[0].element_info.control_type == 'Button' and top_window[0].window_text() == '确定' :
                        print(f"found {ctrl.window_text()}, fz need update")
                        top_window[0].click_input()
                        return 'update'

                if ('更新公告' not in ctrl.window_text() or debug == 1) and ctrl.element_info.control_type == 'Window':
                    #print("found the window")
                    #print(f"{ctrl.class_name()}")
                    top_window = ctrl.children()
                    if debug == 1: print(f"top_window 中控件数量: {len(top_window)}")
                    if debug == 1: print(f"child0控件类型: {top_window[0].element_info.control_type}, 控件名称: {top_window[0].window_text()}")
                    for w in top_window:
                        # 获取每个窗口对象的控件类型和窗口文本信息
                        #print(f"child控件类型: {w.element_info.control_type}, 控件名称: {w.window_text()}")
                        if w.element_info.control_type == 'Pane':
                            w = w.children()
                            three_star_txt = w[0].window_text()
                            print(f"合体机文本: {three_star_txt}")
                            #print(f"child d child控件类型: {w[0].element_info.control_type}, 控件名称: {w[0].window_text()}")
                            if '3星' in three_star_txt:
                                return three_star_txt
                            else:
                                print("not found 3 star text, don't know what happened")
    
    if three_star_txt is None:
        print("not found 3 star text")
        return 'not found'
    else:
        return three_star_txt

def is_program_running(program_name):
    # 检查程序是否在运行
    for process in psutil.process_iter(['name']):
        if process.info['name'] == program_name:
            return True
    return False

def is_program_running_pattern(program_name_pattern):
    # 遍历当前所有进程
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # 获取进程名称并检查是否符合模式
            if fnmatch.fnmatch(proc.info['name'], program_name_pattern):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False

def open_program(path):
	##open some program
    print(f"open {path}")
    subprocess.Popen(path)

def click_at(x, y):
    ##click at some spec location
    pyautogui.click(x, y)
    time.sleep(0.9)

def close_program(process_name):
    ##close some program
    #subprocess.call(["taskkill", "/F", "/IM", process_name])
    subprocess.call(["powershell", "-Command", f"Stop-Process -Name '{process_name}' -Force"])

def open_browser(url):
    ##open spec web on browser
    webbrowser.open(url)
    time.sleep(3)  ##wait it

def type_in_browser(text):
    ##type in text on some window
    pyautogui.write(text)
    pyautogui.press('enter')
    
def show_success_message():
    ##show a message box
    root = tk.Tk()
    root.withdraw()  #hide main window
    messagebox.showinfo("auto action success", "auto action is all done")
    root.destroy()
#----------------------------------------------------------------------------------------------------------------#
from playwright.sync_api import sync_playwright

def update_fz(fz_path):
    files = os.listdir(fz_path)
    for file in files:
        if debug == 1: print(file)
        if '悟空' in file and 'exe' in file:
            click_at(1960, 1200) #close fz avoid delete failed
            oldfz = file
            oldfz = os.path.join(fz_path, oldfz)
            print(f"delete old {oldfz}")
            os.remove(oldfz)

    print(f"we are going download to {fz_path}")
    final_url = None
    with sync_playwright() as p:
        #browser = p.chromium.launch_persistent_context(#非inprivate模式
        browser = p.chromium.launch(
            #user_data_dir=r"C:\Users\19508\Desktop\封包\工具\data",#非inprivate模式
            executable_path="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
            #headless=False,#出现窗口
            channel="msedge",
            downloads_path=fz_path,   
            #no_viewport=True,#非inprivate模式
            #bypass_csp=True,#非inprivate模式
            #accept_downloads=True,#非inprivate模式
            args=['--start-maximized']
            )

        page = browser.new_page() 
        #page = browser.pages[0]#非inprivate模式
        page.goto("http://www.5kfz.com/#ltnr_download")
        time.sleep(3)
        # 查找元素，使用 CSS 选择器来定位
        buttons = page.query_selector_all('button, a')  # 查找所有 button 和 a 标签
        for button in buttons:
            #print(button.inner_text())  # 打印每个按钮的文本内容
            if '蓝奏' in button.inner_text():
                print("found lan zou button")
                button.click()
                time.sleep(0.5)

            if 'pan' in button.inner_text():
                download_url = button.get_attribute('href')  # 获取下载链接
                print(f"try goto {download_url}")
                page.goto(download_url)#以下载链接开启新的页面
                page.wait_for_selector("button, a")
                time.sleep(3)
                iframe = page.query_selector('iframe.n_downlink')
                inside_thing = iframe.content_frame()
                next_child = inside_thing.content()
                url_pattern = r'href="(https://[^"]+)"'
                target = re.search(url_pattern, next_child)
                final_url = target.group(1)
                #print(f"new page {iframe}  ----------- {inside_thing}----------{next_child}")
                print(f"new page {target.group(1)}")
                with page.expect_download() as download_info:
                    try:
                        page.goto(final_url)
                    except:
                        pass
                
                download = download_info.value
                download.save_as(f"{fz_path}/{download.suggested_filename}")
                print(f"download success {download.suggested_filename}")
                download.delete()
                break

    print(f"end")

def finish_open_fz():
    directory = personal_path
    qq_path = r"C:\Program Files\Tencent\QQNT\QQ.exe"
    if not is_program_running("QQ.exe"):
        open_program(qq_path)
        print(f"自动启动QQ, 便于辅助登录")
        time.sleep(10)
    else:
        print("QQ Already running, don't reopen.")

    files = os.listdir(directory)
    for file in files:
        if debug == 1: print(file)
        if '悟空' in file and 'exe' in file:
            target_fz = os.path.join(directory, file)
            open_program(target_fz)
            break
    #open_program(path)
    time.sleep(70)      #开辅助后的启动时间
    click_at(1450,956)  #规避辅助更新导致的可能提示框
    click_at(1440,972)  #规避辅助更新导致的可能提示框2
    click_at(1438,988)  #规避辅助更新导致的可能提示框3
    result = test_get_top_window_txt()
    if result == 'update':
        update_fz(directory)
        finish_open_fz()
    else:
        click_at(1960,1093)  #click start
        time.sleep(15)
        click_at(1364,375)  #click qq account
        time.sleep(15)
        click_at(1282,454)  #click 7 server 空海
        time.sleep(25)

def finish_plant_and_set_new_plant():
    print(f"收菜和种菜")
    click_at(967,1338)  #pick 日常活动
    time.sleep(1)
    click_at(673,1375)  #pick 庄园助手
    click_at(501,1409)  #选中 满菜自动出售
    click_at(521,1474)  #选中 玩家庄园O
    click_at(1668,1498)  #打开选菜栏
    #for _ in range(4):
    #    click_at(1674,1334)  #滚动四页
    for _ in range(7):
        click_at(1676,1413)  #滚动7页
    
    ##click_at(1527,1096)  #爱心豆豆的等级满了
    ##click_at(1527,1325)  #珊瑚海马等级满了
    click_at(1566,1437)  #选中桑葚
    click_at(1772,1501)  #最后开始
    time.sleep(16)       #16个田，休眠16秒
    time.sleep(10)

def carry_want_pets(name):
    select_pos = (0, 0)
    pick_pos = (0, 0)
    if name in pets:
        select_pos = pets[name]["携带坐标"] #带宠物方案坐标
        pick_pos = pets[name]["打法坐标"] #默认打法坐标
        print(f"carry {name}")
    else:
        print(f"{name} is not availible choise, return")
        return

    click_at(649,1327)  #pick 宠物专区
    click_at(1725,1372)  #pick 本地精灵仓库
    click_at(2119,1439)  #打开 宠物方案栏
    click_at(*select_pos)  #选中 带对应的宠物      
    click_at(2098,1500)  #点击 携带
    time.sleep(1)
    if '灵犬' not in name:
        click_at(1278,1324)     #选中活动专区
        click_at(670,1448)     #打开 活动打法的选择栏
        click_at(*pick_pos)     #pick 对应的打法
        time.sleep(3)

def get_most_tiny_things():
    print(f"完成一些乱七八糟的小事情，比如说刷蓝萃")
    click_at(649,1327)      #pick 宠物专区
    click_at(1725,1372)     #pick 本地精灵仓库

    click_at(2119,1439)     #
    click_at(1881,1472)     #
    click_at(2098,1500)     #选中蓝色精粹队伍，并携带，前面两个点击的具体含义忘了
    
    click_at(1278,1324)     #选中活动专区
    click_at(941,1413)      #选中日常
    pyautogui.doubleClick(949,1480)  #双击 破茧重生
    time.sleep(15)       #5次打怪机会，休眠10秒
    pyautogui.doubleClick(1155,1541)  #双击 乐园探险
    time.sleep(10)          #休眠10秒
    click_at(971,1331)      #选中 日常活动
    click_at(992,1369)      #选中 其他
    click_at(646,1407)      #选中 扭蛋机
    click_at(1188,1477)      #选中 其他
    time.sleep(90)          #30个游戏币，每个等3秒
    click_at(538,1369)      #选中 取物助手
    click_at(1164,1475)      #取消可可树，看是否保留猜箱子的机会
    click_at(1164,1511)      #取消海底挖宝
    click_at(1334,1453)      #勾选 结束不去大剧院
    click_at(1336,1508)      #勾选 后台跳图
    click_at(1542,1419)      #开始取物
    time.sleep(200)          #取物较久，多等会

def try_to_finish_mix_machine(text):
    print(f"尝试完成合体机")
    need_pet = None
    time.sleep(1)
    click_at(1550,918)  #先关闭合体机窗口，方便可能要做的换宠物操作
    time.sleep(0.5)
    if '机械' in text or '冰' in text:
        need_pet = '立冬'
    elif '武' in text or '恶魔' in text:
        need_pet = '魔武'
    elif '龙' in text:
        need_pet = '龙王'
    elif '水' in text:
        need_pet = '碧水'
    elif '虫' in text:
        need_pet = '虫王'
    elif '翼' in text:
        need_pet = '苍羽'
    else:
        print(f"{text} this we can't handle yet")
        click_at(1278,1324)  #选中活动专区
        return need_pet
    
    carry_want_pets(need_pet)
    pyautogui.doubleClick(743,1507)      #再打开合体机
    time.sleep(2)
    
    #click_at(1302,843)  #一星
    #click_at(1302,860)  #二星
    for i in range(3): #打三次
        print("normal start fight")
        click_at(1302,879)  #三星
        click_at(1486,920)  #点击确认
        time.sleep(20)
        if '3星' not in test_get_top_window_txt() and i != 2:
            print("fight fail try again")
            pyautogui.doubleClick(743,1507)      #再打开合体机
            time.sleep(2)
            click_at(1302,879)  #三星
            click_at(1486,920)  #点击确认
            time.sleep(20)
    
    return need_pet

def try_to_finish_seven(last_pet):
    if last_pet != '魔武':
        carry_want_pets('魔武')    
    click_at(930,1400)  #选中活动专区的日常
    print(f"start 勇者训练馆")
    pyautogui.doubleClick(743,1450)      #开始勇者训练馆
    time.sleep(30)
    for count in range(3):
        print(f"try 暗黑远征军 {count+1}")
        pyautogui.doubleClick(950,1450)      #暗黑远征军容易失败，重试3次
        time.sleep(35)
    click_at(1111,1400)  #选中 活动专区的七曜圣地
    click_at(923,1476)  #点击难度选择条
    click_at(911,1560)  #选择困难
    click_at(1081,1471) #点击七曜打法选择条
    click_at(*pets["魔武"]["七曜打法坐标"])
    for count in range(3):   #七曜偶尔也会失败，重试3次
        print(f"try 七曜 {count+1}")
        click_at(1180,1460) #开始
        time.sleep(36)
    return '魔武'

def try_to_finish_newest_activity():
    #这是尝试完哨兵阴阴，已经停留在了活动专区
    time.sleep(1)
    click_at(1008,1405)      #选中 活动专区里的常驻
    pyautogui.doubleClick(743,1507)      #点开合体机
    time.sleep(1)
    last_pet = try_to_finish_mix_machine(test_get_top_window_txt()) #做合体机相关操作

    last_pet = try_to_finish_seven(last_pet)
    click_at(1008,1405)      #选中 活动专区里的常驻

    click_at(1530,1516)      #下滑三次
    click_at(1530,1516)      #下滑三次
    click_at(1530,1516)      #下滑三次
    print("start to do old vip pet activity")
    pyautogui.doubleClick(950,1480)      #机械圣殿
    time.sleep(25)
    click_at(1530,1516)      #下滑两次
    click_at(1530,1516)      #下滑两次
    pyautogui.doubleClick(740,1453)      #火焰圣殿
    time.sleep(25)
    #pyautogui.doubleClick(740,1520)      #虫子圣殿，虫子已经刷到极品了，不用再打
    #time.sleep(25)

    print(f"try newest activity start {time.strftime('%H:%M:%S', time.localtime())}")
    click_at(851,1405)      #选中 活动专区里的热门
    # 分别是热门活动里九个最新的活动坐标
    coordinates = [
        (742, 1450), (948, 1450), (1156, 1450),
        (742, 1480), (948, 1480), (1156, 1480),
        (742, 1514), (948, 1514), (1156, 1514)
    ]
    # 循环执行双击操作
    for coord in coordinates:
        pyautogui.doubleClick(coord[0], coord[1])  # 双击指定坐标
        time.sleep(42)

def first_month_challege_star_tower():
    print(f"星辰塔 start {time.strftime('%H:%M:%S', time.localtime())}")
    carry_want_pets('青琼灵犬')
    click_at(1513,1325)  #click star tower
    time.sleep(1)
    click_at(1135,1529)  #click 扫荡
    time.sleep(2)
    click_at(1303,901)  #pick level 6
    time.sleep(0.5)
    click_at(1300,918)  #pick level 7
    time.sleep(0.5)
    click_at(1473,955)  #click 确定  
    time.sleep(5)
    click_at(1047,1374)  #click 8 level
    time.sleep(1)
    #这里默认就是狗子打法，所以不用选中打法
    click_at(644,1522)  #选中次数框
    pyautogui.typewrite('30') #输入 尝试30次
    click_at(706,1521)  #不去大剧院
    click_at(1027,1523)  #click 挑战
    time.sleep(60)      #每次尝试给2秒吧
    click_at(885,1524)  #click stop fight
    time.sleep(10)

def play_little_game_and_hang_out():
    print(f"小游戏挂机流程 start {time.strftime('%H:%M:%S', time.localtime())}")
    time.sleep(5)
    pyautogui.keyDown('alt')
    pyautogui.press('f4')
    pyautogui.keyUp('alt')
    time.sleep(19)
    
    program_name = r"悟空神辅II*.exe"
    if is_program_running_pattern(program_name):
        print("we are normal status")
        click_at(1505,153)     #挂机小游戏之前重新选服，避免某些新活动卡住不能正常进小游戏
        time.sleep(10)
        click_at(1364,375)  #click qq account
        time.sleep(15)
        click_at(1282,454)  #click 7 server 空海
        time.sleep(3)
    else:
        print("we are not struck, but we closed fz")
        program_path = r"C:\Users\19508\Desktop\封包\find_fz_and_run.bat"  ## find newest fz and open it
        finish_open_fz(program_path)
    
    # just solve hang out use out of roco time problem #
    time.sleep(6)
    click_at(852,1336)     #选中人物专区
    click_at(669,1367)     #选中小游戏助手
    click_at(880,1444)     #打开选择栏箭头
    for _ in range(2):
        click_at(873,1636)  #向下滚动两页

    click_at(678,1654)     #选魔法账簿
    pyautogui.doubleClick(1094,1450)  #选中每次消耗时间框
    pyautogui.typewrite('10') #输入 10s
    click_at(1517,1459)     #start little game

def daily_uxlink_job():
    # do air drop task
    if is_program_running("QQ.exe"):
        print("kill the qq")
        close_program("QQ")
    
    #open_program(r"C:\Users\19508\Desktop\墙\v2rayN-With-Core\v2rayN.exe")
    open_program(r"D:\clash\Clash Verge.exe")
    time.sleep(7)
    open_browser("https://dapp.uxlink.io/discover/detail?id=1779158074653667329")  #change as u need
    time.sleep(7)
    click_at(1562,613) # pick [check in]
    time.sleep(7)

    click_at(1791,1039) # click [passwd]
    pyautogui.typewrite("qwertyasdfg123")  #change as u need
    click_at(1442,1265) # click [check in]
    time.sleep(10)
    if is_program_running("Clash Verge.exe"):
        print("kill the magic")
        close_program("Clash Verge")
        time.sleep(3)
    click_at(2644,24) # 把浏览器最小化

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
original_text = r'体重在'
def capture_and_ocr_region(x, y, width, height):
    """
    截取指定区域并使用 OCR 提取文本。
    参数:
        x, y: 目标区域左上角坐标
        width, height: 目标区域的宽度和高度
    返回:
        str: OCR 提取的文本
    """
    # 截取指定区域
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save("target_screenshot.png")

    image = Image.open("target_screenshot.png")
    text = pytesseract.image_to_string(image, lang='chi_sim', config='--psm 6')
    global original_text
    original_text = text
    print(f"最开始提取的文本:{text}")
    print(f"保存最开始提取的文本:{original_text}")

    # 放大图像
    scale_factor = 10
    new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
    image = image.resize(new_size, Image.Resampling.LANCZOS)  # 使用高质量插值
    #text = pytesseract.image_to_string(image, lang='chi_sim', config='--psm 6')
    #print(f"\n 放大提取的文本:{text}") 

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)  # 提高对比度（可调整参数）
    #text = pytesseract.image_to_string(image, lang='chi_sim', config='--psm 6')
    #print(f"\n 对比度提取的文本:{text}") 

    '''# 锐化图像
    image = image.filter(ImageFilter.SHARPEN)
    text = pytesseract.image_to_string(image, lang='chi_sim', config='--psm 6')
    print(f"\n 锐化提取的文本:{text}")'''

    image = image.filter(ImageFilter.GaussianBlur(radius=0.3)) # 应用高斯模糊减少噪声
    #text = pytesseract.image_to_string(image, lang='chi_sim', config='--psm 6')
    #print(f"\n 高斯提取的文本:{text}")

    # 转换为灰度图像
    image = image.convert('L')
    #text = pytesseract.image_to_string(image, lang='chi_sim', config='--psm 6')
    #print(f"\n 灰度提取的文本:{text}") 

    # 二值化（阈值处理），突出文本
    threshold = 160  # 阈值（可调整，0-255）
    image = image.point(lambda p: 255 if p > threshold else 0)
    #text = pytesseract.image_to_string(image, lang='chi_sim', config='--psm 6')
    #print(f"\n 二值化提取的文本:{text}") 
    
    '''image = Image.eval(image, lambda p: 255 - p)
    text = pytesseract.image_to_string(image, lang='chi_sim', config='--psm 6')
    print(f"\n 反转提取的文本:{text}") '''
    
    # 保存处理后的图像（用于调试）
    image.save("processed_screenshot.png")

    text = pytesseract.image_to_string(image, lang='chi_sim', config='--psm 6')
    print(f"处理后提取的文本:{text}") 
    return text  

def try_to_challenge_the_green_chicken():
    print(f"尝试哨兵阴阴============================== {time.strftime('%H:%M:%S', time.localtime())}")
    carry_want_pets('龙王')
    try_times = 50
    click_at(1278,1324)     #选中活动专区
    click_at(1247,1411)  #选中 哨兵阴阴框
    click_at(898,1460)  #选中 打法栏
    click_at(*pets["龙王"]["哨兵打法坐标"])  #选中 龙王打法
    click_at(1056,1472)  #选中次数框
    pyautogui.typewrite(str(try_times)) #输入 尝试次
    click_at(1213,1481)  #点击 挑战
    time.sleep(3)      
    ocr_text = capture_and_ocr_region(1287, 800, 300, 15)#尝试获取挑战条件
    use_pet = '龙王'
    pets_list = None
    if '身高' in ocr_text:
        value_matches = re.findall(r'\d+\.\d+|\d+', ocr_text)
        value_matches[0] = float(value_matches[0])
        print(f"身高模式:{ocr_text} 尝试获取数值 {value_matches[0]}")
        if '以下' in ocr_text:
            pets_list = {name: info for name, info in pets.items() if info["身高"] < value_matches[0]}
            for name, info in pets_list.items():
                print(f"小于的有 {name}")
                if '冰' in info["属性"] or '机械' in info["属性"] or '武' in info["属性"] or '水' in info["属性"]:
                    use_pet = name
                    break
        elif '以上' in ocr_text:
            pets_list = {name: info for name, info in pets.items() if info["身高"] > value_matches[0]}
            for name, info in pets_list.items():
                print(f"大于的有 {name}")
                if '冰' in info["属性"] or '机械' in info["属性"] or '武' in info["属性"] or '水' in info["属性"]:
                    use_pet = name
                    break
        elif '围内' in ocr_text:
            value_matches[1] = float(value_matches[1])
            pets_list = {name: info for name, info in pets.items() if info["身高"] > value_matches[0] and info["身高"] < value_matches[1]}
            for name, info in pets_list.items():
                print(f"大于{value_matches[0]} 且小于 {value_matches[1]} 的有 {name}")
                if '冰' in info["属性"] or '机械' in info["属性"] or '武' in info["属性"] or '水' in info["属性"]:
                    use_pet = name
                    break
        
        if use_pet == '龙王' and pets_list != None:
                use_pet = next(iter(pets_list.items()))[0]  # 获取字典的第一项的名字
    elif '体重' in ocr_text:
        if '内' not in ocr_text:
            ocr_text = original_text
        value_matches = re.findall(r'\d+\.\d+|\d+', ocr_text)
        if value_matches:
            value_matches[0] = float(value_matches[0])
            print(f"体重模式:{ocr_text} 尝试获取数值 {value_matches[0]}")
        else:
            print(f"value_matches 列表为空")
        if '以下' in ocr_text:
            pets_list = {name: info for name, info in pets.items() if info["体重"] < value_matches[0]}
            for name, info in pets_list.items():
                print(f"小于的有 {name}")
                if '冰' in info["属性"] or '机械' in info["属性"] or '武' in info["属性"] or '水' in info["属性"]:
                    use_pet = name
                    break
        elif '以上' in ocr_text:
            pets_list = {name: info for name, info in pets.items() if info["体重"] > value_matches[0]}
            for name, info in pets_list.items():
                print(f"大于的有 {name}")
                if '冰' in info["属性"] or '机械' in info["属性"] or '武' in info["属性"] or '水' in info["属性"]:
                    use_pet = name
                    break
        elif '内' in ocr_text:
            value_matches[1] = float(value_matches[1])
            pets_list = {name: info for name, info in pets.items() if info["体重"] > value_matches[0] and info["体重"] < value_matches[1]}
            for name, info in pets_list.items():
                print(f"大于{value_matches[0]} 且小于 {value_matches[1]} 的有 {name}")
                if '冰' in info["属性"] or '机械' in info["属性"] or '武' in info["属性"] or '水' in info["属性"]:
                    use_pet = name
                    break

        if use_pet == '龙王' and pets_list != None:
            use_pet = next(iter(pets_list.items()))[0]  # 获取字典的第一项的名字
    elif '回合' in ocr_text:
        value_matches = re.findall(r'\d+\.\d+|\d+', ocr_text)
        value_matches[0] = float(value_matches[0])
        print(f"回合模式:{ocr_text} 尝试获取数值 {value_matches[0]}")
        use_pet = '立冬'
    elif '雄' in ocr_text or '雌' in ocr_text:
        print(f"性别模式:{ocr_text} ")
        if '雄' in ocr_text:
            use_pet = '魔武'
        else:
            use_pet = '立冬'
    else:
        print(f"\n 其他模式:{ocr_text}") 
        if '冰' in ocr_text or '机' in ocr_text:
            use_pet = '立冬'
        elif '武' in ocr_text or '魔' in ocr_text:
            use_pet = '魔武'
        elif '龙' in ocr_text:
            use_pet = '龙王'
        elif '水' in ocr_text:
            use_pet = '碧水'
        elif '虫' in ocr_text:
            use_pet = '虫王'
        elif '翼' in ocr_text:
            use_pet = '苍羽'
    
    if use_pet != '龙王':
        click_at(1560,950)  #关闭选择框便于换宠物
        print(f"changed to use this pet:{use_pet} ")
        carry_want_pets(use_pet)
        click_at(1278,1324)     #选中活动专区
        click_at(1247,1411)  #选中 哨兵阴阴框
        click_at(898,1460)  #选中 打法栏
        click_at(*pets[use_pet]["哨兵打法坐标"])  #对应的打法
        click_at(1056,1472)  #选中次数框
        pyautogui.typewrite(str(try_times)) #输入 尝试次
        click_at(1213,1481)  #点击 挑战
    time.sleep(2)

    if use_pet == '虫王':
        try_times = 2*try_times
    click_at(1485,947)  #确定挑战 第1个怪
    time.sleep(try_times)      #由于最大49次
    #第1个和第2个，确定按钮位置没有太大变化，坐标沿用
    click_at(1485,947)  #确定挑战 第2个怪 
    time.sleep(try_times)
    #第3，4，5个的确定按钮位置也没有太大变化，坐标沿用
    click_at(1476,922)  #确定挑战 第3个怪 
    time.sleep(try_times)
    click_at(1476,922)  #确定挑战 第4个怪 
    time.sleep(try_times)
    click_at(1476,922)  #确定挑战 第5个怪 
    time.sleep(try_times)
    print(f"尝试哨兵阴阴结束============================== {time.strftime('%H:%M:%S', time.localtime())}")

# 所有可选的函数
functions = [finish_open_fz, finish_plant_and_set_new_plant, get_most_tiny_things, first_month_challege_star_tower, 
             try_to_challenge_the_green_chicken, try_to_finish_newest_activity, play_little_game_and_hang_out, show_success_message]

# 函数名的对应文本
function_names = [
    "打开辅助的全部准备", "收菜+种上特定的菜", "打蓝萃以及在王国取物", "灵犬扫荡以及挑战星辰塔", 
    "智能打哨兵阴阴(可能打不过田鸡)", "七曜暗黑城勇者馆合体机+尝试新闻活动", "结尾小游戏挂机", "结束提醒"
]

selected_functions = []
def on_ok():
    # 检查哪些选项被选中
    for i, var in enumerate(vars):
        if var.get() == 1:
            selected_functions.append(functions[i])
    # 提示框
    root.destroy()
def on_cancel():# 取消按钮的回调函数
    root.destroy()
def select_all():# 全选按钮的回调函数
    for var in vars:
        var.set(1)
def deselect_all():# 反选按钮的回调函数
    for var in vars:
        var.set(0)

root = tk.Tk()
# 创建勾选框变量
vars = [tk.IntVar(value=1) for _ in range(8)]  # 8个选项，默认全选
def info_box():
    root.title("选择本次执行的流程")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # 设置窗口宽高
    window_width = 550
    window_height = 600
    # 计算窗口位置：居中显示
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')# 设置窗口位置
    # 创建勾选框
    for i in range(8):
        checkbox = tk.Checkbutton(root, text=function_names[i], variable=vars[i])
        checkbox.pack(anchor='w', padx=20, pady=4)# 使用 'w' 使勾选框靠左对齐
    # 创建按钮
    button_select_all = tk.Button(root, text="全选", command=select_all)
    button_deselect_all = tk.Button(root, text="反选", command=deselect_all)
    button_ok = tk.Button(root, text="确定", command=on_ok)
    button_cancel = tk.Button(root, text="取消", command=on_cancel)
    # 布局按钮
    button_select_all.pack(side="left", padx=20)
    button_deselect_all.pack(side="left", padx=20)
    button_ok.pack(side="left", padx=20)
    button_cancel.pack(side="left", padx=20)
    root.mainloop()

def main():
    #time.sleep(6)
    #ocr_text = capture_and_ocr_region(1287, 800, 300, 15) 
    info_box()#创建选择窗口
    if selected_functions and selected_functions[0] != finish_open_fz:
        print(f"\n 请确保已经是前面流程的最终状态")
        time.sleep(1)
        click_at(1400, 1580)

    for func in selected_functions:
        func()# 执行选中的函数
        print(f"{func} is selected")
    exit()
    #--------0 doing something may get u rich
    #daily_uxlink_job()
    #--------1 open
    finish_open_fz()
    #--------2 收菜并种上自己想种的菜
    finish_plant_and_set_new_plant()
    #--------3 蓝色精粹、获取游戏币、取物助手取各种灵石
    get_most_tiny_things()
    #--------4 尝试狗子打法自动打第八层以及扫荡，减少每月刷新星辰塔的时间消耗
    first_month_challege_star_tower()
    #--------5 尝试一下打哨兵
    try_to_challenge_the_green_chicken()
    #--------6 打暗黑城，勇者训练馆，合体机，七曜圣地，以及尝试最新的新闻活动(能成功就赚了，不成功也没事)
    try_to_finish_newest_activity()
    #--------7 尝试完所有的东西之后，放到小游戏挂机，避免手动检查时，因为在线时间太长而被无法战斗
    play_little_game_and_hang_out()
    #open_browser("http://www.baidu.com")  #change as u need
    #--------8 show success msg
    show_success_message()

if __name__ == "__main__":
    main()

