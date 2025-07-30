from flask import Flask, render_template, request, send_file
import os
import pdfkit
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
options = { 'enable-local-file-access': None }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form.to_dict()
        photo = request.files.get('photo')
        if photo and photo.filename != '':
            filename = secure_filename(photo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(filepath)
            data['photo_path'] = filepath
        return render_template('resume.html', data=data)
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_pdf():
    data = request.form.to_dict()
    rendered = render_template('resume.html', data=data)
    pdf_path = 'static/generated_resume.pdf'
    pdfkit.from_string(rendered, pdf_path, configuration=config, options=options)
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)