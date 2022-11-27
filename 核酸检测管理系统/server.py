from flask import Flask, render_template
import flask
import pymysql
import datetime
import re

app = flask.Flask(__name__)
# 初始化数据库连接
# 使用pymysql.connect方法连接本地mysql数据库
db = pymysql.connect(host='localhost', port=3306, user='root',
                     password='dax71205', database='mysql_dys', charset='utf8')
# 操作数据库，获取db下的cursor对象
cursor = db.cursor()
# 存储登陆用户的名字用户其它网页的显示
users = []
now = datetime.datetime.now()
now = now.strftime("%Y%m%d")
print(now)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/templates/user1.html", methods=["GET", "POST"])
def user1():
    insert_result = ''
    if flask.request.method == 'GET':
        sql_list = "select * from users"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    if flask.request.method == 'POST':
        # 获取输入的学生信息
        user_id = flask.request.values.get("user_id", "")
        user_name = flask.request.values.get("user_name", "")
        user_code = user_id + now
        print(user_id, user_name, user_code)

        try:
            # 信息存入数据库
            sql = "create table if not exists users(user_id varchar(255) primary key,user_name varchar(20),user_code varchar(255));"
            cursor.execute(sql)
            sql_1 = "insert into users(user_id, user_name, user_code)values(%s,%s,%s)"
            cursor.execute(sql_1, (user_id, user_name, user_code))
            # result = cursor.fetchone()
            insert_result = "成功存入一条用户信息"
            print(insert_result)
        except Exception as err:
            print(err)
            insert_result = "用户信息插入失败"
            print(insert_result)
            pass
        db.commit()
        # POST方法时显示数据
        sql_list = "select * from users"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    return flask.render_template('user1.html', insert_result=insert_result, results=results)


@app.route("/templates/user2.html", methods=["GET", "POST"])
def user2():
    user_name = flask.request.values.get("user_name", "")
    user_id = flask.request.values.get("user_id", "")
    try:
        sql_delete = "delete from users where user_id='" + user_id + "';"
        cursor.execute(sql_delete)
        insert_result = "成功删除用户" + user_id + user_name
        print("删除成功")
    except Exception as err:
        print(err)
        insert_result = "删除用户失败"
        pass
    db.commit()
    sql_list = "select * from users"
    cursor.execute(sql_list)
    results = cursor.fetchall()
    return flask.render_template('user2.1.html', results=results)


@app.route("/templates/user3.html", methods=["GET", "POST"])
def user3():
    user_name = flask.request.values.get("user_name", "")
    user_id = flask.request.values.get("user_id", "")
    try:
        sql_select = "select * from users where user_id='" + user_id + "';"
        cursor.execute(sql_select)
        insert_result = "成功查询结果" + user_id + user_name
        print("查询成功")
    except Exception as err:
        print(err)
        sql_delete = ""
        insert_result = "查询结果失败"
        pass
    db.commit()
    results = cursor.fetchone()
    print(results)
    return flask.render_template('user3.html', results=results)


@app.route("/templates/doctor-login.html", methods=["GET", "POST"])
def doctor_login():
    results = ''
    if flask.request.method == 'POST':
        doctor_name = flask.request.values.get("doctor_name", "")
        doctor_id = flask.request.values.get("doctor_id", "")
        # 防止sql注入,如:select * from admin where admin_name = '' or 1=1 -- and password='';
        # 利用正则表达式进行输入判断
        if doctor_name != None and doctor_id != None:  # 验证通过
            msg = '用户名或id错误'
            # 正则验证通过后与数据库中数据进行比较
            sql = "select * from doctors where doctor_name='" + \
                  doctor_name + "' and doctor_id='" + doctor_id + "';"
            cursor.execute(sql)
            results = cursor.fetchone()
            # print(results)
            # 匹配得到结果即管理员数据库中存在此管理员
            if results:
                # 登陆成功
                # return
                return flask.redirect(flask.url_for('doctor2'))
                # return flask.redirect('/file')
        else:  # 输入验证不通过
            msg = '非法输入'
    else:
        msg = ''
    return flask.render_template('doctor-login.html', results=results)


@app.route("/templates/doctor2.html", methods=["GET", "POST"])
def doctor2():
    doctor_id = flask.request.values.get("doctor_id", "")
    group_id = flask.request.values.get("group_id", "")
    user_code = flask.request.values.get("user_code", "")
    doctor_name = ''
    print(doctor_id)
    try:
        sql_select = "select doctor_name from doctors where doctor_id ='" + \
                     doctor_id + "';"
        cursor.execute(sql_select)
    except Exception as err:
        # print(err)
        sql_delete = ""
        insert_result = "查询结果失败"
        pass
    db.commit()
    doctor_name = (cursor.fetchone())
    print(doctor_name)

    try:
        sql_select = "insert into doctors(doctor_name,doctor_id,group_id,user_code)  values(%s,%s,%s,%s)"
        cursor.execute(
            sql_select, (doctor_name, doctor_id, group_id, user_code))
        insert_result = "成功查询结果" + \
                        ''.join(doctor_name) + doctor_id + group_id + user_code
        print("查询成功")
    except Exception as err:
        print(err)
        sql_delete = ""
        insert_result = "查询结果失败"
        pass
    db.commit()
    results = cursor.fetchall()
    return flask.render_template('doctor2.html', results=results)


