# app.py

from flask import Flask, render_template, redirect, flash, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Config & Connexion to database
app.secret_key = "any_random_string"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model definition (= tables creation)
class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(255))
	email = db.Column(db.String(255))
	
	def __init__(self, name, email):
		self.name = name
		self.email = email

@app.route('/')
def index():
	users = User.query.all()
	return render_template("index.html", users=users)
	
@app.route('/add', methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		# Get data from the form
		name = request.form.get('name')
		email = request.form.get('email')
		# Save to db
		user = User(name, email)
		db.session.add(user)
		db.session.commit()
		# Redirect
		flash("User added.")
		return redirect(url_for('index'))
	else:
		return render_template('add.html')
		
@app.route('/edit', methods=['GET', 'POST'])
def edit():
	if request.method == 'POST':
		user = User.query.get(request.form.get('id'))
		user.name = request.form.get('name')
		user.email = request.form.get('email')
		db.session.commit()
		flash("User edited.")
	else:
		id=request.args.get('id')
		if not id:
			flash("No user ID provided.")
		else:
			user=User.query.get(id)
			return render_template('edit.html', user=user) 
	return redirect(url_for('index'))
		
@app.route('/delete')
def delete():
	id=request.args.get('id')
	if not id:
		flash("No user ID provided.")
	else:
		db.session.delete(User.query.get(id))
		db.session.commit()
		flash("User deleted.")
	return redirect(url_for('index'))