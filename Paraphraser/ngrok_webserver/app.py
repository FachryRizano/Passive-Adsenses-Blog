#!/usr/bin/env python3
from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
from Paraphraser.paraphraser import paraphrased_list_article
import os


app = Flask(__name__,template_folder='template')
app.config['UPLOAD_FOLDER'] = './upload_file'
run_with_ngrok(app)
ALLOWED_EXTENSIONS = ['txt']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/paraphrased', methods = ['GET', 'POST'])
def upload_source():
    if request.method == 'POST':
        # check if the post request has the file part
        f = request.files['file']
        if f.filename == "":
            print("No file Name")
            return redirect(request.url)
        if not allowed_file(f.filename):
            print("File extension not allowed!")
            return redirect(request.url)
        else:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            f.seek(0)
            print("File saved")
            content = f.read()
            content = str(content, 'utf-8')
            print('Paraphrasing text...')
            result = paraphrased_list_article(content)
            return result

if __name__ == "__main__":
  app.run()