import cv2
import numpy as np 
import math
from pynput.keyboard import Key, Controller

 
cv2.namedWindow("Ghassen")
cap = cv2.VideoCapture(2)

if cap.isOpened():
	ret, frame = cap.read()
else:
	ret = False

while ret:
	
	ret, frame = cap.read()
	frame=cv2.flip(frame,1)
	kernel = np.ones((3,3),np.uint8)
	roi = frame[100:300, 100:300]
	cv2.rectangle(frame,(100,100),(300,300),(0,255,0),0)
	hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

	lower_skin = np.array([0,20,70], dtype=np.uint8)
	upper_skin = np.array([20,255,255], dtype=np.uint8)

	mask = cv2.inRange(hsv, lower_skin, upper_skin)
	mask = cv2.dilate(mask,kernel,iterations = 4)
	mask = cv2.GaussianBlur(mask,(5,5),100)
	contours,hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cnt = max(contours, key = lambda x: cv2.contourArea(x))
	epsilon = 0.0005*cv2.arcLength(cnt,True)
	approx= cv2.approxPolyDP(cnt,epsilon,True)
	hull = cv2.convexHull(cnt)

	areahull = cv2.contourArea(hull)
	areacnt = cv2.contourArea(cnt)
	#find the percentage of area not covered by hand in convex hull
	arearatio = ((areahull-areacnt)/areacnt)*100

	#find the defects in convex hull with respect to hand 
	hull = cv2.convexHull(approx, returnPoints=False)
	defects = cv2.convexityDefects(approx, hull)

	l=0

	#for finding no of defecfts due to fingers
	for i in range (defects.shape[0]):
		s,e,f,d = defects[i,0]
		start = tuple(approx[s][0])
		end = tuple(approx[e][0])
		far = tuple(approx[f][0])
		pt= (100,180)

		#find length of all sides of trinagle
		a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
		b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
		c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
		s = (a+b+c)/2
		ar= math.sqrt(s*(s-a)*(s-b)*(s-c))

		#distance between point and convex hull 
		d = (2*ar)/a
		#apply cosine rule here 
		angle = math.acos((b**2 + c**2 - a**2)/(2*b*c))* 57

		#ignore angles > 90 and ignore points very close to convex hull
		if angle <= 90 and d>30:
			l += 1
			cv2.circle(roi, far, 3, [255,0,0], -1)

		#draw lines around hand
		cv2.line(roi,start, end, [0,255,0],2)

	l+=1

	#print corresponding gestures which are intheir ranges
	font = cv2.FONT_HERSHEY_SIMPLEX
	Keyboard = Controller()
	if l==1:
		if areacnt<2000:
			cv2.putText(frame,'Put hand in the box',(0,80),font, 2, (0,0,255),3, cv2.LINE_AA)
		else:
			if arearatio<1:
				cv2.putText(frame,'0',(0,50),font, 2, (0,0,255), 3, cv2.LINE_AA)
			elif arearatio<17.5:
				cv2.putText(frame,'Best of luck',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
			else:
				cv2.putText(frame,'1',(0,50), font, 2, (0,0,255), 3,cv2.LINE_AA)
	elif l==2:
		Keyboard.press(Key.space)
		Keyboard.release(Key.space)
		cv2.putText(frame,'Jump',(0,50), font, 2,(0,0,255), 3, cv2.LINE_AA)

	elif l==3:
		 if arearatio<27:
			 cv2.putText(frame,'3',(0,50),font, 2, (0,0,255), 3, cv2.LINE_AA)
	elif l==4:
		cv2.putText(frame,'4',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
	elif l==5:
		cv2.putText(frame,'5',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
	elif l==6:
		cv2.putText(frame,'6',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
	else:
		cv2.putText(frame,'Reposition',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)


	cv2.imshow("Ghassen", mask)
	cv2.imshow('frame', frame)
 























	key = cv2.waitKey(20)
	if key == 27:
		break
cv2.destroyWindow("ghassen")