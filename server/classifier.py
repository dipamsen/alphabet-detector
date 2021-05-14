import cv2
import pickle
from PIL import Image
import PIL.ImageOps
import numpy as np

# LOAD PRE-TRAINED MODEL FROM FILE
model = pickle.load(open("model.lr", 'rb'))


cap = cv2.VideoCapture(0)
print("camera started")
while(True):
  try:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    height, width = gray.shape
    upper_left = (int(width / 2 - 60), int(height / 2 - 40))
    bottom_right = (int(width / 2 + 60), int(height / 2 + 40))
    cv2.rectangle(gray, upper_left, bottom_right, (0, 255, 0), 2)

    # SELECT ONLY NEEDED PART
    roi = gray[upper_left[1]:bottom_right[1], upper_left[0]:bottom_right[0]]

    # CREATE PIL IMAGE
    im_pil = Image.fromarray(roi)

    # CONVERT THE IMAGE TO MODEL-READABLE array
    image_bw = im_pil.convert('L')
    image_bw_resized = image_bw.resize((22, 30), Image.ANTIALIAS)
    image_bw_resized_inverted = PIL.ImageOps.invert(image_bw_resized)
    pixel_filter = 20
    min_pixel = np.percentile(image_bw_resized_inverted, pixel_filter)
    image_bw_resized_inverted_scaled = np.clip(
        image_bw_resized_inverted - min_pixel, 0, 255)
    max_pixel = np.max(image_bw_resized_inverted)

    image_bw_resized_inverted_scaled = np.asarray(
        image_bw_resized_inverted_scaled) / max_pixel

    test_sample = np.array(image_bw_resized_inverted_scaled).reshape(1, 660)
    # PREDICT
    test_pred = model.predict(test_sample)
    print("Predicted class is: ", test_pred)

    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  except Exception as e:
    print(e)
    pass
cap.release()
cv2.destroyAllWindows()
