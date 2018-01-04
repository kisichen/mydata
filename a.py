import pyautogui,time
print('按Ctrl+c结束')
try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
#        pixeColor = pyautogui.screenshot().getpixel((x,y))
        print(positionStr,end='')
        print('\b' * 20,end='',flush=True)
except KeyboardInterrupt:
    print('\n完成！')