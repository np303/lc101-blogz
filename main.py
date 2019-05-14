from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    post = db.Column(db.Text())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __init__(self, title, post, owner):
        self.title = title
        self.post =  post
        self.owner = owner

posts = []


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password
        

##############################
def logged_in_user():
    owner = User.query.filter_by(email=session['user']).first()
    return owner

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')     


@app.route('/')
def index():
    return render_template('singleuser.html',title="Blogz", posts=posts,)       


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')    


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        
        email_db_count = User.query.filter_by(email=email).count()
        if email_db_count > 0:
            flash('yikes! "' + email + '" is already taken and password reminders are not implemented')
            return redirect('/signup')
        if password != verify:
            flash('passwords did not match')
            return redirect('/signup')
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.email
        return redirect("/")
    else:
        return render_template('signup.html')


@app.route('/blogs', methods=['POST', 'GET'])
def blogs():
    
    #Query database for all blog posts
    allblogposts = Blog.query.all()
    post_id = request.args.get('id')
  
    if (post_id):
        blogpost = Blog.query.get(post_id)
        return render_template('singleuser.html', blogpost=blogpost)

    return render_template('blogs.html', title="Blogs!", posts=allblogposts)



@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    
    posterror = ""
    
    if request.method == 'POST':

        #look inside the html form for user data    
        title = request.form['title']
        post = request.form['post']
        owner = User.query.filter_by(email=session['email']).first()
        
        #creat a newpost reference 
        newpost = Blog(title, post, owner)
        db.session.add(newpost)
        db.session.commit()

        #creat a link to go to the new post when use clicks submit
        postlink = "/blogs?id=" + str(newpost.id)

        return redirect(postlink)

    return render_template('newpost.html', title="WTF", posterror=posterror)
                


if __name__ == '__main__':
    app.run()
