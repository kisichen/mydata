import pyautogui,time
time.sleep(5)
pyautogui.click()
distance = 500
while distance > 0:
    pyautogui.dragRel(distance,0,duration=0.01)#画出右边的线
    distance -= 5
    pyautogui.dragRel(0,distance,duration= 0.01)#鼠标下移
    distance -= 5
    pyautogui.dragRel(-distance,0,duration = 0.01)#鼠标左移
    distance -= 5
    pyautogui.dragRel(0,-distance,duration = 0.01)#鼠标上移