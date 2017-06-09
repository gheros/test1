from flask import Flask, session, redirect, url_for, escape, request,render_template

import passwd
app = Flask(__name__)

@app.route('/change')
def change():
    if 'oldpasswd' in session:
        passwd.sentmail(session['oldpasswd'])
        # passwd.cpasswd('aa','')
        print((session['oldpasswd']))
        return '正在执行，请稍后等待邮件告知管理员，新密码请向管理员咨询，您目前的输入的老密码为%s,若密码有误，将修改失败' % escape(session['oldpasswd'])
    return '谢谢'
@app.route('/loginxx', methods=['GET', 'POST'])
def loginxx():
    if request.method == 'POST':
        session['oldpasswd'] = request.form['oldpasswd']
        return redirect(url_for('change'))
    return '''
        <form action="" method="post">
            <p>老密码：<input type=text name=oldpasswd>
            <p><input type=submit value=修改>
            <p>注意：请输入正确的老密码才能正常修改，修改成功后，会邮件通知到管理员新的密码
        </form>
    '''
@app.route('/login', methods=['GET', 'POST'])
def login():
    return (render_template('login.html',title='Home'))
#模板
@app.route('/index')
def index():
    user = {'nickname': '大爷'}
    return(render_template('index.html',title='Home',user=user))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return(redirect(url_for('index')))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
    app.run(host='0.0.0.0')