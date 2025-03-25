from flask import Flask, render_template, request, send_file
import json
from PIL import Image
import numpy as np
import cv2
import io


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/', methods=['POST'])
def original():
    file = request.files['file']
    img = Image.open(file)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    file = io.BytesIO(cv2.imencode('.jpg', img)[1])
    return send_file(file, mimetype='image/jpeg')

@app.route('/upload/blur', methods=['POST'])
def blur():
    file = request.files['file']
    img = Image.open(file)
    img = np.array(img)
    img = cv2.GaussianBlur(img, (35, 35), 0)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    file = io.BytesIO(cv2.imencode('.jpg', img)[1])
    return send_file(file, mimetype='image/jpeg')

@app.route('/upload/sharpen', methods=['POST'])
def sharpen():
    file = request.files['file']
    img = Image.open(file)
    img = np.array(img)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    img = cv2.filter2D(img, 5, kernel)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    file = io.BytesIO(cv2.imencode('.jpg', img)[1])
    return send_file(file, mimetype='image/jpeg')


@app.route('/upload/rotate', methods=['POST'])
def rotate():
    file = request.files['file']
    img = Image.open(file)
    img = np.array(img)
    center = (img.shape[1] // 2, img.shape[0] // 2)
    M = cv2.getRotationMatrix2D(center, 45, 1.0)
    img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    file = io.BytesIO(cv2.imencode('.jpg', img)[1])
    return send_file(file, mimetype='image/jpeg')