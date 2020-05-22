import base64
import uuid
import os
from flask import current_app, request


def img_decode(s):
    extension = (s.split("data:image/"))[1].split(";base64")[0]
    filename = str(uuid.uuid4())
    b64string = (s.split("base64,"))[1].split('" ')[0]
    img_dict = {"filename": filename+"."+extension, "b64string": b64string}
    return img_dict


def img_src(s):
    with open(os.path.join("\\", img_decode(s)["filename"]), "wb") as fh:
        fh.write(base64.b64decode(str(img_decode(s)["b64string"])))
    to_replace = (s.split("img src="))[1].split(" style=")[0]
    s = s.replace(to_replace, fh.name)
    return s

file = request.files

f = file.save()