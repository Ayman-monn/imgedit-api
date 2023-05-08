from flask import Flask,jsonify, request, send_from_directory, current_app
from actions import bp as actionsbp
from filters import bp as filtersbp
from android import bp as androidbp 
from helper import allowed_extension, get_secure_filename_filepath, uploat_to_s3
import boto3

UPLOAD_FOLDER='uploads/'
DOWNLOAD_FOLDER='downloads/'
ALLOWED_EXTENSION = ['png', 'jpg', 'jpeg']
app = Flask(__name__) 

app.secret_key = 'SECERT_KEY' 

app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER']= DOWNLOAD_FOLDER
app.config['ALLOWED_EXTENSION']= ALLOWED_EXTENSION

app.config['S3_BUCKET']= 'imgedit-api-bucket'
app.config['S3_KEY']= 'AKIAX4CPVG77XW5V4LNP'
app.config['S3_SECRET']= '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'
app.config['S3_LOCATION']='https://imgedit-api-bucket.s3.eu-central-1.amazonaws.com/upload/' 

app.register_blueprint(actionsbp)
app.register_blueprint(filtersbp)
app.register_blueprint(androidbp)


@app.route('/')
def index(): 
    return jsonify({
        'message': 'Welcome to Images API .'
    })


@app.route('/images', methods=['GET', 'POST'])
def images(): 
    if request.method == 'POST': 
        if 'file' not in request.files: 
            return jsonify({'error':'No file was selected'}), 400 
        file = request.files['file']

        if file.filename =='': 
            return jsonify({'error':'No file was selected'}), 400
        
        if not allowed_extension(file.filename): 
            return jsonify({'error': 'The extension is not supported . '}), 400
        
        # filename, filepath =get_secure_filename_filepath(file.filename) 
        output = uploat_to_s3(file, app.config['S3_BUCKET'])
        # file.save(filepath) 
        return jsonify({
            'message': 'File successfully uploaded',
            'filename':output
        }), 201

    # images=[]
    # s3_resource = boto3.resource('s3', aws_access_key_id=current_app.config['S3_KEY'], aws_secret_access_key=current_app.config['S3_SECRET'])
    # s3_bucket = s3_resource.Bucket(current_app.config['S3_BUCKET'])
    # for object in s3_bucket.objects.all(): 
    #     images.append(object.key) 
    # return jsonify({"data": images}), 200  
    
    images=[] 
    s3_resource = boto3.resource('s3', aws_access_key_id=current_app.config['S3_KEY'], aws_secret_access_key=current_app.config['S3_SECRET'])
    s3_bucket = s3_resource.Bucket(current_app.config['S3_BUCKET']) 
    for obj in s3_bucket.objects.filter(Prefix='upload/'):
        if obj.key =='upload/': 
            continue 
        images.append (obj.key) 
    return jsonify({"data": images}), 200 




@app.route('/downloads/<name>')
def download_file(name): 
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], name)



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))