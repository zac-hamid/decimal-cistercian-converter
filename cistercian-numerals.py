import enum
import cv2
import numpy as np
import math

class Place(enum.Enum):
	Ones = 1
	Tens = 2
	Hundreds = 3
	Thousands = 4

def main():
	bg, imgs = load_images("./images/")
	print("############################################")
	print("Welcome to the Decimal-Cistercian converter!")
	print("############################################")
	print("\n")
	num_in = int(input("Please enter a number to convert: "))
	print("Converting " + str(num_in) + " to a Cistercian numeral...")

	cistercians = []
	result = num_in
	while result > 0:
		remainder = result % 10000
		result = math.floor(result // 10000)
		cistercians.append(num_to_img(bg, imgs, remainder))

	im = horizontal_stack(cistercians[::-1])
	cv2.namedWindow('Cistercian Representation of ' + str(num_in), cv2.WINDOW_NORMAL)   
	cv2.imshow('Cistercian Representation of ' + str(num_in), im)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def horizontal_stack(img):
	return np.concatenate((img), axis=1)

def num_to_img(bg, imgs, num):
	assert num >= 0 and num < 10000
	im = cv2.bitwise_and(bg, imgs[0])
	num_str = str(num)
	for i in range(len(num_str), 0, -1):
		im = cv2.bitwise_or(im, rotate_image(imgs[int(num_str[len(num_str) - i])], i))
	return 255 - im

def rotate_image(img, place):
	if (place == 1): # Ones position
		return img
	elif (place == 2): # Tens position
		return cv2.flip(img, 1)
	elif (place == 3): # Hundreds position
		return cv2.flip(img, 0)
	elif (place == 4): # Thousands position
		return cv2.flip(cv2.flip(img, 1), 0)
	return img

def load_images(img_path):
	bg = cv2.imread(img_path + "background.png", cv2.IMREAD_UNCHANGED)
	bg = np.asarray(bg, np.float64)
	img = []
	for i in range(10):
		new_img = cv2.imread(img_path + str(i)+"-invert.png", cv2.IMREAD_UNCHANGED)
		new_img = np.asarray(new_img, np.float64)
		img.append(new_img)
	return bg, img

if __name__ == "__main__":
	main()