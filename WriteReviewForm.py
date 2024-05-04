from flask import Flask, render_template, request, url_for, flash, redirect, make_response, app
from data import db_session
from data import __all_models
from header import header_logic, search_logic
import datetime


def writeNewReview(method):
    if method == 'GET':
        return render_template('NewReviewForm.html', film_title='', mark_value=0,
                               year_film='', review_user='', btn_text='Добавить отзыв')
    else:
        if 'header_btn' in request.form:
            return header_logic()
        elif 'submit_btn' in request.form:
            return search_logic()
        else:
            user_id = request.cookies.get('id')
            db_sess = db_session.create_session()
            title = request.form['movie_title']
            mark = request.form['mark']
            genre = request.form['genreOfFilm']
            year = request.form['movie_year']
            review = request.form['feedback']
            db_film = db_sess.query(__all_models.Reviews).filter(__all_models.Reviews.title == title,
                                                                 __all_models.Reviews.id_user == user_id).first()
            if db_film:
                flash('Вы уже написали обзор на этот фильм!')
                return render_template('NewReviewForm.html')
            else:
                user = db_sess.query(__all_models.User).filter(__all_models.User.id == user_id).first()
                film = __all_models.Reviews()
                film.id_user = user_id
                film.name_user = user.name
                film.title = title
                film.mark = mark
                film.genre = genre
                film.year = year
                film.review = review
                created_date = datetime.datetime.now()
                created_date = created_date.strftime("%d-%m-%Y %H:%M")
                film.date = created_date
                db_sess.add(film)

                films = db_sess.query(__all_models.Films).filter(__all_models.Films.title == title).first()
                if films:
                    films.countReviews += 1
                    user.reviews_count += 1
                    films.mark = f'{films.mark}_{mark}'
                    films.average_mark = sum([int(i) for i in films.mark.split('_')]) / films.countReviews
                    if genre not in films.genres.split(', '):
                        films.genres = f'{films.genres}, {genre}'
                else:
                    films = __all_models.Films()
                    films.title = title
                    films.mark = f'{mark}'
                    films.genres = f'{genre}'
                    films.year = year
                    films.countReviews = 1
                    user.reviews_count += 1
                    films.average_mark = int(films.mark) / films.countReviews
                    db_sess.add(films)
                db_sess.commit()
                return redirect('/news')