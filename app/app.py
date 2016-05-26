import os
from flask import Flask, render_template, request, jsonify, flash, url_for, redirect
from imsearch.colordescriptor import ColorDescriptor
from imsearch.deepfeature import DeepFeature
from imsearch.searcher import Searcher
from imsearch import imutils
from werkzeug import secure_filename
# create flask instance

UPLOAD_FOLDER = 'static'
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
        image_url = 'static' + request.form.get('img')
        print image_url
        try:
            # Color Descriptor
            # initialize the image descriptor
            #cd = ColorDescriptor((8, 12, 3))

            # load the query image and describe it
            #from skimage import io
            import cv2
            #query = io.imread(image_url)
            #query = (query * 255).astype("uint8")
            #(r, g, b) = cv2.split(query)
            #query = cv2.merge([b, g, r])

            #query = imutils.url_to_image(image_url)
            #features = cd.describe(query)


            # Deep Feature
            query = imutils.url2image(image_url)
            features = df.describe(image_url)

            # perform the search
            searcher = Searcher(INDEX)
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
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'upload.jpg'))
            #flash("file uploaded successfully!")
            return render_template('index.html')


# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