@app.route("/templates/doctor3.html", methods=["GET", "POST"])
def doctor3():
    if flask.request.method == 'GET':
        sql_list = "select user_name,user_id,users.user_code,group_id,doctor_id,doctor_name,result" \
                   " from users,doctors where users.user_code = doctors.user_code ;"

        cursor.execute(sql_list)
        results = cursor.fetchall()
        print(results)
        return flask.render_template('doctor3.html', results=results)

    elif flask.request.method == 'POST':
        user_code = flask.request.values.get("user_code", "")
        results = ''
        try:
            sql_select = "delete " \
                         " from doctors where user_code = '" + \
                         user_code + "';"
            cursor.execute(sql_select)
            db.commit()
            sql_select = "select user_name,user_id,users.user_code,group_id,doctor_id,doctor_name,result" \
                         " from users,doctors where users.user_code = doctors.user_code ;"
            cursor.execute(sql_select)
        except Exception as err:
            # print(err)
            sql_delete = ""
            insert_result = "查询结果失败"
            pass
        db.commit()

        results = (cursor.fetchall())
        print(results)
        return flask.render_template('organization3.html', results=results)


@app.route("/templates/organization-login.html", methods=["GET", "POST"])
def organization_login():
    results = ''
    if flask.request.method == 'POST':
        organ_name = flask.request.values.get("organ_name", "")
        organ_id = flask.request.values.get("organ_id", "")
        # 防止sql注入,如:select * from admin where admin_name = '' or 1=1 -- and password='';
        # 利用正则表达式进行输入判断
        if organ_name != None and organ_id != None:  # 验证通过
            msg = '用户名或id错误'
            # 正则验证通过后与数据库中数据进行比较
            sql = "select * from organs where organ_name='" + \
                  organ_name + "' and organ_id='" + organ_id + "';"
            cursor.execute(sql)
            results = cursor.fetchone()
            # print(results)
            # 匹配得到结果即管理员数据库中存在此管理员
            if results:
                # 登陆成功
                # return
                return flask.redirect(flask.url_for('organization2'))
                # return flask.redirect('/file')
        else:  # 输入验证不通过
            msg = '非法输入'
    else:
        msg = ''
    return flask.render_template('organization-login.html', results=results)


@app.route("/templates/organization2.html", methods=["GET", "POST"])
def organization2():
    user_code = flask.request.values.get("user_code", "")
    result = flask.request.values.get("result", "")
    print(user_code, result)

    try:
        sql_select = "update users set result = '" + result + "'where user_code='" + user_code + "'and result " \
                                                                                                 "is NULL ; "
        cursor.execute(sql_select)
        print("增加成功")
    except Exception as err:
        print(err)
        sql_delete = ""
        insert_result = "增加失败"
        pass
    db.commit()
    results = cursor.fetchall()
    return flask.render_template('organization2.html', results=results)


@app.route("/templates/organization3.html", methods=["GET", "POST"])
def organization3():
    if flask.request.method == 'GET':
        sql_list = "select user_name,user_id,users.user_code,group_id,doctor_id,doctor_name,result" \
                   " from users,doctors where users.user_code = doctors.user_code ;"

        cursor.execute(sql_list)
        results = cursor.fetchall()
        print(results)
        return flask.render_template('organization3.html', results=results)

    elif flask.request.method == 'POST':
        user_code = flask.request.values.get("user_code", "")
        results = ''
        try:
            sql_select = "select user_name,user_id,users.user_code,group_id,doctor_id,doctor_name,result" \
                         " from users,doctors where users.user_code = doctors.user_code ;"
            cursor.execute(sql_select)
        except Exception as err:
            # print(err)
            sql_delete = ""
            insert_result = "查询结果失败"
            pass
        db.commit()

        sql_select = "delete " \
                     " from doctors where user_code = '" + \
                     user_code + "';"
        cursor.execute(sql_select)
        db.commit()
        sql_select = "update users set result = NULL where user_code = '" + user_code + "';"
        cursor.execute(sql_select)
        db.commit()
        results = (cursor.fetchall())
        print(results)
        return flask.render_template('organization3.html', results=results)
    # else:
    #     results = ''
    #     return flask.render_template('organization3.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)
