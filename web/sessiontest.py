from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return '正在执行，请稍后等待邮件告知'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['oldpasswd']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p>老密码：<input type=text name=oldpasswd>
            <p><input type=submit value=修改>
            <p>注意：请输入正确的老密码才能正常修改，修改成功后，会邮件通知到管理员新的密码
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
    app.run(host='0.0.0.0')