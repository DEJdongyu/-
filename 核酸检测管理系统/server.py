from flask import Flask, render_template
import flask
import pymysql


app = flask.Flask(__name__)
# 初始化数据库连接
# 使用pymysql.connect方法连接本地mysql数据库
db = pymysql.connect(host='localhost', port=3306, user='root',
                     password='dax71205', database='mysql_dys', charset='utf8')
# 操作数据库，获取db下的cursor对象
cursor = db.cursor()
# 存储登陆用户的名字用户其它网页的显示
users = []


@app.route("/",methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/templates/user1.html",methods=["GET", "POST"])
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
        user_code = user_id + user_id[::-1]
        print(user_id, user_name,user_code)

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
    return flask.render_template('user1.html', insert_result=insert_result,  results=results)


@app.route("/templates/user2.html",methods=["GET", "POST"])
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


@app.route("/templates/user3.html",methods=["GET", "POST"])
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
    results = cursor.fetchall()
    return flask.render_template('user3.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)
