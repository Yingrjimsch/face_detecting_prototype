#!/usr/bin/env python3

import requests
import json
import cv2
import numpy as np
import base64

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
face_detected = None

def main(img, gallery_name):
    url = 'https://api.kairos.com/recognize'
    headers = {
			'Content-Type' : 'application/json',
            'app_id' :  'id',
            'app_key' : 'key' }
			
    body = {
            'image': img,
            'gallery_name': gallery_name }

    r = requests.post(url, headers=headers, json=body)
    d = json.loads(r.text)
    print(r.json()['images'][0]['transaction']['subject_id'])
    return r.json()['images'][0]['transaction']['status'] == 'success' if True else False 
    #print(r.text)
	
def opencv():
	while True: 
		ret, img = cap.read()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		if len(faces) != 0:
			cv2.imwrite('face.png',img)
			if main(convertImage(img), 'realfaces'):
				break
		
		cv2.imshow('img',img)	
		k = cv2.waitKey(30) & 0xff
		if k == 27:
			break
			
	cap.release()
	cv2.destroyAllWindows()

def convertImage(img):
	ret, buffer = cv2.imencode('.jpg', img)
	returnimage = base64.b64encode(buffer).decode('ascii')
	return returnimage
	
if __name__ == '__main__':
    opencv()