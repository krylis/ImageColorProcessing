import numpy as np
from PIL import Image
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD FOLDER'] = '/Images/'
app.config['MAX_CONTENT_PATH'] = 10000000


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/submit', methods=["GET", "POST"])
def submit():
    if request.method == "POST:
        f = request.files['file']
        filename = secure_filename(f.filename)

    if len(filename) > 1:
        fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(fullpath)
        palette_hex, palette_rgb = get_colors_in_image(full_path)
        return render_template("index.html", hex_success=True, palette_hex=palette_hex, palette_rgb=palette_rgb)

    return render_template("index.html")
