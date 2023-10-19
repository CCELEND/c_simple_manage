#coding=utf-8
from Flask_app import *
from UserDataPart import User_information
from copy import *

#判断员工ID是否存在
def AdminJudgeEmployeeId(id):
    for user in User_information.USERS_DATA:
        if user.get("id") == int(id): #获取键id的值
            return True
    return False

 #判断员工用户名是否存在
def AdminJudgeEmployeeUsername(username):
    for user in User_information.USERS_DATA:
        if user.get("username") == username:
            return True
    return False

#添加职工
def AdminAddEmployee(id,name,sex,birth,education,job,address,phone,username,password):
    user_dict = {}
    user_dict["id"] = int(id)

    user_dict["姓名"] = name
    user_dict["性别"] = sex
    user_dict["出生年月"] = birth
    user_dict["学历"] = education
    user_dict["职务"] = job
    user_dict["住址"] = address
    user_dict["电话"] = phone

    user_dict["username"] = username
    #密码需要加盐保存
    hash_password = User_information.generate_password_hash(password)
    user_dict["password"] = hash_password

    User_information.USERS_DATA.append(user_dict) #对象列表添加用户信息的字典
    #按照姓名以字典排序，姓名需要gbk编码
    User_information.USERS_DATA = sorted(User_information.USERS_DATA, key=lambda x: x['姓名'].encode('gbk'))
    User_information.write_data() #数据同步到文件中

#编辑职工
def AdminEditEmployee(id,name,sex,birth,education,job,address,phone,username,password):
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
            if job != '':
                user["职务"] = job
            if address != '':
                user["住址"] = address
            if phone != '':
                user["电话"] = phone
            
            if username != '':
                user["username"] = username
            if password != '':
                #密码加盐
                hash_password = User_information.generate_password_hash(password)
                user["password"] = hash_password
            
            User_information.write_data() #数据同步到文件中
            break

#搜索职工, 返回用户信息列表
def AdminSearchEmployee(id,name,sex,birth,education,job,address,phone):
    id_data = []
    name_data = []
    sex_data = []
    birth_data = []
    education_data = []
    job_data = []
    address_data = []
    phone_data = []

    user_data_temp = deepcopy(User_information.USERS_DATA) #深拷贝，不会修改源列表
    for user in user_data_temp:
        user['id'] = str(user['id'])

    if id != '':
        for user in user_data_temp:
            if user.get("id") == id:
                id_data.append(user)
                return id_data
  
    if name != '':
        for user in user_data_temp:
            if user.get("姓名") == name:
                name_data.append(user)
        return name_data

    if sex != '':
        for user in user_data_temp:
            if user.get("性别") == sex:
                sex_data.append(user)
        return sex_data

    if birth != '':
        for user in user_data_temp:
            if user.get("出生年月") == birth:
                birth_data.append(user)
        return birth_data

    if education != '':
        for user in user_data_temp:
            if user.get("学历") == education:
                education_data.append(user)
        return education_data   

    if job != '':
        for user in user_data_temp:
            if user.get("职务") == job:
                job_data.append(user)
        return job_data

    if address != '':
        #地址模糊查找
        address_data = [temp for temp in user_data_temp if any(address in v for v in temp.values())]
        return address_data

    if phone != '':
        for user in user_data_temp:
            if user.get("电话") == phone:
                phone_data.append(user)
                return phone_data

#删除职工
def AdminDeleteEmployee(id):
    for user in User_information.USERS_DATA:
        if user.get("id") == int(id):
            if id in session:
                session.pop(id) #如果是登录状态就弹出
            User_information.USERS_DATA.remove(user) #删除该用户信息的字典
            User_information.write_data() #数据写入文件
            break

#排序职工, reverse: 排序规则, reverse=False升序(默认), reverse=True降序
def AdminSortEmployee(parameters,sort_reverse):
    USERS_DATA_SORT = []
    if parameters == '姓名':
        USERS_DATA_SORT = sorted(User_information.USERS_DATA, key=lambda x: x['姓名'].encode('gbk'), reverse=sort_reverse)
        return USERS_DATA_SORT
    USERS_DATA_SORT = sorted(User_information.USERS_DATA, key=lambda x: x[parameters], reverse=sort_reverse)
    return USERS_DATA_SORT

