import enum
import cv2
import numpy as np
import math

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

	# Convert base-10 number into base-10000 and construct images for each numeral
	while result > 0:
		remainder = result % 10000
		result = math.floor(result // 10000)
		cistercians.append(num_to_img(bg, imgs, remainder))

	im = image_resize(horizontal_stack(cistercians[::-1]), height = 250)
	cv2.imshow('Cistercian Representation of ' + str(num_in), im)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

# Horizontally stack images so that we can display all Cistercian numerals
def horizontal_stack(img):
	return np.concatenate((img), axis=1)

# Convert a base-10000 number to a Cistercian numeral image
def num_to_img(bg, imgs, num):
	assert num >= 0 and num < 10000
	# Base image, made up of a white background and "stem" (which the numbers will branch off of)
	im = cv2.bitwise_and(bg, imgs[0])
	num_str = str(num)
	# Build up the numeral image by going from right to left of the number so "953", we would add the "3" to the image
	# then the "5", etc. rotating as required.
	for i in range(len(num_str), 0, -1):
		im = cv2.bitwise_or(im, rotate_image(imgs[int(num_str[len(num_str) - i])], i))
	return 255 - im

# Rotate a specific Cistercian number (0-9) to the correct position depending on if it's a ones,
# tens, hundreds, or thousands position, used to build the "components" of a Cistercian numeral
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

# Resize an image while maintaining aspect ratio (if either width or height are not specified)
# Taken from: https://stackoverflow.com/a/44659589
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized


# Load background, "stem", and numeral images used to construct the Cistercian numerals
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