from RootClass import Root
from Album import Album
import copy
import pygame
from PIL import Image
import os
from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2


class Same:
    items = []
    images = []
    res = {}

    def __init__(self, root):
        if root.Current_Album is None:
            for line in root.Albums:
                for album in line:
                    for list in album.Items:
                        for item in list:
                            self.items.append(item)
        else:
            for list in root.Current_Album.Items:
                for item in list:
                    self.items.append(item)

    def find_same(self):
        for item in self.items:
            image = Image.open(os.getcwd() + "\\" + item.Location + "\\" + item.Name)
            image = image.resize((8, 8), Image.ANTIALIAS)
            image.convert('1')
            pixels = image.load()
            res = 0
            for i in range(8):
                for j in range(8):
                    pix = pixels[i, j]
                    res += (pix[0]*j*i + pix[1]*j*i + pix[2]*j*i)
            self.images.append((item, res, True))
            print(item.Name + "  " + str(res))

    def find_copy(self, per):
        self.find_same()
        #original = cv2.imread("images/jp_gates_original.png")
        #contrast = cv2.imread("images/jp_gates_contrast.png")
        #shopped = cv2.imread("images/jp_gates_photoshopped.png")
        #original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        #contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
        #shopped = cv2.cvtColor(shopped, cv2.COLOR_BGR2GRAY)
        for image in self.images:
            if not self.in_res(image):
                continue
            self.res[image] = []
            image_origin = cv2.imread(os.getcwd() + "\\" + image[0].Location + "\\" + image[0].Name)
            image_origin = cv2.resize(image_origin, (200, 200))
            image_origin = cv2.cvtColor(image_origin, cv2.COLOR_BGR2GRAY)
            for image1 in self.images:
                image1_origin = cv2.imread(os.getcwd() + "\\" + image1[0].Location + "\\" + image1[0].Name)
                image1_origin = cv2.resize(image1_origin, (200, 200))
                image1_origin = cv2.cvtColor(image1_origin, cv2.COLOR_BGR2GRAY)
                res = ssim(image_origin, image1_origin)
                print(res)
                if image1[2] and res >= 1 - per:
                    self.res[image].append(image1)

    def in_res(self, item):
        for key in self.res.keys():
            if key == item:
                return False
            for i in self.res[key]:
                if i == item:
                    return False
        return True




    def mse(self, imageA, imageB):
        print(type(imageA))
        # the 'Mean Squared Error' between the two images is the
        # sum of the squared difference between the two images;
        # NOTE: the two images must have the same dimension
        err = np.sum((imageA.astype('float') - imageB.astype('float')) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])

        # return the MSE, the lower the error, the more "similar"
        # the two images are
        return err

    def compare_images(self, imageA, imageB, title):
        # compute the mean squared error and structural similarity
        # index for the images
        m = mse(imageA, imageB)
        s = ssim(imageA, imageB)

        # setup the figure
        fig = plt.figure(title)
        plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))

        # show first image
        ax = fig.add_subplot(1, 2, 1)
        plt.imshow(imageA, cmap=plt.cm.gray)
        plt.axis("off")

        # show the second image
        ax = fig.add_subplot(1, 2, 2)
        plt.imshow(imageB, cmap=plt.cm.gray)
        plt.axis("off")

        # show the images
        plt.show()

