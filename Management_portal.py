#coding=utf-8
from Flask_app import *

#管理员系统
@app.route('/HRMS/<user>/<id>')
def HRMS(user,id):
    if id in session:
        if user == session[id]:
            print(Admin_login_dict)
            return render_template("HRMS.html", user=user, id=id)

    session['flag'] = True
    return redirect(url_for('Loginerror'))

#用户系统
@app.route('/Employee/<user>/<id>')
def Employee(user,id):
    if id in session:
        if user == session[id]:
            print(Employee_login_dict)
            return render_template("Employee.html", user=user, id=id)

    session['flag'] = True
    return redirect(url_for('Loginerror'))
