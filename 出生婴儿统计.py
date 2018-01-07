import pandas as pd
path = 'E:\\temp\\pydata-book-2nd-edition\\datasets\\babynames\\'
columns=['name','sex','births']#定义表头
#定义该目录下的年份字段
years = range(1980,2011)
pieces = []
#开始循环，打开该目录下的所有文件
for year in years:
    nowpath = path + 'yob%d.txt' % year
    frame = pd.read_csv(nowpath,names=columns)
    #添加一个列为year，值为当前的年份year值
    frame['year'] = year
    pieces.append(frame)
#将所有数据整合到单个DataFrame中,ignore_index=True是去掉原始的行号
names = pd.concat(pieces,ignore_index=True)
#利用pivot_table在year和sex级别上对其进行聚合，以year为组，以性别统计年龄求合
total_births = names.pivot_table('births',index='year',columns='sex',aggfunc='sum')
#查看聚合后的，后面几行数据
total_births.tail()
#以图形的方式显示
total_births.plot(title='按年统计性别的所有生日和')

#插入一个prop列，用于存放指定名字的婴儿数相对于总出生数的比例
#值为0.02就是相当于100名婴儿就2名取了这个名字，按year和sex分组，再将新的列加到各个分组上
def add_prop(group):
    #整数除法会向下圆整
    #births是整数，所以必须在计算分式时转换成浮点数，如果使用python3则不需要
    births = group.births.astype(float)
    group['prop'] = births / births.sum()
    return group
names = names.groupby(['year','sex']).apply(add_prop)
#执行分组后，作为有效性检查，检查是否所有的prop列相加为1，因数是浮点型，所以使用
#np.allclose醚检查这个分组的和是否接近1
np.allclose(names.groupby(['year','sex']).prop.sum(),1)

#取出按年份，性别分组的头1000名婴儿
def get_top_1000(group):
    return group.sort_index(by='births',ascending=False)[:1000]
grouped = names.groupby(['year','sex'])
top1000 = grouped.apply(get_top_1000)

#这是另一种方法
pieces = []
for year,group in names.groupby(['year','sex']):
    pieces.append(group.sort_index(by='births',ascending=False)[:1000])
top1000 = pd.concat(pieces,ignore_index=True)
#对男女分别保存
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']
#按姓名进行分组，按年进行排序，对births进行求和统计
totail_births = top1000.pivot_table('births',index='year',columns='name',aggfunc=sum)
#提取姓名为下列的几个人的数据保存到subset中
subset = totail_births[['John','Harry','Mary','Marilyn']]
#将统计的信息制图
subset.plot(subplots=True,figsize=(12,10),grid=False,title='每年出生婴儿按姓名统计')
#输出到图片信息
table.plot(title='1000名按姓别年份统计',yticks=np.linspace(0,1.2,13),xticks=range(1980,2020,10))
