from library import app
from flask import render_template, url_for, redirect, request
from library.models import Books, Member
from library import db
import requests


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/books')
def books_page():
    books = Books.query.all()
    return render_template('books.html', books=books)    
    
@app.route('/members')
def members_page():
    member = Member.query.all()
    return render_template('members.html', member=member)

@app.route('/create', methods = ['POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        fee = request.form['fee']
        count = request.form['count']
        book = Books(name=name, author=author, fee=fee, count=count)
        db.session.add(book)
        db.session.commit()
        return redirect('/books')

@app.route('/search', methods = ['POST'])
def search_book(): 
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        if author:
            book = Books.query.filter_by(author=author).first()
            return render_template('data.html', book=book)
        if name:
            book = Books.query.filter_by(name=name).first()
            return render_template('data.html', book=book)

@app.route('/update',methods = ['POST'])
def update():    
    if request.method == 'POST':
        book = Books.query.get(request.form.get('id'))
        book.name = request.form['name']
        book.author = request.form['author']
        book.fee = request.form['fee']
        book.count = request.form['count']

        db.session.commit()
        return redirect('/books')

@app.route('/delete/<id>', methods=['GET','POST'])
def delete(id):
    book = Books.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect('/books')

# Here are member routes:  

@app.route('/member/create', methods = ['POST'])
def createmem():
    if request.method == 'POST':
        name = request.form['name']
        rent = request.form['rent']
        mem = Member(name=name, rent=rent)
        db.session.add(mem)
        db.session.commit()
        return redirect('/members')

@app.route('/members/search', methods = ['POST'])
def search_member(): 
    if request.method == 'POST':
        name = request.form['name']
        if name:
            mem = Member.query.filter_by(name=name).first()
            return render_template('mem_data.html', mem=mem)

@app.route('/members/update',methods = ['POST'])
def update_member():    
    if request.method == 'POST':
        mem = Member.query.get(request.form.get('id'))
        mem.name = request.form['name']
        mem.rent = request.form['rent']

        db.session.commit()
        return redirect('/members')

@app.route('/member/delete/<id>', methods=['GET','POST'])
def delete_member(id):
    mem = Member.query.get(id)
    db.session.delete(mem)
    db.session.commit()
    return redirect('/members')

@app.route('/api')
def import_api():
    response = requests.get('https://frappe.io/api/method/frappe-library')
    json_response = response.json()
    return render_template('api.html', json_response=json_response)