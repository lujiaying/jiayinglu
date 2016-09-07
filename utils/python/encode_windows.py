#coding: utf-8

import csv
import codecs

# 处理微软windows平台上的文件编码问题
with open('egg.csv', 'wb') as csvfile:
    #处理为BOM_UTF8编码
    csvfile.write(codecs.BOM_UTF8)

    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['哈哈', '是不是中文'])
    csvwriter.writerow(['t1', 't2'])
    csvwriter.writerow(['BOM_UTF8编码', '微软的后门编码'])    
