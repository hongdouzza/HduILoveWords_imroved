import pyautogui
import time

AnswerPlaces = ['A', 'B', 'C', 'D', 'SKIP']
XandY = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

pyautogui.FAILSAFE = True
width, height = pyautogui.size()
print(f'屏幕宽度为{width},高度为{height}')

for i in range(len(AnswerPlaces)):
    print(f'[+] 请在两秒内将鼠标移动到 选项{AnswerPlaces[i]} 的位置')
    time.sleep(2)
    XandY[i][0], XandY[i][1] = pyautogui.position()

# 输出鼠标当前位置
for i in range(len(AnswerPlaces)):
    print('各选项坐标如下:')
    print(f"{AnswerPlaces[i]}: ({XandY[i][0]}, {XandY[i][1]})")
