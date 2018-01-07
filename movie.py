import pandas as pd
mvpath = 'E:\\temp\\pydata-book-2nd-edition\\datasets\\movielens\\'
unames = ['user_id','gender','age','occupation','zip']#定义用户标题
#分隔符为:: 头为空，标题为unames中定义的字段
users = pd.read_table((mvpath+'users.dat'),sep='::',header=None,names=unames)
#定义打分用户及电影ID标题
rnames = ['user_id','movie_id','rating','timestamp']
#打开数据文件，以::为分隔符，表头为rnames定义的字段
ratings = pd.read_table((mvpath+'ratings.dat'),sep='::',header=None,names=rnames)
#定义电影头标题
mnames = ['movie_id','title','genres']
#打开电影数据文件，以::为分隔符，表头为mnames
movies = pd.read_table((mvpath+'movies.dat'),sep='::',header=None,names=mnames)
#将三个数据整合，使用pd.merge函数
data = pd.merge(pd.merge(ratings,users),movies)
#以rating电影评份（为平均分），行为电影名称，列为性别
mean_ratings = data.pivot_table('rating','title','gender',aggfunc='mean')
#以data数据中按title分组，计算得出ratings_by_title分组求和
ratings_by_title = data.groupby('title').size()
#按分组求和后的数据进行排序，排序的条件为大于 250的电影
active_titles = ratings_by_title.index[ratings_by_title >= 250]
#根据active_titles中大于250的评分的电影，再筛选出mean_ratings中大于250条件电影男女评分
mean_ratings = mean_ratings.loc[active_titles]
#查看新附值后的数据
mean_ratings
#按照女性平均数据进行降序排序
top_female_ratings = mean_ratings.sort_values(by='F',ascending=False)
#显示头10条数据
top_female_ratings[:10]
#添加一个新的diff列，数据为男性比女性平均评分多数据
mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
#按diff列进行序列，得到的数据为女性观众最为喜爱的电影
sort_by_diff = mean_ratings.sort_index(by='diff')
sort_by_diff[:15]#显示前15行数据
sort_by_diff[::-1][:15]#查看反序后15行
#根据电影名称分组的得分数据的标准差
ratings_std_by_title = data.groupby('title')['rating'].std()

#根据active_titles进行过滤
rating_std_by_title = ratings_std_by_title.loc[active_titles]
#根据值对series进行降序排列
ratings_std_by_title.sort_values(ascending=False)[:10]
