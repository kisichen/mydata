import cx_Oracle,os,numpy,copy
import xlwt,time
import pandas as pd
firsttime = time.time()
sjtital = ['门店ID(必填)','商品SKU编码(必填)','到家价(必填)','市场价(非必填)']
kctital = ['门店编号(必填)','SKU编码','商家商品编号（与SKU编码不能同时为空）','现货库存（必填）']
db = cx_Oracle.connect('dbusrm04/futuremkt@mg08')
data = db.cursor()
sql="""select distinct(gbbarcode),nvl(sl,0) kc,decode(nvl(cx.cxj,zc.sj),null,0,nvl(cx.cxj,zc.sj)) sj from
(select t.gbbarcode,gbid from TEMP_JDBARCODE t,goodsbase w where t.gbbarcode=w.gbbarcode) t,
(select gstgdid,sum(gstkcsl) sl from goodsstock where gstmfid='004701' group by gstgdid) kc, 
(select distinct popgdid,First_value(popsj) OVER (PARTITION BY  popgdid order by popsequece desc) cxj from popcurinfo where popbillno not like '%T%' 
and popksrq<sysdate 
and popjsrq>sysdate-1 
and popkssj<to_char(sysdate,'HH24:mi:ss') 
and popjssj>to_char(sysdate,'HH24:mi:ss') 
and popmfid='004701' 
and popuid='00') cx, 
(select gdid,sj from gds_goodspricegrp where grpid='004701' and guid='00') zc 
where t.gbid=kc.gstgdid(+) 
and t.gbid=cx.popgdid(+) 
and t.gbid=zc.gdid(+)"""
cxdata = pd.read_sql(sql,db)
data.close()
path='D:\\京东上传数据\\'
os.chdir(path)
jdcode = pd.read_excel('gs.xls',sheet_name='Sheet1')
jdcode['UPC编码'] = jdcode['UPC编码'].apply(lambda x: '{:.0f}'.format(x))
total = pd.merge(jdcode,cxdata,how='inner',left_on='UPC编码',right_on='GBBARCODE')
sjdata = copy.deepcopy(total[['ID','SKU编码','SJ']][total.SJ>0])
kcdata = copy.deepcopy(total[['ID','SKU编码','KC']])
kcdata.loc[kcdata['KC'] <10,'KC'] =0
kcdata['KC']=numpy.ceil(kcdata['KC'] /2)
kcdata.insert(2,'null','')
kcdata.columns=(kctital)
sjdata.insert(3,'null','')
sjdata.columns=(sjtital)
kcdata.to_excel('kc.xls',index=False)
sjdata.to_excel('sj.xls',index=False)
totalTime=round(time.time()-firsttime,1)
print('生成结束，请在"D:\京东上传数据"目录中上传京东需要的文件！程序运行时间：%s秒' % (totalTime))