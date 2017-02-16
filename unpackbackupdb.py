#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import os
import sqlite3

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_max_index(db):
    query = 'SELECT max(file_index) FROM apk_file_info'

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)

    try:
        for row in cur:
            maxindex = row[0]
            break
    except Exception, e:
        print Exception, ':', e

    return maxindex


def get_file_path(db, file_index):
    query = 'SELECT * FROM apk_file_info WHERE file_index IS %s;' % file_index

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)

    try:
        for row in cur:
            # print(row[1])
            file_path = row[1]
            break
    except Exception, e:
        print Exception, ':', e

    cur.close()

    return file_path


def get_file_data(db, file_index, file_path):
    status = False

    query = 'SELECT * FROM apk_file_data WHERE file_index=%d;' % file_index

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)

    # Go through returned rows
    try:
        if not os.path.exists(u'%s' % os.path.dirname(file_path)):
            os.makedirs(u'%s' % os.path.dirname(file_path))
        with codecs.open(u'%s' % file_path, 'wb') as f:
            for index, row in enumerate(cur):
                data_index = row[0]
                file_index = row[1]
                file_length = row[2]
                file_data = row[3]
                print 'write file'
                f.write(file_data)
                print 'file writed'

            f.close()
            status = True
    except Exception, e:
        print Exception, ':', e

    cur.close()

    return status


def extract_from_file(db_file, local_path):
    max_index = get_max_index(db_file)

    for fileindex in xrange(0, max_index + 1):
        path = local_path + get_file_path(db_file, fileindex).replace(r'/', '\\')
        print path
        if not get_file_data(db_file, fileindex, path):
            print 'FALSE'
            break


def extract_from_path(backup_path, local_path):
    huawei_system_db = ['alarm.db', 'calendar.db', 'calllog.db', 'contact.db', 'harassment.db', 'HWlanucher.db',
                        'phoneManager.db', 'smartcare.db', 'sms.db', 'weather.db', 'wifiConfig.db']
    for root, subdir, files in os.walk(unicode(backup_path, 'utf-8')):
        for filename in files:
            if filename.endswith('.db') and filename not in huawei_system_db:
                filepath = os.path.join(root, filename)
                print filepath
                extract_from_file(filepath, local_path)


if __name__ == '__main__':
    # Target dir
    ex_path = r'F:\targetdir'
    
    # extract from single db file
    #db_file_path = r'M:\backupdir\com.tencent.mm.db'
    #extract_from_file(db_file_path, ex_path)
    
    # extract from backup directory
    bak_path = r'M:\backupdir'
    extract_from_path(bak_path, ex_path)
