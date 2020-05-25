import base64
import uuid
import os
import re
from flask import current_app, url_for


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
    s = s.replace(to_replace, "\""+url_for("static", filename="uploads/"+os.path.basename(fh.name))+"\"")
    return s


def proc_img(s):
    """This is function!!

    Arguments:
        s {[type]} -- [description]
    """
    for img_tag in re.findall(r"(?<=<img)(.*)(?=>)", s):
        img_src(img_tag)
    return s

