import numpy as np
import cv2
import urllib
from skimage import io

def translate(image,x,y):
	M = np.float32([[1,0,x],[0,1,y]])
	shifted = cv2.warpAffine(image,M,(image.shape[1],image.shape[0]))
	return shifted


def rotate(image,angle,center = None, scale=1.0):
	(h,w) = image.shape[:2]

	if center is None:
		center = (w/2,h/2)

	M = cv2.getRotationMatrix2D(center,angle,scale)
	rotated = cv2.warpAffine(image,M,(w,h))

	return rotated


def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
	dim = None
	(h,w) = image.shape[:2]

	if width is None and height is None:
		return image

	if width is None:
		r = height/float(h)
		dim = (int(w*r),height)
	else:
		r = width/float(w)
		dim = (width,int(h*r))

	resized = cv2.resize(image, dim, interpolation =inter)
	return resized

def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	# return the image
	return image

def url2image(url):
	image = io.imread(url)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	return image



