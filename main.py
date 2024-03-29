from flask import Flask,flash,redirect,render_template,request,url_for
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo



with open ('D:\python exersice\Projects\My Blog\config.json','r') as c:
    params = json.load(c)["params"]
   
local_server=True
app = Flask(__name__)

app.secret_key ="f65d0847e02e55345c1b1eca1fbbeb6b6a874ceafa757244ee15ece12801cd9d"
# app.config.update (
#                    DEBUG = True,
#                    MAIL_SERVER="smtp.gmail.com",
#                    MAIL_PORT="465",
#                    MAIL_USE_SSL=True,
#                    MAIL_USER_NAME=params["gmail_user"],
#                    MAIL_PASSWORD=params["gmail_pass"]
#                    )
# mail= Mail(app)

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI']= params['local_uri']
   
else:
    app.config['SQLALCHEMY_DATABASE_URI']= params['prod_uri']

db=SQLAlchemy(app)
class Registration(db.Model):
    sno=db.Column(db.Integer,primary_key = True)
    name=db.Column(db.String(45),nullable=False)
    emailid = db.Column(db.String(45),nullable=False)
    password = db.Column(db.String(60),nullable=False)
    mobno=db.Column(db.String(45),nullable=False)
    message=db.Column(db.String(45),nullable=False)

class Loginform(FlaskForm): 
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("password",validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("password")])
    submit=SubmitField("Login")



@app.route("/")
def home():
        return render_template("index.html",params= params)

@app.route("/about")
def about():
        return render_template("about.html",params=params)

@app.route("/post")
def post():
        return render_template("post.html",params= params)

@app.route("/register",methods = ['GET','POST'])
def register():
    if  request.method =='POST':
            name = request.form.get('name')
            email= request.form.get('email')
            mobile=request.form.get('mobile')
            message=request.form.get('message')
            entry = Registration(name= name,emailid=email,mobno=mobile,message = message)
            db.session.add(entry)
            db.session.commit()
            
            # mail.send_message("new message from "+ name,
            #     sender= email,recipients=[params['gmail_user']],body=message +"\n"+ mobile)
            
            flash("Registration succesful!","success")
            return redirect(url_for("home"))        
    return render_template("contact.html",params = params)

@app.route("/login",methods=["GET","POST"])
def login():
       form= Loginform()
       if form.validate_on_submit():
                if form.email.data=="sumansatyanshu@gmail.com" and form.password.data=="123456":
                        flash("you are logged in !!")
                        return redirect(url_for("home"))
                else:
                        flash("Login Unsucessfull.please check email and password!",'danger')                    
       return render_template("login.html",title="Login",form=form,params=params)


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0")
