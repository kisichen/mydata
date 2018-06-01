import cx_Oracle,os,numpy,copy
import sys,datetime
import xlwt,xlrd,time
import pandas as pd
#passwd = input('请输入密码:')
#if passwd == 'createby_chenpeng':
to_day = datetime.date.today()
last_year = to_day - datetime.timedelta(days=364)
print('该脚本由cp制作，如有数据发生不匹配，请邮件联系diablocp81@gmail.com')
print('数据正在生成中...请等待！')
firsttime = time.time()
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.WE8ISO8859P1'
path='D:\\每日百货销售\\'
if not os.path.exists(path):
    os.mkdir(path)
os.chdir(path)
tital = ['店号','当前日期','当前收入（万）','去年同期','去年收入（万）','同比率']
systime = time.strftime("%Y-%m-%d")
mkt=['204','205','207','208','248','258','278']
password = 'ebiztornado'
for i in mkt:
    user = 'dbusrmkt'+i
    conn_db = 'm'+i+'_db'
    db = cx_Oracle.connect(user,password,conn_db)
    data = db.cursor()
    sql = """select aa.sglmarket mkt,aa.sgldate,round((aa.xssr/10000),2) sr,bb.sgldate,round((bb.xssr/10000),2) sr,round(((aa.xssr-bb.xssr)/bb.xssr),2)*100||'%' tongbi from (select sglmarket,sgldate,sum(sglxssr) xssr
            from salegoodslist where sgldate = to_date(to_char(sysdate,'yyyymmdd'),'yyyymmdd')
            group by sgldate,sglmarket) aa
            ,
            (select sgldate,sum(sglxssr) xssr
            from salegoodslist where sgldate = to_date(to_char(sysdate-364,'yyyymmdd'),'yyyymmdd')
            group by sgldate) bb"""
    locals()['cxdata'+i] = pd.read_sql(sql,db)
    data.close()

dbxn = cx_Oracle.connect('dbusrmkt248','ebiztornado','m248_db',encoding='utf-8')
dataxn = dbxn.cursor()
sqlxn = """select aa.louchen mkt,aa.sgldate,round((aa.xssr/10000),2) sr,bb.sgldate,round((bb.xssr/10000),2) sr,round(((aa.xssr-bb.xssr)/bb.xssr),2)*100||'%' tongbi  from (select sgldate,case when sglmfid > 00482100 and sglmfid < 00482200 then '1'
              when sglmfid > 00482200 and sglmfid < 00482300 then '2'
              when sglmfid > 00482300 and sglmfid < 00482400 then '3'
              when sglmfid > 00482400 and sglmfid < 00482500 then '4'
              when sglmfid > 00482500 then '5'
 else null end as louchen,
sum(sglxssr) xssr
from salegoodslist where sgldate = to_date(to_char(sysdate,'yyyymmdd'),'yyyymmdd')
group by case when sglmfid > 00482100 and sglmfid < 00482200 then '1'
              when sglmfid > 00482200 and sglmfid < 00482300 then '2'
              when sglmfid > 00482300 and sglmfid < 00482400 then '3'
              when sglmfid > 00482400 and sglmfid < 00482500 then '4'
              when sglmfid > 00482500 then '5'
 else null end,sgldate
union 
select sgldate,replace(sglmfid,'00482103','hj') louchen,sum(sglxssr) xssr from salegoodslist where sglmfid = 00482103 and sgldate = to_date(to_char(sysdate,'yyyymmdd'),'yyyymmdd')
group by sglmfid,sgldate) aa,

(select sgldate,case when sglmfid > 00482100 and sglmfid < 00482200 then '1'
              when sglmfid > 00482200 and sglmfid < 00482300 then '2'
              when sglmfid > 00482300 and sglmfid < 00482400 then '3'
              when sglmfid > 00482400 and sglmfid < 00482500 then '4'
              when sglmfid > 00482500 then '5'
 else null end as louchen,
sum(sglxssr) xssr
from salegoodslist where sgldate = to_date(to_char(sysdate-364,'yyyymmdd'),'yyyymmdd')
group by case when sglmfid > 00482100 and sglmfid < 00482200 then '1'
              when sglmfid > 00482200 and sglmfid < 00482300 then '2'
              when sglmfid > 00482300 and sglmfid < 00482400 then '3'
              when sglmfid > 00482400 and sglmfid < 00482500 then '4'
              when sglmfid > 00482500 then '5'
 else null end,sgldate
union 
select sgldate,replace(sglmfid,'00482103','hj') louchen,sum(sglxssr) xssr from salegoodslist where sglmfid = 00482103 and sgldate = to_date(to_char(sysdate-364,'yyyymmdd'),'yyyymmdd')
group by sglmfid,sgldate) bb
where aa.louchen = bb.louchen"""
xndata = pd.read_sql(sqlxn,dbxn)
dataxn.close()

