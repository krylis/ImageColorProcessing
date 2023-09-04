import os
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'test'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submit an
        # an empty file without a filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fullpath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(fullpath)
            flash(f"You successfully uploaded {file.filename}")
            return render_template("index.html", image_path=fullpath, got_image=True)
        elif file and not allowed_file(file.filename):
            flash("You can only upload files with the following extensions: \t"
                  "JPG, JPEG, GIF, PNG")
            return redirect(request.url)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
