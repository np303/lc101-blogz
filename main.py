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




class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return self.username

##############################
def logged_in_user():
    owner = User.query.filter_by(username=session['user']).first()
    return owner

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')     


# @app.route('/')
# def index():
#     return render_template('singleuser.html',title="Blogz", posts=posts,)       


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    return redirect('/blog')    


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        
        username_db_count = User.query.filter_by(username=username).count()
        if username_db_count > 0:
            flash('yikes! "' + username + '" is already taken and password reminders are not implemented')
            return redirect('/signup')
        if password != verify:
            flash('passwords did not match')
            return redirect('/signup')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.username
        return redirect("/newpost")
    else:
        return render_template('signup.html')

def get_user_posts(username):
    return User.query.filter_by(username=session['username']).first()

@app.route('/',  methods=['POST', 'GET'])
def home():
    allusers = User.query.all()
    return render_template('index.html', users=allusers)

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    
    #Query database for all blog posts
    allblogposts = Blog.query.all()
    post_id = request.args.get('id')
    singleuser_id = request.args.get('owner_id')
    blogpost = Blog.query.filter_by(id=post_id).first()
    

    welcome = "You are not logged in"
    if 'username' in session:
        welcome = "Welcome, " + session['username']
      
    if (post_id):
        welcome = "Welcome, " + session['username']
        blogpost = Blog.query.filter_by(id=post_id).first()
        owner = User.query.filter_by(username=session['username']).first()
        return render_template('singlepost.html', blogpost=blogpost, owner=blogpost.owner.username, welcome=welcome)
    
    else:
        if (singleuser_id):
            singleuserblogs = Blog.query.filter_by(owner_id=singleuser_id)
            return render_template('singleuser.html', posts=singleuserblogs)        


    return render_template('blog.html', title="Blogs!", posts=allblogposts, blogpost=blogpost, welcome=welcome)




@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    
    posterror = ""
    
    if request.method == 'POST':

        #look inside the html form for user data    
        title = request.form['title']
        post = request.form['post']
        owner = User.query.filter_by(username=session['username']).first()
        
        #creat a newpost reference 
        newpost = Blog(title, post, owner)
        db.session.add(newpost)
        db.session.commit()

        #creat a link to go to the new post when use clicks submit
        postlink = "/blog?id=" + str(newpost.id)

        return redirect(postlink)

    return render_template('newpost.html', title="WTF", posterror=posterror)
                


if __name__ == '__main__':
    app.run()
