import os,time, pymysql, datetime
# -*- coding: UTF-8 -*-
import os, time, pymysql, datetime



try:
    newFileNames='01.zip.sncjnd34'
    sql=newFileNames[0:newFileNames.rfind('.zip')]
    print(sql)
except OSError as e:
    print("Error:  %s : %s" % (newFileNames, e.strerror))