import os,xlrd,cx_Oracle,xlwt,time#导入需要用到的模块
starttime=time.time()
def connect():#连接数据库，将数据写入到变量中
     global cxdata
     db = cx_Oracle.connect('dbusrm04/futuremkt@mg08')
     data = db.cursor()
     sql="""select distinct(gbbarcode),nvl(sl,0),decode(nvl(cx.cxj,zc.sj),null,0,nvl(cx.cxj,zc.sj)) sj from
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
     data.execute(sql)
     cxdata = data.fetchall()
     data.close()

def openexcel():#打开京东条码对应商场编码
     global jdcode,x,y
     gs = xlrd.open_workbook('D:\\京东上传数据\\gs.xls')
     jdcode = gs.sheet_by_name('Sheet1')
     x = jdcode.nrows
     y = jdcode.ncols
     

def createnew():#将筛选的条件，生成新的数据，保存列表中
     global kc,sj
     kc=[]
     sj=[]
     for i in range(len(cxdata)):
             for k in range(1,x):
                  if cxdata[i][0] == jdcode.cell(k,1).value:
                       jdkc = cxdata[i][1]/2
                       if jdkc < 5:
                            kc.append(('10052976',jdcode.cell(k,2).value,'',0))
                       else:kc.append(('10052976',jdcode.cell(k,2).value,'',int(jdkc)))
                       if cxdata[i][2] > 0:
                            sj.append(('10052976',jdcode.cell(k,2).value,cxdata[i][2]))

def save_excel():#生成标题，将数据导入到excel中
     w_kc = xlwt.Workbook()
     w_jg = xlwt.Workbook()
     kc_s1 = w_kc.add_sheet('Sheet1')
     jg_s1 = w_jg.add_sheet('Sheet1')
     t_kc = ['门店编号(必填)','SKU编码','商家商品编号（与SKU编码不能同时为空）','现货库存（必填）']
     t_jg = ['门店ID(必填)','商品SKU编码(必填)','到家价(必填)','市场价(非必填)']
     for i in range(0,4):
          kc_s1.write(0,i,t_kc[i])
          jg_s1.write(0,i,t_jg[i])
     for i in range(len(kc)):
          for k in range(len(kc[0])):
               kc_s1.write(i+1,k,kc[i][k])
     for i in range(len(sj)):
          for k in range(len(sj[0])):
               jg_s1.write(i+1,k,sj[i][k])
     w_kc.save('D:\\京东上传数据\\京东上传（库存）.xls')
     w_jg.save('D:\\京东上传数据\\京东上传（价格）.xls')

connect()
openexcel()
createnew()
save_excel()
totalTime=round(time.time()-starttime,2)
print('生成结束，请在"D:\京东上传数据"目录中上传京东需要的文件！程序运行时间：%s秒' % (totalTime))
