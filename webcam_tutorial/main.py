import cv2
import cv2
# from simple_facerec import SimpleFacerec
# import face_recognition
import face_recognition

cap = cv2.VideoCapture(0)
~
while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    
    key = cv2.waitKey(1)
    
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()