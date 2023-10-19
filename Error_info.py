#coding=utf-8
from Flask_app import *

#错误界面
@app.route('/Error')
def Error():
    return render_template("Error.html", myurl="", errorinfo="非法访问! ")

#用户名密码错误路由
@app.route('/Userpassworderror')
def UserPassworderror():
    if session['flag']:
        return render_template("Error.html", myurl="", errorinfo="用户名或密码错误, 请重新登录! ")
    return redirect(url_for('Error'))

#登录错误路由
@app.route('/Loginerror') 
def Loginerror():
    if session['flag']:
        return render_template("Error.html", myurl="", errorinfo="未登录或登录过期, 请重新登录! ")
    return redirect(url_for('Error'))