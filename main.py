from time import sleep
import cv2
import threading
import mediapipe as mp
import pyautogui
from decimal import Decimal
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
nextx=0.0
counter=0
current=0.0

def func1():
   x,y = pyautogui.position()
   pyautogui.keyDown("w")
   pyautogui.keyDown("g")
   #pyautogui.dragTo(x,y,0.6)
   print(nextx)
   """
   if current-nextx>0:
     pyautogui.moveTo(x-nextx, y)
     pyautogui.mouseDown(x-nextx, y,button="left",duration=0.6)
     pyautogui.mouseUp(button="left")
   else:
     pyautogui.moveTo(x+nextx, y)
     pyautogui.mouseDown(x+nextx, y,button="left",duration=0.6)
     pyautogui.mouseUp(button="left")
    """

def func2():
   x,y = pyautogui.position()
   pyautogui.keyUp("w")
   pyautogui.keyUp("g")

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    prev = 0.0
    next = 0.0
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        next = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * 100
        nextx = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * 100
        if counter==0:
          current=nextx
        counter=counter+1
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

    if next>50 and next<60:
      t1 = threading.Thread(target=func1)
      t1.start()
    else:
      t2 = threading.Thread(target=func2)
      t2.start()
      #pyautogui.moveRel(0, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * 100, duration = 0.2)
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    #pyautogui.typewrite("w")
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
