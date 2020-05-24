import base64
import uuid
import os
from app import db
from app.main import bp
from app.main.forms import EditProfileForm, PostForm
from app.models import User, Post
from flask import current_app, request, send_from_directory, url_for


def img_decode(s):
    extension = (s.split("data:image/"))[1].split(";base64")[0]
    filename = str(uuid.uuid4())
    b64string = (s.split("base64,"))[1].split('" ')[0]
    img_dict = {"filename": filename+"."+extension, "b64string": b64string}
    return img_dict


def img_src(s):
    with open(os.path.normpath(os.path.join(current_app.config["UPLOADED_PATH"], img_decode(s)["filename"])), "wb") as fh:
        fh.write(base64.b64decode(str(img_decode(s)["b64string"])))
    to_replace = (s.split("src="))[1].split(" data-")[0]
    s = s.replace(to_replace, "\""+url_for('static\\uploads', filename=os.path.basename(fh.name))+"\"")
    return s

"""
@bp.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOADED_PATH"], filename)
"""