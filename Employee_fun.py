#coding=utf-8
from Flask_app import *
from UserDataPart import User_information

#判断用户id是否存在，存在就返回用户对象字典，否则返回none
def GetEmployee(id):
    for user in User_information.USERS_DATA:
        if user.get("id") == int(id):
            return user
    else:
        return None

#修改用户信息
def EditEmployee(id,name,sex,birth,education,address,phone):
    for user in User_information.USERS_DATA:
        if user.get("id") == int(id):
            if name != '':
                user["姓名"] = name
                #按照姓名以字典排序，姓名需要gbk编码
                # User_information.USERS_DATA = sorted(User_information.USERS_DATA, key=lambda x: x['姓名'])
                User_information.USERS_DATA = sorted(User_information.USERS_DATA, key=lambda x: x['姓名'].encode('gbk'))
            if sex != '':
                user["性别"] = sex
            if birth != '':
                user["出生年月"] = birth
            if education != '':
                user["学历"] = education
            if address != '':
                user["住址"] = address
            if phone != '':
                user["电话"] = phone
            User_information.write_data() #数据同步到文件中
            break

#显示用户信息界面
@app.route('/EmployeeShow/<user>/<id>')
def EmployeeShow(user,id):
    if id in session:
        if user == session[id]:
            Employee = GetEmployee(id)
            return render_template("EmployeeShow.html", user=user, id=id, 
                Employee=Employee)
    
    session['flag'] = True
    return redirect(url_for('Loginerror'))

#修改用户信息界面
@app.route('/EmployeeEdit/<user>/<id>')
def EmployeeEdit(user,id):
    if id in session:
        if user == session[id]:
            Employee = GetEmployee(id)
            return render_template("EmployeeEdit.html", user=user, id=id,
                Employee=Employee)
    
    session['flag'] = True
    return redirect(url_for('Loginerror'))

@app.route('/EmployeeEditHandle/<user>/<id>', methods = ['POST', 'GET'])
def EmployeeEditHandle(user,id):
    if id in session:
        if user == session[id]:
            if request.method == "POST":  # 获取到表单数据

                name = request.form['name']
                sex = request.form['sex']
                birth = request.form['birth']
                education = request.form['education']
                address = request.form['address']
                phone = request.form['phone']

                EditEmployee(id,name,sex,birth,education,address,phone)
                return redirect(url_for('Employee', user=user, id=id))
            else:
                return redirect(url_for('EmployeeEdit', user=user, id=id))

    session['flag'] = True
    return redirect(url_for('Loginerror'))


