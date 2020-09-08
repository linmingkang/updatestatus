# -*- coding: UTF-8 -*-
import os,time, pymysql, datetime


ping_interval = 3
db_user = ''
db_password = ''

try:
    file_r = open('/home/chsr/cf.d/groundusr.conf', 'r')
    file_r.readline()
    file_r.readline()
    db_user = file_r.readline()[len('mysqluser='):].strip()
    db_password = file_r.readline()[len('mysqlpasswd='):].strip()
    file_r.close()
except:
    print('配置文件groundusr.conf异常，该文件是否存在？该文件的内容格式是否符合规范？请相关人员检查。')
    exit()

db_host = '127.0.0.1'
db_port = 3306
db_name = 'db_ground_transfer'


def db_insert_update_del(cursor, sql):
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()



while True:
    print('start')
    try:
        db = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            db=db_name
        )
    except:
        print('mysql数据库连接失败，请确保 /home/chsr/cf.d/trainuser.conf中数据库用户名、密码正确。\n程序退出')
        exit()
    cursor = db.cursor()
    cursor.execute('select train_id, curr_ver from train_other_info where update_status=1;')
    train_id_lists = cursor.fetchall()
    if len(train_id_lists) == 0:
        print('无车辆正在更新')
    else:
        train_ids = {}
        for train_id in train_id_lists:
            train_ids[train_id[0]] = train_id[1]
        for train_id, curr_ver in train_ids.items():
            try:
                #fileList = os.listdir('/home/chsr/data.d/train-to-ground.d/%s/updateinfo/'%train_id)
                #print(fileList[0])
                file_name='%s+%s'%(train_id,curr_ver)
                file_path='/home/chsr/data.d/train-to-ground.d/%s/updateinfo/%s'%(train_id,file_name)
                print(file_path)
                file_r = open(file_path,'r')
                status = file_r.readline(1)
                print(status)
                file_r.close()
                if status=='1':
                    print('ok')
                    update_time = datetime.datetime.now().strftime('%Y-%m-%d')
                    print(update_time)
                    sql = "update train_other_info set update_status = 0,update_time='%s' where train_id = '%s' AND curr_ver='%s';" % (update_time,train_id,curr_ver)
                    db_insert_update_del(cursor, sql)
                    try:
                        os.system("rm %s -rf" % file_path)
                    except OSError as e:
                        print("Error:  %s : %s" % (file_path, e.strerror))
                elif status=='0':
                    print('fail')
                    sql = "update train_other_info set update_status = 9 where train_id = '%s' AND curr_ver='%s';" %(train_id,curr_ver)
                    db_insert_update_del(cursor, sql)
                else:
                    print('wenjianyichang')
                #sql = "update train_other_info set online_flag = %s where train_id = '%s';" % (train_id,status)
                #db_insert_update_del(cursor, sql)
                #try:
                    #os.system("rm %s -rf" % file_path)
                #except OSError as e:
                    #print("Error:  %s : %s" % (file_path, e.strerror))
            except:
                pass
    time.sleep(ping_interval)
db.close()
