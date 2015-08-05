import cv2
import time
import os
import Adafruit_CharLCD as LCD

#
lcd = LCD.Adafruit_CharLCDPlate()
#

# Get ready to start getting images from the webcam
webcam = cv2.VideoCapture(0)
# Setting capture frame resolution
webcam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320*3.2)
webcam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240*3.2)
#

# frontal face pattern detection
frontalface = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
# profile face pattern detection
profileface = cv2.CascadeClassifier("haarcascade_profileface.xml")

#
face = [0,0,0,0]
Cface = [0,0]
lastface = 0
#

# main
while True:

	faceFound = False
	lcd.set_backlight(0)
	lcd.clear()
	
	if not faceFound:
		if lastface ==0 or lastface ==1:
			# capture multiple times to ensure image is current
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			fface = frontalface.detectMultiScale(aframe,1.3,4,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),(60,60))
			#
			if fface!= ():
				# look for front face in the next iteration
				lastface = 1
				# f in fface is the bounding box for the detected face
				for f in fface:	
					faceFound = True
					face = f
	
	# if a face wasn't found searching for a profile face
	if not faceFound:
		# only attempting if the previous loop was executed
		if lastface == 0 or lastface == 2:				
			# capturing more frames 
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			pface_r = profileface.detectMultiScale(aframe,1.3,4,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),(80,80))
			#
			if pface_r != ():
				# if a profile face was found
				lastface = 2
				for f in pface_r:
					faceFound = True
					face = f

	# final attempt for face search
	if not faceFound:
		# looking for faces turned towards the left
		if lastface == 0 or lastface == 3:
			# refreshing frames again
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			aframe = webcam.read()[1]
			# flipping the captured image for  comparision
			cv2.flip(aframe,1,aframe)
			pface_l = profileface.detectMultiScale(aframe,1.3,4,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),(80,80))
			#
			if pface_l != ():
				# if a left proflie face was found
				lastface = 3
				for f in pface_l:
					faceFound = True
					face = f

	if not faceFound:
		# if nothing was found setting parameters for the next iteration
		lastface = 0
		face = [0,0,0]

	if faceFound:
		# if a face is found send a pushbullet notification
		message = "There is someone in front of me!!!"
		os.system('./pushbullet.sh "%s"'%message)
		lcd.set_backlight(1)
		lcd.message("There is someone\nin front of me!!")
		time.sleep(5)
