import time,pyperclip
print('请输入《回车》计时开始，再按下回车将暂停，按ctrl+c程序终止')
input()
print('start')
startTime = time.time()
lastTime = startTime
lapnumber = 1
aa =''
try:
    while True:
        input()
        lastTime = round(time.time() - lastTime,2)
        totalTime = round(time.time() - startTime,2)
        tempa=('Lap #%s:%s (%s)' % (str(lapnumber).ljust(2),str(lastTime).rjust(5)
              ,str(totalTime).rjust(5)))
        print(tempa)
        aa=aa+tempa+'\n'
        lapnumber +=1
        lastTime = time.time()
except KeyboardInterrupt:
    print('\nDone')
    pyperclip.copy(aa)
