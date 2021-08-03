from flask import Flask
from flask import request

import cv2
import mediapipe as mp
from os.path import exists
import sys
import os

import datetime;


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return "HI"


@app.route("/video", methods=['POST'])
def uploadVideo():
    raw_data = request.get_data()

    timestamp = str(round(datetime.datetime.now().timestamp()))
    print(timestamp)

    path = "./uploads/{timestamp}.mp4"

    f = open(path, 'wb')    
    f.write(raw_data)
    f.close()

    return createCSV(path)




def createCSV(videoFilePath):
    output = ''
    try:
        cap = cv2.VideoCapture(videoFilePath)
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        mp_holistic = mp.solutions.holistic
        frame = 0
        with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:

            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    cap.release()
                    return output
                
                # Flip the image horizontally for a later selfie-view display, and convert
                # the BGR image to RGB.
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                results = pose.process(image)

                # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                templist=[]

                if results.pose_landmarks != None:
                    for i in range (33):
                        x = results.pose_landmarks.landmark[i].x
                        y = results.pose_landmarks.landmark[i].y
                        z = results.pose_landmarks.landmark[i].z
                        line = '%d,%d,%f,%f,%f\n' % (frame,i,x,y,z)
                        output += line
                frame += 1

    except cv2.error as e:
        return "Couldn't read the file"

  

if __name__ == '__main__':
    app.run(host='0.0.0.0')