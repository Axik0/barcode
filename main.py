from flask import Flask, render_template, request, url_for, flash, redirect
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os

from processor import process, generate_qr


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzzz'
Bootstrap(app)

app.config['UPLOAD_FOLDER'] = 'static/temp'
app.config['MAX_CONTENT_LENGTH'] = 1000*1000*10
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def is_allowed(filename):
    # we check that there is some filename (dot condition) and it's allowed
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


img_path, text = None, None


@app.route("/", methods=['GET', 'POST'])
def index():
    global img_path, text
    if text:
        # remove previous text
        text = None
    elif img_path:
        try:
            # remove previous file from temp folder by its path
            os.remove(img_path)
        except:
            flash("previous temp file doesn't exist or hasn't been removed", 'error')
    if request.method == 'POST':
        action = request.form.get('gen')
        action2 = request.form.get('text_submit')
        if action == 'Generate':
            return render_template("index.html", input_text=True)
        elif action2 == 'Submit':
            text = request.form.get('text')
            if text:
                return redirect(url_for('result'))
            else:
                flash('Please enter something.', 'error')
        else:
            f = request.files['file']
            if f.filename != '':
                if is_allowed(f.filename):
                    img_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
                    f.save(img_path)
                    flash('file uploaded successfully', 'info')
                    return redirect(url_for('result'))
                else:
                    flash('incorrect file', 'error')
            else:
                flash('No selected file', 'error')
    return render_template("index.html")


@app.route("/result")
def result():
    global img_path, text
    if img_path:
        data = process(img_path)
        # d = data["raw_text"] doesn't work!
        qr_path = None
    else:
        data = None
        qr_path = 'static/temp/generated_qr.png'
        with open(qr_path, 'wb') as gen_qr:
            gen_qr.write(generate_qr(text))
    return render_template("result.html", decoded=data, encoded=qr_path)


if __name__ == '__main__':
    app.run()
    debug = True