from flask import Flask, render_template, request, url_for, redirect, flash, make_response
from data import db_session
from flask_uploads import UploadSet, configure_uploads, IMAGES
import login_script
import registration_script
import main_script
import WriteReviewForm
import profile_script

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fjgut7gjvhd8794kbhd65h'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/pictures'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@app.route('/login', methods=['POST', 'GET'])
def loginFormEnter():
    return login_script.login(request.method)


@app.route('/registration', methods=['POST', 'GET'])
def regFormEnter():
    return registration_script.reg(request.method)


@app.route('/news', methods=['POST', 'GET'])
def newsFormEnter():
    return main_script.news(request.method)


@app.route('/reviews', methods=['POST', 'GET'])
def reviewsFormEnter():
    return main_script.reviews_check(request.method)


@app.route('/writeReview', methods=['POST', 'GET'])
def writeRevFormEnter():
    return WriteReviewForm.writeNewReview(request.method)


@app.route('/delete_review/<int:id>', methods=['POST', 'GET'])
def deleteReview(id):
    return profile_script.delete_review(request.method, id)


@app.route('/change_review/<int:id>', methods=['POST', 'GET'])
def changeReview(id):
    return profile_script.change_review(request.method, id)


@app.route('/profile', methods=['POST', 'GET'])
def profileEnter():
    return profile_script.main(request.method, photos)


if __name__ == '__main__':
    db_session.global_init("data/db/users.db")
    app.run(port=8080, host='127.0.0.1')