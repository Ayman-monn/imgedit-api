from flask import Blueprint, request, jsonify, redirect, url_for, current_app
from PIL import Image
from helper import get_secure_filename_filepath, download_from_s3
import os 


bp = Blueprint('actions', __name__, url_prefix='/actions')


@bp.route('/resize', methods=['POST'])
def resize(): 
    filename = request.json['filename']
    filename, filepath = get_secure_filename_filepath(filename) 

    try:
        width, height = int(request.json['width']), int(request.json['height'])
        file_stream =  download_from_s3(filename) 
        # image =Image.open(filepath) 
        image =Image.open(file_stream)  
        out = image.resize((width, height))
        out.save(os.path.join(current_app.config['DOWNLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', name=filename)) 
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404 
        

@bp.route('/presets/<preset>', methods=['POST'])
def resize_preset(preset): 
    prests = {'small': (640, 400), 'medium': (1280, 960), 'large': (1600, 1200)}
    if preset not in prests: 
        return jsonify({'message': 'The prest is not available'})
    
    filename = request.json['filename']
    filename, filepath = get_secure_filename_filepath(filename) 
    try: 
        size = prests[preset]
        file_stream = download_from_s3(filename) 
        # image =Image.open(filepath) 
        image = Image.open(file_stream)
        out = image.resize(size) 
        # out.save(filepath)
        out.save(os.path.join(current_app.config['DOWNLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', name=filename))
    except FileNotFoundError: 
        return jsonify({'message': 'File not found'}), 404 
    


@bp.route('/rotate', methods=['POST'])
def rotate(): 
    filename = request.json['filename']
    filename, filepath = get_secure_filename_filepath(filename) 
    try:
        degree = float(request.json['degree'])
        # image = Image.open(filepath) 
        file_stream = download_from_s3(filename) 
        image = Image.open(file_stream) 
        out =image.rotate(degree) 
        # out.save(filepath)
        out.save(os.path.join(current_app.config['DOWNLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', name=filename))
    except FileNotFoundError: 
        return jsonify({'message': 'File not found'}), 404
    
@bp.route('/flip', methods=['POST'])
def flip(): 
    filename = request.json['filename'] 
    filename, filepath = get_secure_filename_filepath(filename) 

    try: 
        # image = Image.open(filepath)
        file_stream = download_from_s3(filename)
        image= Image.open(file_stream)   
        out = None
        if request.json['decoration'] =="horizental": 
            out = image.transpose(Image.FLIP_TOP_BOTTOM)
        else: 
            out = image.transpose(Image.FLIP_LEFT_RIGHT)
        # out.save(filepath) 
        out.save(os.path.join(current_app.config['DOWNLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', name=filename)) 
    except FileNotFoundError: 
        return jsonify({'message':'File not found. '}), 404