aa = {'0000':'配送中心','0001':'徐东平价店','0005':'沙市中商百货','0003':'小东门店','0002':'中南商都店','0006':'中南商业大楼','0008':'荆门中商百货','0016':'雄楚店','0013':'吴家山店','0010':'南湖店','0011':'青山店','0009':'中商平价黄石超市','0028':'中商百货销品茂店','0026':'曙光店','0014':'首义店','0015':'唐家墩店','0012':'三阳店','0017':'大冶店','0038':'中商百货随州店','0043':'中商平价黄石延安路购物广场','0023':'大楼超市','0029':'公安店','0888':'商科工贸','0032':'荆州东门店','0027':'京山店','0030':'光谷店','0033':'潜江店','0018':'信阳店','0019':'岳阳店','0020':'襄樊店','0022':'仙桃店','0025':'中商平价荆门店','0035':'咸宁店','0037':'杨汊湖购物广场','0024':'中商平价沙市店','0039':'中商平价随州店','0045':'中商平价枝江店','0048':'中商百货咸宁店','0049':'黄冈超市','0036':'黄石八卦咀购物广场','0040':'中商平价松滋店','0041':'中商平价庙山购物广场','0042':'中商平价黄石颐阳路店','0044':'中商平价板桥超市','0031':'新洲店','0034':'长丰店','0004':'黄冈中商百货','0078':'中商百货黄石店','0007':'武汉中商百货连锁有限责任公司','0021':'十堰店','0055':'中商平价荆门长宁店','0052':'中商平价鹦鹉洲店','0046':'中商平价杨家湾购物广场','0051':'中商平价东湖超市','0053':'中商平价荆门石化店','0058':'中商百货孝感店','0047':'中商平价珞珈山购物广场','1':'咸宁1楼','2':'咸宁2楼','3':'咸宁3楼','4':'咸宁4楼','5':'咸宁5楼','hj':'咸宁黄金柜'}
bb = pd.DataFrame()
bb['编码']=aa.keys()
bb['门店']=aa.values()
alldata = cxdata248.append([xndata,cxdata204,cxdata207,cxdata205,cxdata208,cxdata258,cxdata278])
alldata.columns=(tital)
cc = pd.merge(alldata,bb,how='inner',left_on='店号',right_on='编码')
dd = copy.deepcopy(cc[['门店','当前日期','当前收入（万）','去年同期','去年收入（万）','同比率']])
dd['去年同期'] = dd['去年同期'].astype('str')
dd['当前日期'] = dd['当前日期'].astype('str')
ab = pd.DataFrame([['中商十堰店','','','','',''],['中商销品茂','','','','','']],columns=['门店', '当前日期', '当前收入（万）', '去年同期', '去年收入（万）', '同比率'])
save1 = dd[:8].append(ab[:1]).append(dd[8:9]).append(ab[1:]).append(dd[9:])


save1.to_excel("%s.xls" %to_day,index=False)
#readxl = xlrd.open_workbook("%s.xls" %today)
#rew = readcp.gets('Sheet1')
#rew.put_cell(rew.nrows,0,1,'中商百货十堰店',xf_index=None)
#rew.put_cell(rew.nrows,0,1,'中商销品茂店',xf_index=None)
#rew.

totalTime=round(time.time()-firsttime,1)

print('生成结束，请在"D:\每日百货销售"目录中查看生成的以%s.xls文件！程序生成时间：%s秒!' % (to_day,totalTime))
os.system('pause')
#else:print ('输入的密码不对！请重新运行程序！')
    
    
    
    
