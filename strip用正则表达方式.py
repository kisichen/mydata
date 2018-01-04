import re
a = input("请输入一个需要修改的字符串:")
b = input("请输入需要修改的字符")
def changword(before,change):
    if change == '':
        print('您输入的是一个空字符，下面将默认删除行首及行尾空白字符')
        b="^\s+|\s+$"
        blank = re.compile(r'%s'%b)
        after=blank.sub('',before)
        print('删除行首行尾空白字符后为:'+after)
    else :
        print('下面将开始替换操作')
        b=change
        blank = re.compile(r'%s'%b)
        after=blank.sub('',before)
        print('修改完后的字符:'+after)

changword(a,b)

