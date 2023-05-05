from flask import Blueprint, request, redirect, url_for, current_app
from helper import get_secure_filename_filepath, download_from_s3
from PIL import Image
import os 
from os.path import basename
from datetime import datetime
from zipfile import ZipFile
import shutil
import boto3 

bp = Blueprint('android', __name__, url_prefix='/android')

ICON_SIZES = [29, 40, 58, 80, 87, 114, 120, 180, 1024] 


@bp.route('/', methods=['POST'])
def upload_image(): 
    filename= request.json['filename']
    filename, filepath = get_secure_filename_filepath(filename) 

    temp_folder = os.path.join(current_app.config['DOWNLOAD_FOLDER'], 'temp')
    os.makedirs(temp_folder) 

    for size in ICON_SIZES: 
        outfile = os.path.join(temp_folder, f'{size}.png')
        # image = Image.open(filepath)
        file_stream = download_from_s3(filename)
        image = Image.open(file_stream) 
        out = image.resize((size, size))
        out.save(outfile, 'PNG') 

    now = datetime.now() 
    timestamp = str(datetime.timestamp(now)).rsplit('.')[0] 
    zipfilename = f'{timestamp}.zip' 
    zipfilepath = os.path.join(current_app.config['DOWNLOAD_FOLDER'], zipfilename) 

    with ZipFile(zipfilepath, 'w') as zipobj: 
        for foldername , subfolder, filenames , in  os.walk(temp_folder): 
            for filename in filenames: 
                filepath = os.path.join(foldername, filename)
                zipobj.write(filepath, basename(filepath)) 
        shutil.rmtree(temp_folder) 
        return redirect(url_for('download_file', name=zipfilename))



