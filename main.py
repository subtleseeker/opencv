import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

subjects = ["", "Shahrukh Khan", "Aamir Khan"]


def detect_face(img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascades/lbpcascade_frontalface.xml')
	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
	if len(faces)==0:
		return None, None

	(x,y,w,h) = faces[0]
	return gray[y:y+w, x:x+h], faces[0]


def prepare_training_data(data_folder_path):
	dirs = os.listdir(data_folder_path)
	faces=[]
	labels=[]

	for dir_name in dirs:
		if not dir_name.startswith("s"):
			continue
		label = int(dir_name.replace("s",""))
		subject_dir_path = data_folder_path+"/"+dir_name
		subject_images_names = os.listdir(subject_dir_path)

		for image_name in subject_images_names:
			if image_name.startswith("."):
				continue
			image_path = subject_dir_path + "/" + image_name
			image = cv2.imread(image_path)
			cv2.imshow("Training...", image)
			cv2.waitKey(100)

			face, rect = detect_face(image)
			if face is not None:
				faces.append(face)
				labels.append(label)

	# cv2.destoryAllWindows()
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	return faces, labels


print("Preparing data...")
faces, labels = prepare_training_data("training-data")
print("Data prepared")
print("Total faces: "+ str(len(faces)))
print("Total labels: "+ str(len(labels)))

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(faces, np.array(labels))

def draw_rectangle(img, rect):
	(x,y,w,h) = rect
	cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)


def draw_text(img, text, x, y):
	cv2.putText(img, text, (x,y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,255,0), 2)


def predict(test_img):
	img = test_img.copy()
	face, rect = detect_face(img)
	label = face_recognizer.predict(face)

	print label

	label_text = subjects[label[0]]
	draw_rectangle(img, rect)
	draw_text(img, label_text, rect[0], rect[1]-5)
	return img

test_img1 = cv2.imread("test_data/srk.jpeg")
test_img2 = cv2.imread("test_data/aamir.jpeg")

predicted_img1 = predict(test_img1)
predicted_img2 = predict(test_img2)
print("Prediction complete.")

cv2.imshow("SRK test", predicted_img1)
cv2.imshow("Aamir test", predicted_img2)
cv2.waitKey(0)
cv2.destroyAllWindows()