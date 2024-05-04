from flask import Flask, render_template, request, url_for, redirect, flash, make_response
from data import db_session
from werkzeug.security import generate_password_hash, check_password_hash
import registration_script
import main_script
from data import __all_models


def login(method):
    db_sess = db_session.create_session()
    user_id = request.cookies.get('id')

    if method == 'GET':
        user1 = db_sess.query(__all_models.User).filter(__all_models.User.id == user_id).first()
        if user1.remember_form:
            resp = make_response(render_template(
                'login.html', email_value=user1.email, password_value=user1.hashed_password, check_value='checked'))
            resp.set_cookie('autofill', '1', max_age=30 * 24 * 3600)
            return resp
        else:
            resp = make_response(render_template(
                'login.html', email_value='', password_value='', check_value=''))
            resp.set_cookie('autofill', '0', max_age=30 * 24 * 3600)
            user1.remember_form = False
            db_sess.commit()
            return resp

    elif method == 'POST':
        if request.form['btn'] == 'registration':
            return redirect('/registration')
        else:
            autofill = request.cookies.get('autofill')
            login = request.form['email']
            user2 = db_sess.query(__all_models.User).filter(__all_models.User.email == login).first()
            if autofill == '1' and user2.email == login:
                if 'remember_data' in request.form:
                    user2.remember_form = True
                else:
                    user2.remember_form = False
                db_sess.commit()
                resp1 = make_response(redirect('/news'))
                resp1.set_cookie('id', str(user2.id), max_age=30 * 24 * 3600)
                resp1.set_cookie('autofill', '1' if user2.remember_form is True else '0', max_age=30 * 24 * 3600)
                return resp1
            else:
                password = request.form['password']
                user = db_sess.query(__all_models.User).filter(__all_models.User.email == login).first()
                if 'remember_data' in request.form:
                    user.remember_form = True
                else:
                    user.remember_form = False
                db_sess.commit()

                if check_password_hash(user.hashed_password, password):
                    resp2 = make_response(redirect('/news'))
                    resp2.set_cookie('id', str(user.id), max_age=30 * 24 * 3600)
                    resp2.set_cookie('autofill', '1' if user.remember_form is True else '0', max_age=30 * 24 * 3600)
                    return resp2
                else:
                    flash('Неверный логин или пароль')
                    return redirect('/login')