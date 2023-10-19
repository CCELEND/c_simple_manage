
from Module_management import *
from UserDataPart import User_information

app = Flask(__name__)
app.secret_key = 'celendedbdfeldbsdemddkwcelend'  #设置应用程序的secret_key
app.permanent_session_lifetime = timedelta(seconds=60*10) #设置session存活时间为10分钟

#用户登录状态字典
Admin_login_dict={}
Employee_login_dict={}

# User_information.write_data()

#读取职工数据文件到内存
User_information.read_data()


def get_user(username):
    for user in User_information.USERS_DATA:
        if user.get("username") == username:
            return user
    return None

#根路由，跳转到登录表单页面
@app.route('/')
def Login():
    session['flag'] = False
    return render_template("Login.html")

#注销判断路由
@app.route('/LogoutHandle/<user>/<id>')
def LogoutHandle(user,id):
    global Admin_login_dict,Employee_login_dict
    if id in session:
        if user == session[id]:
            if id in Admin_login_dict:
                whatmanage = 'HRMS'
            else:
                whatmanage = 'Employee'
            return render_template("LogoutHandle.html", user=user, id=id, whatmanage=whatmanage)
    
    session['flag'] = True
    return redirect(url_for('Loginerror'))

#注销后，跳转到登录表单页面
@app.route('/Logout/<user>/<id>')
def Logout(user,id):
    global Admin_login_dict,Employee_login_dict
    if id in session:
        if user == session[id]:
            session.pop(id)
            if id in Admin_login_dict:
                Admin_login_dict.pop(id)
            else:
                Employee_login_dict.pop(id)
            
            return redirect(url_for('Login'))
    
    session['flag'] = True
    return redirect(url_for('Loginerror'))

#登录验证路由，跳转到验证页面，并传递表单参数。允许POST和GET方式。
@app.route('/Loginjudgment', methods=["POST", "GET"])
def Loginjudgment():
    # 对POST方式提交过来的表单数据进行处理
    # POST方式用 request.form 获取数据，GET方式用 request.args 获取数据
    global Admin_login_dict,Employee_login_dict
    if request.method == "POST":  # 获取到表单数据
        username = request.form['Username']
        password = request.form['Password']
        user_info = get_user(username)
        if user_info is None:
            session['flag'] = True
            return redirect(url_for('UserPassworderror'))
        else:
            if user_info.get("username") == 'admin':
                if check_password_hash(user_info.get("password"), password):
                    id = str(user_info.get("id"))
                    if id in session:
                        session.pop(id)
                        if id in Admin_login_dict:
                            Admin_login_dict.pop(id)    
                    session.permanent = True
                    username_hash = generate_password_hash(username)
                    session[id] = username_hash
                    Admin_login_dict[id] = username
                    return redirect(url_for('HRMS', user=username_hash, id=id)) #函数名
                else:
                    session['flag'] = True
                    return redirect(url_for('UserPassworderror'))	
            else:
                if check_password_hash(user_info.get("password"), password):
                    id = str(user_info.get("id"))
                    if id in session:
                        session.pop(id)
                        if id in Employee_login_dict:
                            Employee_login_dict.pop(id)               
                    session.permanent = True
                    username_hash = generate_password_hash(username)
                    session[id] = username_hash
                    Employee_login_dict[id] = username
                    return redirect(url_for('Employee', user=username_hash, id=id)) #函数名
                else:
                    session['flag'] = True
                    return redirect(url_for('UserPassworderror'))
    else:
        return redirect(url_for('Login'))
