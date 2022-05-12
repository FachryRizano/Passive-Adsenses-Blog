from flask import Flask, render_template
from flask_ngrok import run_with_ngrok

app = Flask(__name__,template_folder='template')
run_with_ngrok(app)

@app.route('/')
def hello():
    return render_template('index.html')

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
            full_filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], full_filename))
            f.seek(0)
            print("File saved")
            content = f.read()
            content = str(content, 'utf-8')
            return render_template('source.html', text=content)

if __name__ == "__main__":
  app.run()