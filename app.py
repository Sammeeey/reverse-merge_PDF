from flask import Flask, request, send_from_directory, Request

app = Flask(__name__)

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf', 'tif', 'tiff'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.debug = True
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-one', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))    # flask url_for(): https://stackoverflow.com/a/7478705/12946000
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/', methods=['GET', 'POST'])
def upload_multiple():  # flask upload multiple files: https://stackoverflow.com/a/11817318/12946000 & https://youtu.be/krcyh42ShLg & https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
    print(f'request.files: {request.files}')

    upload_files = request.files.getlist("file")
    print(f'upload_files: {upload_files}')

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        for file in upload_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # return redirect(url_for('download_file', name=filename))    # flask url_for(): https://stackoverflow.com/a/7478705/12946000

    # find uploaded files in upload folder
    uploadFileList = findFiles()
    uploadFilenameList = makeFileNameList(uploadFileList)
    sortedFileNameList = sortFileNameList(uploadFilenameList)
    return '''
    <!doctype html>
    <title>Upload new Files</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file multiple>
      <input type=submit value=Upload>
    </form>
    '''

# basically rmPdfScript.py
from rmPDF import *

def findFiles() -> list:
    pdfList = findByCriterions("Bild*.pdf", dirPath=Path(UPLOAD_FOLDER))
    print(f'pdfList: {pdfList}')
    return pdfList

def makeFileNameList(fileList) -> list:
    pdfNameList = []
    for path in fileList:
        pathName = path.name
        pdfNameList.append(pathName)
    print(f'pdfNameList: {pdfNameList}')
    return pdfNameList

def sortFileNameList(fileNameList, toMove='Bild.pdf') -> list:
    # # sort names of pdf files inside list descending (based on integer in file format `Bild (10).pdf` if(!) integer available, else ignore respective item (Bild.pdf)!?)
    # sortedNameList = sorted(fileNameList, key=lambda x: int(x.split('_')[-1].split('.')[0] if '_' in x else 0, reverse=True))
    # Using sorted() function with reverse=True and handling non-digit elements
    sortedNameList = sorted(fileNameList, key=lambda x: int(''.join(filter(str.isdigit, x))) if any(char.isdigit() for char in x) else float('inf'), reverse=True)  # https://chat.openai.com/share/c4b0ab8c-676a-486f-af98-2772d7213b88
    print(sortedNameList)
    # move `Bild.pdf` to end of sorted list manually: https://www.geeksforgeeks.org/python-move-element-to-end-of-the-list/
    try:
        sortedNameList.append(sortedNameList.pop(sortedNameList.index(toMove)))
        print(f'sortedNameList: {sortedNameList}')
    except ValueError as ve:
        print(f'{toMove} not found in sortedNameList.\nFollowing ValueError occured: {ve}')
    return sortedNameList

# reversedNameList = []
# # reverse order of every single pdf
# for pdf in sortedNameList:
#     reversedPdf = reverse(pdf)
#     print(f"Reversed file {pdf} into {reversedPdf}")
#     reversedNameList.append(reversedPdf)
# print(f"Reversed files: {reversedNameList}")

# mergedPdf = merge(reversedNameList)
# print(f"Merged files {reversedNameList} into {mergedPdf}")



# download uploaded file as is: https://stackoverflow.com/a/42137385/12946000
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

# download processed file
@app.route('/uploads/processed/<hash>')
def download_processed(hash):
    return



if __name__ == '__main__':
    app.run(debug=True)