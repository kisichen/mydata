import os,openpyxl
codetext = open('e:\\temp\\jdcode.txt','r')
wb = openpyxl.Workbook()
sheet = wb.get_sheet_by_name('Sheet')
x = 1#初始化行
y = 1#初始化列
while True:
     line = codetext.readline()#逐行读取
     if not line:#没有文件时退出
          break
     for i in line.split():#以空格为单位分别读取每个
          item=i.strip()#去掉头尾空格
          sheet.cell(row=x,column=y).value=item
          y +=1#行固定，分别进行列写
     x += 1
     y=1#初始化列
codetext.close()
wb.save('e:\\temp\\aaa.xlsx')
