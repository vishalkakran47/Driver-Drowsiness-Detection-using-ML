import os
from imutils import face_utils #imutils- basic image processing
from scipy.spatial import distance as dist #scipy - to use mathematical calculations to find distance
import cv2 #opencv Libary
import pyttsx3 #convert text to speech library
import dlib #facial landmarks library

#to retrive or detect face
detectFace = dlib.get_frontal_face_detector() 
#to map face co-ordinates (X,Y)
location =os.path.join('static', 'models/shape_predictor_68_face_landmarks.dat')
faceModel = dlib.shape_predictor(location)

class VideoCamera():        
    def __init__(self):
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        #to plot video frame on html page
        success, image = self.video.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	    # detect faces in the grayscale frame
        facialRectangles = detectFace(gray, 0)

        for i in facialRectangles:
            Deriveshape = faceModel(gray, i)
            Deriveshape = face_utils.shape_to_np(Deriveshape)

            threshTemp = 0.092
            (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
            (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
            lefteyeBall = Deriveshape[lStart:lEnd]
            righteyeBall = Deriveshape[rStart:rEnd]
            
            A = dist.euclidean(lefteyeBall[1], lefteyeBall[5])
            B = dist.euclidean(lefteyeBall[2], lefteyeBall[4])
            C = dist.euclidean(lefteyeBall[0], lefteyeBall[3])
            #eye ratio = EA

            EALeft = (A + B) / (2.0 )

            A = dist.euclidean(righteyeBall[1], righteyeBall[5])
            B = dist.euclidean(righteyeBall[2], righteyeBall[4])
            C = dist.euclidean(righteyeBall[0], righteyeBall[3])
            EARight = (A + B) / (2.0 )

            x = (EALeft + EARight) / 2.0
            #print(x*100)

            if (EALeft + EARight) / 2.0 < threshTemp:
                print((EALeft + EARight) / 2.0)
                cv2.putText(image, "Please Wake up", (90, 90), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 255, 0), 2)
                engine = pyttsx3.init()
                engine.say("Please wake up sir you are sleeping, drive slowly")
                engine.runAndWait()
                print("Alert!! drowsiness is detected")
            else:
                cv2.putText(image, "Hello. you are looking smart!!", (10, 90), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 0, 0), 2)       
            for (x, y) in Deriveshape:
                cv2.circle(image, (x, y), 2, (0,255,0), -1)
        ret, jpeg = cv2.imencode('.jpeg', image)
        return jpeg.tobytes()