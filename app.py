#Import Flask and SQLAlchemy
from flask import Flask, render_template, session, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

#Intiate flask
app = Flask(__name__)
app.secret_key = ';;fwfwe;dsad423dds23ds'

#The session will close and expire when the browser closes
app.config['SESSION_PERMANENT'] = False
#Session type has been set to file system
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

#Intiate and configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SQLALCHEMY_BINDS'] = {'products': 'sqlite:///new_products.db'}
db = SQLAlchemy(app)

#Login database structure
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)    

    def __repr__(self):
        return f"login('{self.username}, {self.email}, {self.password}')"

#Products database structure
class product(db.Model):
    __bind_key__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    stocks = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image  = db.Column(db.String(100), nullable=False, default='default.png')
    category_name = db.Column(db.String(100), nullable=False)
    discount = db.Column(db.Float, nullable=True)
    best_category = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"products('{self.name}, {self.description}, {self.stocks}, {self.price}, {self.image}, {self.category_name}, {self.discount}, {self.best_category}')"



#Render Home page
@app.route('/')
def index():
    best_categories = product.query.filter_by(best_category=True).all()
    return render_template('index.html', best_categories=best_categories)

#Render Login page
@app.route('/login')
def login():
    return render_template('login.html')

#Render Settings page
@app.route('/accessibility')
def accessibility():
    return render_template('accessibility.html')

#Render View Products page
@app.route('/products')
def products():
    fruits = product.query.filter_by(category_name='Fruit').all()
    return render_template('Products.html', fruits=fruits)

#render Cart page
@app.route('/cart/<int:product_id>')
def cart(product_id):
    product_id = product.query.get_or_404(product_id)
    return render_template('cart.html', product_id=product_id)

#Render About us page
@app.route('/about')
def about():
    return render_template('About.html')

#Render Offers page
@app.route('/offers')
def offers():
    return render_template('Offers.html')

#Render Dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template('Dashboard.html')
    

#Render Loyalty page
@app.route('/loyalty')
def loyalty():
    return render_template('Loyalty.html')

#Render Register page
@app.route('/register')
def register():
        return render_template('Register.html')



#Ensuring users account is created from the data base
@app.route('/registering', methods=['POST', 'GET'])
def Registering():
    #Check if the method was post
    if request.method == 'POST':


        #Username, email and password from register form input
        username = request.form.get('Username')
        email = request.form.get('Email')
        password = request.form.get('Password')

        #Checking if a user already exists
        user_existence = user.query.filter_by(email=email).first()
        if user_existence:
            flash('User already exists')
            return redirect('/register')
        
        #Hashing password
        hashed_password = generate_password_hash(password)

        #Putting the form together in a variable
        create_account = user(username=username, email=email, password=hashed_password)

        #Adding te input form information to the database 
        db.session.add(create_account)
        db.session.commit()
        #Redirect back to login
        return redirect('/login')
    else:
        #Stay in register page
        return redirect('/Register')

#user logs in
@app.route('/logging', methods=['POST', 'GET'])
def logging():
    
    #Check if the method was post
    if request.method == 'POST':
        #email and password from register form input
        email = request.form.get('Email')
        password = request.form.get('Password')

        #Fetching the email being requested upon
        new_user = user.query.filter_by(email=email).first()

        #If the email and the checked password is correct login in to the home page.
        if new_user and check_password_hash(new_user.password, password):
            
            session['username'] = f'{new_user.username}...'
            session['email'] = f'{new_user.email}...'
            session['password'] = f'{new_user.password}...'
            return redirect('/')
        else:
            return redirect('/login')
    
#User logs out
@app.route('/logout')
def logout():
    #Setting the session username, email and password to none
    session['username'] = ''
    session['email'] = ''
    session['password'] = ''
    return redirect('/')

#render privacy policy
@app.route('/policy')
def privacy_policy():
    return render_template('privacy_policy.html')

#Run the website WSAG
if __name__ == "__main__":
    app.run(debug=True)