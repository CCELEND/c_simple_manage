
import Flask_app
import Management_portal
import Error_info
import Employee_fun
import Admin_fun

if __name__ == '__main__':
    # Flask_app.app.run()
    Flask_app.app.run(debug=True,host='0.0.0.0',port=8000)
