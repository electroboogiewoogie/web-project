from flask import Flask, render_template, request, url_for, flash, redirect, make_response, app, abort
from data import db_session
from data import __all_models
import pymorphy2
import random

morph = pymorphy2.MorphAnalyzer()
word = morph.parse('Человек')[0]


def header_logic():
    if request.form['header_btn'] == 'Home':
        return redirect('/news')
    if request.form['header_btn'] == 'Profile':
        return redirect('/profile')
    if request.form['header_btn'] == 'Logout':
        return redirect('/login')
    if request.form['header_btn'] == 'search':
        return search_logic()
    if request.form['header_btn'] == 'Generate':
        return generate_film()


def search_logic():
    db_sess = db_session.create_session()
    user_id = request.cookies.get('id')
    title = request.form['movie_title']
    genre = request.form['genreOfFilm']
    year = request.form['movie_year']
    sort_type = request.form['type_of_sort']
    if not title:
        films1 = []
        value = [genre, year, sort_type]
        Nones_pos = [i for i, param in enumerate(value) if param == '' or param == 'Жанр' or param == 'Сортировать по']
        filters_without_nones = list(filter(lambda x: x != '' or x != 'Жанр' or x != 'Сортировать по', value))
        print(value, Nones_pos)
        if not Nones_pos:
            return redirect('/news')
        elif Nones_pos[0] == 0:
            films = db_sess.query(__all_models.Films).filter(__all_models.Films.year == year).all()
        elif Nones_pos[0] == 1:
            films = db_sess.query(__all_models.Films).filter(__all_models.Films.genres == genre).all()
        for i in films:
            films1.append([i.title, i.average_mark, i.genres, i.year, i.countReviews])
        if sort_type == 'title_filter':
            films1.sort(key=lambda x: x[1])
        elif sort_type == 'year_filter':
            films1.sort(key=lambda x: x[4])
        elif sort_type == 'marks_filter':
            films1.sort(key=lambda x: x[2])
        elif sort_type == 'count_filter':
            films1.sort(key=lambda x: x[-1])
    else:
        films1 = []
        films = db_sess.query(__all_models.Reviews).filter(__all_models.Reviews.title == title).all()
        for i in films:
            films1.append([i.title, i.year, i.genre, i.mark, i.review, i.date, i.name_user])

        return render_template('Reviews_form.html', reviews=films1)

    return render_template('news.html', reviews=films1, word=word)


def generate_film():
    db_sess = db_session.create_session()
    user_id = request.cookies.get('id')

    films = db_sess.query(__all_models.Films).all()
    films = random.choice(films)
    films1 = [[films.title, films.average_mark, films.genres, films.year, films.countReviews], []]
    print(films1)
    return render_template('news.html', reviews=films1, word=word)