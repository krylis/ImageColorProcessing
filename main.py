import os
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'test'


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_colors_in_image(filepath):
    def rgb_to_hex(r, g, b):
        ans = ('{:X}{:X}{:X}').format(r, g, b)

        while len(ans) < 6:
            ans = "0" + ans

        return "#" + ans

    def get_top_10(hex_list):
        hex_frequency = {}

        for item in hex_list:
            if item in hex_frequency:
                hex_frequency[item] += 1
            else:
                hex_frequency[item] = 1

        sorted_hex = dict(sorted(hex_frequency.items(), key=lambda item: item[1]))

        return list(sorted_hex.keys())[-10:][::-1]

    image_file = Image.open(filepath)
    image_array = np.array(image_file)

    shape = image_array.shape

    x = shape[0]
    y = shape[1]

    hex_list = []
    for x in range(x):
        for y in range(y):
            rgb = image_array[x, y, :]

            r = rgb[0]
            g = rgb[1]
            b = rgb[2]

            hex_list.append(rgb_to_hex(r, g, b))

    top_10_hex = get_top_10(hex_list)

    return top_10_hex


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
            hex_palette = get_colors_in_image(fullpath)
            flash(f"You successfully uploaded {file.filename}")
            return render_template("index.html", image_path=fullpath, got_image=True, top_10_colors=hex_palette)
        elif file and not allowed_file(file.filename):
            flash("You can only upload files with the following extensions: \t"
                  "JPG, JPEG, GIF, PNG")
            return redirect(request.url)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
