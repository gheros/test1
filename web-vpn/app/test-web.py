from flask import Flask, session, redirect, url_for, escape, request,render_template
from flask import app
app = Flask(__name__)
@app.route("/")
def index():
    import subprocess
    cmd = subprocess.Popen(["ps_mem"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,error = cmd.communicate()
    memory = out.splitlines()
    return()
