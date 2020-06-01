
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
    s = s.replace(to_replace, "\""+url_for(os.path.normpath('main.uploads'), filename=os.path.basename(fh.name), _external=True)+"\"")
    return s

@bp.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOADED_PATH"], filename)


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


@bp.route("/upload", methods=["POST", "GET"])
def upload():
    form = PostForm()
    if request.method == "POST":
        if "image" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["image"]
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename): 
            #if os.path.exists(current_app.config["UPLOADED_PATH"] + "/" + file.filename): # if image with same name exists
            _dot = file.filename.find(".")
            file.filename = str(uuid.uuid4()) + file.filename[_dot:]
            filename = secure_filename(file.filename)
            file.save(os.path.normpath(os.path.join(current_app.config["UPLOADED_PATH"], filename)))
            flash("File successfully uploaded")
            return file.filename
        else:
            flash("Not allowed file typed")
            return redirect(request.url)
