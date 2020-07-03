import base64
import uuid
import os
import re
from bs4 import BeautifulSoup as bs
from flask import current_app, url_for


def img_proc(src):
    data = bs(src, "html.parser")
    for img in data.find_all("img"):
        img_src = img["src"]
        if not os.path.exists(img_src):
            filename = str(uuid.uuid4())
            extension = str(re.findall(r"(?<=image/)(.*)(?=;base64)", img_src)[0])
            b64string = str(re.findall(r"(?<=base64,)(.*)", img_src))
            with open(os.path.normpath(os.path.join(current_app.config["UPLOADED_PATH"], filename+"."+extension)), "wb") as fh:
                fh.write(base64.b64decode(b64string))
            img["src"] = url_for("static", filename="uploads/"+os.path.basename(fh.name))
            img["data-filename"] = os.path.basename(fh.name)
        else:
            continue
    return data.prettify()


