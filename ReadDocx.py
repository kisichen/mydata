import os,docx
def getText(filename):
    if os.path.exists(filename):
        doc = docx.Document(filename)
        fulltext = []
        for detail in doc.paragraphs:
            fulltext.append(detail.text)
        return '\n'.join(fulltext)
        a='\n'.join(fulltext)
    else:break
        print('输入的文件找不到,请重新输入')
       
a = input('请输入全路径及文件名（.doc）')
if a =='':
    print('请不要为空值，重新运行程序输入')
else:
    getText(a)
    list = getText('e:\\1.docx')
    print(list)