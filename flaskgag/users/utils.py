import os
from datetime import date
import secrets
import PIL
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskgag import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)


    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def save_post_picture(form_post_picture, form_post_title):
    current_time = str(date.today())
    file_name = form_post_title + "-" + current_time
    _, f_ext = os.path.splitext(form_post_picture.filename)
    picture_fn = file_name + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', picture_fn)

    basewidth = 600
    i = Image.open(form_post_picture)
    wpercent = (basewidth / float(i.size[0]))
    hsize = int((float(i.size[1]) * float(wpercent)))
    i = i.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    i.save(picture_path)

    return picture_fn

# basewidth = 300
#  img = Image.open(‘fullsized_image.jpg')
#  wpercent = (basewidth / float(img.size[0]))
#  hsize = int((float(img.size[1]) * float(wpercent)))
#  img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
#  img.save(‘resized_image.jpg')


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@successcode.pro', recipients=[user.email])
    msg.body = f''' To reset your email click on the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email.
'''
    mail.send(msg)


