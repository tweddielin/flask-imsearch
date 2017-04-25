import os
from flask import Flask, render_template, request, jsonify, flash, url_for, redirect, send_from_directory
#from imsearch.colordescriptor import ColorDescriptor
from imsearch.deepfeature import DeepFeature
from imsearch.searcher import Searcher
#from imsearch import imutils
from werkzeug import secure_filename
# create flask instance

UPLOAD_FOLDER = '/home/tweddielin/cbir/flask-imsearch/app/static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'JPG'])
INDEX = os.path.join(os.path.dirname(__file__), 'deep_index.csv')
#INDEX = os.path.join(os.path.dirname(__file__), 'index.csv')
app = Flask(__name__, static_url_path = '', static_folder = "static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
df = DeepFeature()
print INDEX
# main route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":

        RESULTS_ARRAY = []

        # get url
        image_url = '/home/tweddielin/cbir/flask-imsearch/app/static' + request.form.get('img')
        print image_url
        try:
            # Color Descriptor
            # initialize the image descriptor
            #cd = ColorDescriptor((8, 12, 3))

            # load the query image and describe it
            from skimage import io
            print 'skimge loaded'
            #import cv2
            query = io.imread(image_url)
            print "successfully transform query image!"
            query = (query * 255).astype("uint8")
            print 'successfully transform query image from url!'
            #(r, g, b) = cv2.split(query)
            #query = cv2.merge([b, g, r])

            #query = imutils.url_to_image(image_url)
            #features = cd.describe(query)


            # Deep Feature
            #query = imutils.url2image(image_url)
            print 'feature extracting...'
            features = df.describe(image_url)
            print 'feature extracted'
            # perform the search
            print 'performing the search'
            searcher = Searcher(INDEX)
            print 'search done'
            results = searcher.search(features)
            # loop over the results, displaying the score and image name
            for (score, resultID) in results:
                RESULTS_ARRAY.append({"image": str(resultID), "score": str(score)})
            # return success
            print 'success!'
            return jsonify(results=(RESULTS_ARRAY))

        except:

            # return error
            print 'there are some problems'
            return jsonify({"sorry": "Sorry, no results! Please try again."}), 500

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    print "UPLOADING!!!"
    if request.method == 'POST':
        print "POST SUCCESSFULLY!!"
        if 'file' not in request.files:
            print "FILE IS NOT IN REQUEST.FILE!!!"
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            print "FILE NAME IS NULL!!!"
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            print "SAVING!!!"
            filename = secure_filename(file.filename)
            print os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "upload.jpg"))
            #flash("file uploaded successfully!")
            #return redirect(url_for('uploaded_file',filename=filename))
            return render_template('index.html')

@app.route('/static/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

# run!
if __name__ == '__main__':
    app.run()
