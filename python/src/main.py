import sys

import cv2
import os
# tells environment to not log any warnings and erros
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from keras.models import load_model
sys.stderr = stderr

import numpy as np


from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.inference import load_image
from utils.preprocessor import preprocess_input



def main(image_path) : 
  # parameters for loading data and images
  # image_path = sys.argv[1]
  # ? override path of image if you want to test other image here
  # image_path = '../images/happy.png'
  
  try :
    
    detection_model_path = '../trained_models/detection_models/haarcascade_frontalface_default.xml'
    # emotion_model_path = '../trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
    emotion_model_path = '../trained_models/emotion_models/fer2013_mini_XCEPTION.107-0.66.hdf5'
    gender_model_path = '../trained_models/gender_models/simple_CNN.81-0.96.hdf5'
    emotion_labels = get_labels('fer2013')
    gender_labels = get_labels('imdb')
    font = cv2.FONT_HERSHEY_SIMPLEX

    # hyper-parameters for bounding boxes shape
    gender_offsets = (30, 60)
    gender_offsets = (10, 10)
    emotion_offsets = (20, 40)
    emotion_offsets = (0, 0)

    # loading models
    face_detection = load_detection_model(detection_model_path)
    emotion_classifier = load_model(emotion_model_path, compile=False)
    gender_classifier = load_model(gender_model_path, compile=False)

    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]
    gender_target_size = gender_classifier.input_shape[1:3]
    # loading images
    rgb_image = load_image(image_path, grayscale=False)
    gray_image = load_image(image_path, grayscale=True)
    gray_image = np.squeeze(gray_image)
    gray_image = gray_image.astype('uint8')

    faces = detect_faces(face_detection, gray_image)
    face_type = str(type(faces))
    totalFaces = 0

    if face_type == "<class 'numpy.ndarray'>" :
      totalFaces = (faces.size / 4)
      status = {
        "status" : "face-detected-from-image",
        "totalFaces": totalFaces
      }
      print('**sep**',status,'**sep**')
      if totalFaces == 1 :
        for face_coordinates in faces:
          x1, x2, y1, y2 = apply_offsets(face_coordinates, gender_offsets)
          rgb_face = rgb_image[y1:y2, x1:x2]

          x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
          gray_face = gray_image[y1:y2, x1:x2]

          try:
              rgb_face = cv2.resize(rgb_face, (gender_target_size))
              gray_face = cv2.resize(gray_face, (emotion_target_size))
          except:
              continue

          rgb_face = preprocess_input(rgb_face, False)
          rgb_face = np.expand_dims(rgb_face, 0)
          gender_prediction = gender_classifier.predict(rgb_face)
          gender_label_arg = np.argmax(gender_prediction)
          gender_text = gender_labels[gender_label_arg]

          gray_face = preprocess_input(gray_face, True)
          gray_face = np.expand_dims(gray_face, 0)
          gray_face = np.expand_dims(gray_face, -1)
          emotion_label_arg = np.argmax(emotion_classifier.predict(gray_face))
          emotion_text = emotion_labels[emotion_label_arg]

          if gender_text == gender_labels[0]:
              color = (0, 0, 255)
          else:
              color = (255, 0, 0)

          draw_bounding_box(face_coordinates, rgb_image, color)
          draw_text(face_coordinates, rgb_image, gender_text, color, 0, -20, 1, 2)
          draw_text(face_coordinates, rgb_image, emotion_text, color, 0, -50, 1, 2)

        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite('../images/predicted_test_image.png', bgr_image)

        # print('the emotion in the picture is : ', emotion_text)
        status = {
          "status" : "emotion-detected-from-image",
          "result" : emotion_text
        }
        print(status,'**sep**')

        # print('the gender in the picture is : ', gender_text)
      else:
        status = {
          "status" : "more-than-one-faces-detected",
          "totalFaces": totalFaces
        }
        print(status,'**sep**')
    else: 
      status = {
        "status" : "more-than-one-faces-detected",
        "totalFaces": totalFaces
      }
      print(status,'**sep**')

  except Exception as e:
    print(e)
  

def captureImage():
  key = cv2. waitKey(1)
  webcam = cv2.VideoCapture(0)
  # initially path saved as current directory
  # this path will be appended when the file will be created 
  saved_image_path = os.path.dirname(os.path.abspath(__file__))
  while True:
      try:
          check, frame = webcam.read()
          # print(check) #prints true as long as the webcam is running
          # print(frame) #prints matrix values of each framecd 
          cv2.putText(frame, "Press S to save image", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
          cv2.putText(frame, "Press Q to close and exit", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
          # cv2.putText(frame, "Press Q close and exit", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))
          cv2.imshow("Capturing", frame)
          key = cv2.waitKey(1)
          if key == ord('s'): 
              cv2.imwrite(filename='saved_img.jpg', img=frame)
              webcam.release()
              img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
              img_new = cv2.imshow("Captured Image", img_new)
              cv2.waitKey(1650)
              cv2.destroyAllWindows()
              # print("Processing image...")
              status = {
                "status" : "capturing-image"
              }
              print(status ,'**sep**')
              img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
              # print("Converting RGB image to grayscale...")
              # gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
              # print("Converted RGB image to grayscale...")
              # print("Resizing image to 28x28 scale...")
              # img_ = cv2.resize(gray,(28,28))
              # print("Resized...")
              saved_image_path  += '\saved_img-final.jpg'
              img_resized = cv2.imwrite(filename=saved_image_path, img=img_)
              status = {
                "status" : "image-captured"
              }
              print(status,'**sep**')
          
              break
          elif key == ord('q'):
              # print("Turning off camera.")
              webcam.release()
              # print("Camera off.")
              # print("Program ended.")
              cv2.destroyAllWindows()
              break
          
      except(KeyboardInterrupt):
          # print("Turning off camera.")
          webcam.release()
          # print("Camera off.")
          # print("Program ended.")
          cv2.destroyAllWindows()
          break
  return saved_image_path
    
if __name__ == "__main__":  
  if(len(sys.argv) == 1):
    saved_image_path = captureImage()
    status = {
      "status" : "processing-image",
      "image_path": saved_image_path
    }
    print(status,'**sep**')
    
    main(saved_image_path)
  elif(len(sys.argv) == 2):
    relativeUploadedPath = os.path.abspath(__file__ + '/../../server/' + sys.argv[1]) 
    main(relativeUploadedPath)
  
  # if (isinstance(sys.argv[1], str) ):
  #   print('going with uploaded image')
  # else:
  #   print('need to capture image with webcam')
  # saved_image_path = captureImage() 
  # status = {
  #   "status" : "processing-image",
  #   "image_path": saved_image_path
  # }
  # print(status)
  # main(saved_image_path)