#显示所有职工信息路由
@app.route('/AdminShow/<user>/<id>')
def AdminShow(user,id):
    if id in session:
        if user == session[id]:
            Employee_all = User_information.USERS_DATA
            return render_template("AdminShow.html", user=user, id=id, 
                Employee = Employee_all )
            
    session['flag'] = True
    return redirect(url_for('Loginerror'))

#添加职工路由
@app.route('/AdminAdd/<user>/<id>')
def AdminAdd(user,id):
    if id in session:
        if user == session[id]:
            return render_template("AdminAdd.html", user=user, id=id)
    session['flag'] = True
    return redirect(url_for('Loginerror'))

@app.route('/AdminAddHandle/<user>/<id>', methods = ['POST', 'GET'])
def AdminAddHandle(user,id):
    if id in session:
        if user == session[id]:
            if request.method == "POST":  # 获取到表单数据
                Employeeid = request.form['Employeeid']

                name = request.form['name']
                sex = request.form['sex']
                birth = request.form['birth']
                education = request.form['education']
                job = request.form['job']
                address = request.form['address']
                phone = request.form['phone']

                username = request.form['username']
                password = request.form['password']
                
                if len(Employeeid) != 0 and len(username) != 0: 
                    #满足用户名，ID都不存在
                    if not (AdminJudgeEmployeeId(Employeeid) or AdminJudgeEmployeeUsername(username)):
                        if not (len(name) == 0 or len(sex) == 0 or len(birth) == 0 or len(education) == 0
                        or len(job) == 0 or len(address) == 0 or len(phone) == 0
                        or len(password) == 0):
                            AdminAddEmployee(Employeeid,name,sex,birth,education,job,address,phone,username,password)
                            return redirect(url_for('HRMS', user=user, id=id))
                    
                    return render_template("Error.html", user=user, id=id, 
                        errorinfo="用户名或ID已存在, 请重新输入", myurl='AdminAdd')

                return render_template("Error.html", user=user, id=id, 
                    errorinfo="请输入用户名和ID", myurl='AdminAdd')
            
            return redirect(url_for('AdminAdd', user=user, id=id))

    session['flag'] = True
    return redirect(url_for('Loginerror'))

#修改员工信息路由
@app.route('/AdminEdit/<user>/<id>')
def AdminEdit(user,id):
    if id in session:
        if user == session[id]:
            return render_template("AdminEdit.html", user=user, id=id)
    
    session['flag'] = True
    return redirect(url_for('Loginerror'))

@app.route('/AdminEditHandle/<user>/<id>', methods = ['POST', 'GET'])
def AdminEditHandle(user,id):
    if id in session:
        if user == session[id]:
            if request.method == "POST":  # 获取到表单数据
                Employeeid = request.form['Employeeid']

                name = request.form['name']
                sex = request.form['sex']
                birth = request.form['birth']
                education = request.form['education']
                job = request.form['job']
                address = request.form['address']
                phone = request.form['phone']

                username = request.form['username']
                password = request.form['password']

                #如果id存在, 且用户名为空
                if len(Employeeid) != 0 and AdminJudgeEmployeeId(Employeeid) and len(username) == 0:
                    AdminEditEmployee(Employeeid,name,sex,birth,education,job,address,phone,username,password)
                    return redirect(url_for('HRMS', user=user, id=id))

                #如果id存在, 且用户名不为空, 用户名不存在, 密码不为空
                if (len(Employeeid) != 0 and AdminJudgeEmployeeId(Employeeid) and len(username) != 0
                and len(password) != 0 and not AdminJudgeEmployeeUsername(username)):
                    AdminEditEmployee(Employeeid,name,sex,birth,education,job,address,phone,username,password)
                    return redirect(url_for('HRMS', user=user, id=id))
                
                return render_template("Error.html", user=user, id=id,
                    errorinfo="ID错误, 请重新输入！", myurl='AdminEdit')

            return redirect(url_for('AdminEdit', user=user, id=id))

    session['flag'] = True
    return redirect(url_for('Loginerror'))


