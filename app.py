from flask import Flask, request, send_from_directory, Request, send_file

app = Flask(__name__)

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ROOT_DIR = os.getcwd()
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
                print(filename)
                uploadFilePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print(uploadFilePath)
                
                savePath = Path(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print(f'savePath: {savePath}')
                file.save(savePath)

                # convert .tiff/.tif to pdf
                try:
                    pdfPath = tiff_to_pdf(str(uploadFilePath))
                    print(f'tif/tiff now {pdfPath}')
                except UnboundLocalError as ule:
                    print(f'{ule}\nno tiff extension (can only be pdf then, because only pdf, tif & tiff allowed)')

        # find uploaded files in upload folder
        uploadFileList = findFiles()    # TODO: can be replaced by using Flask.request.files!?
        uploadFilenameList = makeFileNameList(uploadFileList)   # TODO: can be replaced by using Flask.request.files!?
        sortedFilenameList = sortFileNameList(uploadFilenameList)
        os.chdir(app.config['UPLOAD_FOLDER'])
        reversedFilenameList = reverseFiles(sortedFilenameList)
        resultFileName = 'merged.pdf'
        merge(reversedFilenameList, mergedFileName=resultFileName)
        os.chdir(ROOT_DIR)

        # deleteAndDownload(app.config['UPLOAD_FOLDER'], resultFileName)
        return redirect(url_for('deleteAndDownload', directory=app.config['UPLOAD_FOLDER'], name=resultFileName))    # flask url_for(): https://stackoverflow.com/a/7478705/12946000

    return f'''
    <!doctype html>
    <title>Reverse-Merge PDF's</title>
    <h1>Upload new Files</h1>
    <p>reverses PDFs & eventually merges them into a single, downloadable file (meant to reverse-merge scanned tif-files on Windows)</p>
    <p>only works for unix pattern "Bild*.pdf"</p>
    <p>allowed file types: {ALLOWED_EXTENSIONS}</p>
    <p>if file-type "tif" or "tiff": converts file to PDF</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file multiple>
      <input type=submit value=Upload>
    </form>
    <p>
        <a href="https://github.com/Sammeeey/reverse-merge_PDF" target="_blank">reverse-merge project on Github</a>
    </p>
    '''

# python tiff to pdf inspired by https://stackoverflow.com/a/68336325
from PIL import Image, ImageSequence
import os

def tiff_to_pdf(tiff_path: str) -> str:
    # check if file extension with 1 or 2 ff in .tiff
    twoF = '.tiff' in tiff_path
    # print(f'tiff in path? {twoF}')
    oneF = '.tif' in tiff_path
    # print(f'tif in path? {oneF}')

    if twoF:
        tiffExtension = '.tiff'
    elif oneF:
        tiffExtension = '.tif'

    pdf_path = tiff_path.replace(tiffExtension, '.pdf')
    if not os.path.exists(tiff_path): raise Exception(f'{tiff_path} does not find.')
    image = Image.open(tiff_path)

    images = []
    for i, page in enumerate(ImageSequence.Iterator(image)):
        page = page.convert("RGB")
        images.append(page)
    if len(images) == 1:
        images[0].save(pdf_path)
    else:
        images[0].save(pdf_path, save_all=True,append_images=images[1:])

    # print(images)
    return pdf_path


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

def reverseFiles(sortedNameList, dirPath=Path(UPLOAD_FOLDER)) -> list:
    reversedNameList = []
    # reverse order of every single pdf
    for pdf in sortedNameList:
        reversedPdf = reverse(pdf)
        print(f"Reversed file {pdf} into {reversedPdf}")
        reversedNameList.append(reversedPdf)
    print(f"Reversed files: {reversedNameList}")
    return reversedNameList



import io
import glob

# download uploaded file as is: https://stackoverflow.com/a/42137385/12946000
# delete uploaded files after processing: https://stackoverflow.com/a/59232222/12946000
@app.route('/<directory>/<name>')
def deleteAndDownload(directory, name):   
    filePath = os.path.join(directory, name)
    # save binary of result file
    return_data = io.BytesIO()
    with open(filePath, 'rb') as fo:
        return_data.write(fo.read())
    # (after writing, cursor will be at last byte, so move it to start)
    return_data.seek(0)

    # empty upload directory (delete all files in upload folder) 
    files = glob.glob(directory + '/*')
    for file in files:
        os.remove(file)

    # download saved result file
    return send_file(return_data, mimetype='application/pdf',
                     download_name=name)

    # return send_from_directory(app.config["UPLOAD_FOLDER"], name)


# download processed file
@app.route('/uploads/processed/<hash>')
def download_processed(hash):
    return



if __name__ == '__main__':
    app.run(debug=True)