import numpy as np
import cv2
from imutils.video import VideoStream
import imutils

"""
    This is the basic vision impairment model
    the steps are:
    1. get the original image.
    2. Use the Gaussian filter to blur it.
    3. Add black ellipse on the center of the blurred image.
    4. Copy the original image.
    5. Add normal view ellipse to the original image and convert everything else to black.
    6. Now, you have 2 images, one (step 3) is a blurry image with black ellipse in the center, the other one
    (step 5) is black with same normal ellipse in the center.
    7. Use bitwise_or to blend these two images together.

"""
vs = cv2.VideoCapture("example3.mp4")
while(True):
    image= vs.read()[1]
    image = imutils.resize(image, width=600, height=600)

    # Load original image
    # -1 loads as-is so if it will be 3 or 4 channel as the original
    #image = cv2.imread('./example_06.jpg', -1)
    
    cv2.imshow("original",image)

    #blur the original image using gaussian filter
    # you can increase/decrease the level of bluriness by changing the kernel size. ksize.width and ksize.height can differ but they both must be positive and odd (second argument)
    blure=cv2.GaussianBlur(image,(15,15),9)
    # now, its time to prepare the black ellipse on the blurry image
    image2=blure.copy()
    # get the size for the image to put the ellipse in the middle
    (h, w) = image.shape[:2]
    centerx=int(w/2)
    centery=int(h/2)
    #you can customize the ellipse by changing its center (second argument) and its dimentions (thired )
    cv2.ellipse(image2, (centerx,centery),(100,60),0.0,0.0,360,(0,0,0),-1)
    #cv2.imshow("black ellipse on image",image2)


    # now, its time to create the black image with normal vision ellipse in the middle
    # mask defaulting to black for 3-channel and transparent for 4-channel
    # (of course replace corners with yours)
    mask = np.zeros(image.shape, dtype=np.uint8)
    cv2.ellipse(mask, (centerx,centery),(100,60),0.0,0.0,360,(255,255,255),-1)
    masked_image = cv2.bitwise_and(image, mask)


    #cv2.imshow("mask2",mask2)

    # apply the mask

    #masked_image2 = cv2.bitwise_or(blure, masked_image)
    masked_image3 = cv2.bitwise_or(image2, masked_image)

    #cv2.imshow("masked",masked_image)
    cv2.imshow("result",masked_image3)

    #cv2.imshow("masked2",masked_image2)
    #cv2.imwrite('image_masked.png', masked_image)
    #cv2.waitKey(0)
    key = cv2.waitKey(10) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
vs.stop()
