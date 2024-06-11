from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, DiaryEntryForm, UpdateEntryForm
from app.models import User, DiaryEntry
from flask_login import login_user, current_user, logout_user, login_required
from app.utils import save_picture  # Import the save_picture function

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/new_entry", methods=['GET', 'POST'])
@login_required
def new_entry():
    form = DiaryEntryForm()
    if form.validate_on_submit():
        picture_file = None
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        entry = DiaryEntry(content=form.content.data, image_file=picture_file, author=current_user)
        db.session.add(entry)
        db.session.commit()
        flash('Your entry has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_entry.html', title='New Entry', form=form)

@app.route("/calendar")
@login_required
def calendar():
    entries = DiaryEntry.query.filter_by(author=current_user).all()
    return render_template('calendar.html', entries=entries)

@app.route("/entry/<int:entry_id>/update", methods=['GET', 'POST'])
@login_required
def update_entry(entry_id):
    entry = DiaryEntry.query.get_or_404(entry_id)
    if entry.author != current_user:
        abort(403)
    form = UpdateEntryForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            entry.image_file = picture_file
        entry.content = form.content.data
        db.session.commit()
        flash('Your entry has been updated!', 'success')
        return redirect(url_for('calendar'))
    elif request.method == 'GET':
        form.content.data = entry.content
    return render_template('update_entry.html', title='Update Entry', form=form)

@app.route("/entry/<int:entry_id>/delete", methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = DiaryEntry.query.get_or_404(entry_id)
    if entry.author != current_user:
        abort(403)
    db.session.delete(entry)
    db.session.commit()
    flash('Your entry has been deleted!', 'success')
    return redirect(url_for('calendar'))







