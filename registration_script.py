from flask import Flask, render_template, request, url_for, flash, redirect, make_response
from data import db_session
from werkzeug.security import generate_password_hash, check_password_hash
from data import __all_models
import datetime


def reg(method):
    if method == 'GET':
        return render_template('register.html')
    elif method == 'POST':
        db_sess = db_session.create_session()
        email = request.form['email']
        password_1 = request.form['password1']
        password_2 = request.form['password2']
        name = request.form['nickname']
        db_email = db_sess.query(__all_models.User).filter(__all_models.User.email == email).first()
        db_name = db_sess.query(__all_models.User).filter(__all_models.User.name == name).first()
        if db_email is not None and email == db_email.email:
            flash('Данный email занят')
            return reg('GET')
        elif db_name is not None and name == db_name.name:
            flash('Данный никнейм занят')
            return reg('GET')
        if password_1 == password_2:
            user = __all_models.User()
            user.name = name
            user.email = email
            user.hashed_password = generate_password_hash(password_1)
            user.reviews_count = 0
            created_date = datetime.datetime.now()
            created_date = created_date.strftime("%d-%m-%Y")
            user.created_date = created_date
            db_sess.add(user)
            db_sess.commit()
            resp = make_response(redirect('/login'))
            resp.set_cookie('id', str(user.id), max_age=30*24*3600*3)
            return resp
        else:
            flash('Пароли не совпадают')
            return reg('GET')