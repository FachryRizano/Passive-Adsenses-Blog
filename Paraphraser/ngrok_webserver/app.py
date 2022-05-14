#!/usr/bin/env python3
from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
from Paraphraser.paraphraser import paraphrase_list_article, paraphrase_html
from Article.article_generator import get_article_html
import os
import ssl
from pyngrok import ngrok,  conf, installer

# Config
app = Flask(__name__,template_folder='template')

ALLOWED_EXTENSIONS = ['txt']
app.config['UPLOAD_FOLDER'] = './upload_file'
auth_token = "25S4u3Z68NdRzz9T9AYpx6pknPQ_47ShGUpwzB1ZPTZSr56Jt"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def start_ngrok():
    ngrok.set_auth_token(auth_token)
    pyngrok_config = conf.get_default()
    # Set up a tunnel on port 5000 for our Flask object to interact locally
    if not os.path.exists(pyngrok_config.ngrok_path):
        myssl = ssl.create_default_context();
        myssl.check_hostname=False
        myssl.verify_mode=ssl.CERT_NONE
        installer.install_ngrok(pyngrok_config.ngrok_path, context=myssl)
    url = ngrok.connect(5000).public_url.split("//")[1]
    print(' * Tunnel URL:', url)
    return url

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
            result = paraphrase_list_article(content)
            return result
            
@app.route('/link',methods=['GET','POST'])
def paraphrased_by_link():
    if request.method =='POST':
        article_link = request.form.get('article_link')
        soup = get_article_html(article_link)
        html = paraphrase_html(soup)
        return render_template('paraphrase_link.html',paraphrased_result=html)
    else:
        return render_template('paraphrase_link.html')

if __name__ == "__main__":
    # Setup NGROK
    # url = start_ngrok()
    # app.config["SERVER_NAME"] = url

    app.run(host="0.0.0.0") 