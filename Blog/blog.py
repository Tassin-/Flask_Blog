#blog.py - CONTROLLER

#Imports
from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from functools import wraps

#Configure
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'hard_to_guess'


app = Flask(__name__)

#pulls in app config by looking for uppercase variables
app.config.from_object(__name__)

#function used for connecting to the database
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

@app.route('/', methods = ['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		#If the login form from the login page does not match the USERNAME or PASSWORD return an error
		if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']: 
			error = 'Invalid Credentials. Please try again.'
		#Else if the login form is correct the session status is set to logged in and the error = none
		else:
			session['logged_in'] = True
			return redirect(url_for('main')) #redicrts you to the main page.
	return render_template('login.html', error = error)

@app.route('/main')
@login_required
def main():
	g.db = connect_db() #connects to the database
	cur = g.db.execute('select * from posts') #Fetches data from the posts table within the database
	posts = [dict(title = row[0], post = row[1]) for row in cur.fetchall()] #assins the data in the database as a dictionary
	g.db.close()
	return render_template('main.html', posts = posts)

@app.route('/add', methods = ['POST'])
@login_required
def add():
	title = request.form['title']
	post = request.form['post']
	if not title or not post:
		flash('All fields are required. Please try again.')
		return redirect(url_for('main'))
	else:
		g.db = connect_db()
		#after connecting to the database insert into the posts table title and post from the HTML form
		g.db.execute('insert into posts (title, post) values (?,?)', [request.form['title'], request.form['post']])
		#commit the following into the database
		g.db.commit()
		g.db.close()
		flash('New entry was successfully posted')
		return redirect(url_for('main'))

@app.route('/logout')
def logout():
	session.pop('logged_in', None) #pops the logged in to reset the session key
	flash('You were logged out')
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug = True)
