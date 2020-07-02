from flask import Flask,render_template,request,redirect,url_for,session,make_response
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anime.db'
app.config['SECRET_KEY'] = 'imsecre'
app.config[' SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Register(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    mail = db.Column(db.String)
    feedback = db.Column(db.String(10))



@app.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        feedback = request.form['feedback']
        u = Register(name=name,mail=mail,feedback=feedback)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('users'))


@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/contact',methods=['GET','POST'])
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/what')
def what():
    return render_template('what.html')

@app.route('/best')
def best():
    return render_template('best.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/users')
def users():
    users= Register.query.all()

    return render_template('user.html',users=users)


@app.route('/success',methods=['POST'])
def success():
    
    if request.method=='POST':
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        password = request.form['pass']

    if password == 'ninu':
        resp = redirect(url_for('profile'))
        resp.set_cookie('name',session['name'])
        return resp

    else:
        return '<h1>Wrong password</h1>'

@app.route('/profile')
def profile():
    name = request.cookies.get('name')
    resp = make_response(render_template('index.html',name=name))
    return resp

@app.route('/logout')
def logout():
    if 'name' in session:
        session.pop('name',None)
        return 'Logout succesfull'
    else:
        return 'Already logged Out'

@app.route('/char',methods=['GET','POST'])
def charactors():
    return render_template('charactors.html')



   




@app.before_first_request
def create_tables():
    db.create_all()




if __name__=='__main__':
    app.run(debug=True)