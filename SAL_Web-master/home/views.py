from django.http.response import HttpResponse
from django.shortcuts import render
from datetime import datetime
import pymysql.cursors


def getConnection():
    return pymysql.connect(host='localhost',
                           user='user',
                           password='user',
                           db='sal',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor
                           )


def setting(request):
    table = []
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM sal.sensorlist "
        cursor.execute(sql)
        for row in cursor.fetchall():
            table.append(row)
        connection.close()

    for t in table:
        if request.GET.get(t["id"] + '_update') == None or request.GET.get(t["id"] + '_update') == '':
            print(t["id"] + 'はnullですよ')
        else:
            print(t["id"] + 'のNameを' +
                  request.GET.get(t["id"] + '_update') + 'に変更しました。')
            sql = "UPDATE sal.SensorList SET Name = '" + \
                request.GET.get(t["id"] + '_update') + \
                "' WHERE id = '" + t["id"] + "'; "

            connection = getConnection()
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
                print(sql)
                # 更新
                sql = "SELECT * FROM sal.sensorlist "
                cursor.execute(sql)
                print(sql)
                table = []
                for row in cursor.fetchall():
                    table.append(row)
                connection.close()

    d = {
        'table': table,
    }
    return render(request, 'setting.html', d)


def home(request):
    # sqlに接続
    connection = getConnection()
    # select文 よりスマートな方法があるはず
    with connection.cursor() as cursor:
        sql = "SELECT path FROM sal.imagelist WHERE id = (SELECT MAX(id) FROM sal.imagelist)"
        cursor.execute(sql)
        result = cursor.fetchone()
        path = result["path"]

        sql = "SELECT Date FROM sal.imagelist WHERE id = (SELECT MAX(id) FROM sal.imagelist)"
        cursor.execute(sql)
        result = cursor.fetchone()
        data = result["Date"]
    # sqlから切断
    connection.close()
    d = {
        'path': path,
        'data': data,
    }

    return render(request, 'home.html', d)


def logs(request):
    connection = getConnection()
    logs = []
    with connection.cursor() as cursor:
        sql = "SELECT * FROM sal.imagedate "
        cursor.execute(sql)
        for row in cursor.fetchall():
            logs.append(row)
        connection.close()
    d = {
        'logs': logs,
    }
    print(logs[1])
    return render(request, 'logs.html', d)