#删除员工信息路由
@app.route('/AdminDelete/<user>/<id>')
def AdminDelete(user,id):
    if id in session:
        if user == session[id]:
            return render_template("AdminDelete.html", user=user, id=id)
    
    session['flag'] = True
    return redirect(url_for('Loginerror'))

@app.route('/AdminDeleteHandle/<user>/<id>', methods = ['POST', 'GET'])
def AdminDeleteHandle(user,id):
    if id in session:
        if user == session[id]:
            if request.method == "POST":  # 获取到表单数据
                Employeeid = request.form['Employeeid']

                if len(Employeeid) != 0 and AdminJudgeEmployeeId(Employeeid):
                    AdminDeleteEmployee(Employeeid)
                    return redirect(url_for('HRMS', user=user, id=id))
                
                return render_template("Error.html", user=user, id=id,
                    errorinfo="ID错误, 请重新输入！", myurl='AdminDelete')
            
            return redirect(url_for('AdminDelete', user=user, id=id))

    session['flag'] = True
    return redirect(url_for('Loginerror'))

#搜索员工信息路由
@app.route('/AdminSearch/<user>/<id>')
def AdminSearch(user,id):
    if id in session:
        if user == session[id]:
            return render_template("AdminSearch.html", user=user, id=id)
    
    session['flag'] = True
    return redirect(url_for('Loginerror'))

@app.route('/AdminSearchResult/<user>/<id>', methods = ['POST', 'GET'])
def AdminSearchResult(user,id):
    if id in session:
        if user == session[id]:
            if request.method == "POST":  # 获取到表单数据
                Employeeid = request.form['Employeeid']

                name = request.form['name']
                sex = request.form['sex']
                birth = request.form['birth']
                education = request.form['education']
                job = request.form['job']
                address = request.form['address']
                phone = request.form['phone']

                Employee = []
                Employee = AdminSearchEmployee(Employeeid,name,sex,birth,education,job,address,phone)
                return render_template("AdminSearchResult.html", user=user, id=id,
                             Employee = Employee)

            return redirect(url_for('AdminSearch', user=user, id=id))

    session['flag'] = True
    return redirect(url_for('Loginerror'))

#排序所有职工信息路由
@app.route('/AdminSort/<user>/<id>')
def AdminSort(user,id):
    if id in session:
        if user == session[id]:
            return render_template("AdminSort.html", user=user, id=id)
    
    session['flag'] = True
    return redirect(url_for('Loginerror'))

@app.route('/AdminSortHandle/<user>/<id>', methods = ['POST', 'GET'])
def AdminSortHandle(user,id):
    if id in session:
        if user == session[id]:
            if request.method == "POST":  # 获取到表单数据

                parameters = request.form['parameters']
                sort_reverse = request.form['sort_reverse']

                if parameters == '':
                    return render_template("Error.html", user=user, id=id,
                        errorinfo="请输入排序参数", myurl='AdminSort')

                if ((parameters == 'id' or parameters == '姓名' or parameters == '性别' or parameters == '出生年月' or parameters == '电话') and (sort_reverse == 'True' or sort_reverse == '' or sort_reverse == 'False')):
                    if sort_reverse == '' or sort_reverse == 'False':
                        sort_reverse = False
                    else:
                        sort_reverse = True
                    Employee_sort = []
                    Employee_sort = AdminSortEmployee(parameters,sort_reverse)
                    return render_template("AdminSortShow.html", user=user, id=id, 
                        Employee = Employee_sort)
                return render_template("Error.html", user=user, id=id,
                    errorinfo="排序参数错误", myurl='AdminSort')

            return redirect(url_for('AdminSort', user=user, id=id))

    session['flag'] = True
    return redirect(url_for('Loginerror'))