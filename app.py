import os
from flask import Flask, render_template, request
from flask.helpers import flash
from flask_wtf.recaptcha import validators
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from wtforms import FileField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired
from db import cur,conn,create_tables
import secrets
import os
app=Flask(__name__)
@app.route("/")
def index():
    return "APP IS RUNNING"

class Upload(FlaskForm):
    file=FileField("File", validators=[DataRequired()])
    submit=SubmitField("Submit")

def save_file(file): 
    random_hex=secrets.token_hex(8)
    _, f_ext=os.path.splitext(file.filename)
    file_fn=random_hex+f_ext
    file_path=os.path.join('uploads',file_fn)
    file.save(file_path)
    return file_fn

@app.route("/upload", methods=["POST","GET"])
def upload():
    form=Upload()
    try:
        if request.method == 'POST':
            file =request.files["file"]
            print(file)
            try:
                file_name=save_file(file)
                print(file_name)
                fop=open("uploads/"+file_name,"rb")
                fdata=fop.read()
                que="""INSERT INTO files(filename,file_data) VALUES(%s,%s)"""
                val=(file_name,fdata)
                cur.execute(que,val)
                conn.commit()

            except Exception as e:
                print(str(e))

                
    except Exception as e:
            return "ther was an error"  + str(e)
    return render_template("upload.html", form=form)

if __name__=="__main__":
    app.secret_key="karimojid"
    app.run(debug=True)