import utils
import numpy as np
import json

def median_filter(img):
    """
    Implement median filter on the given image.
    Steps:
    (1) Pad the image with zero to ensure that the output is of the same size as the input image.
    (2) Calculate the filtered image.
    Arg: Input image. 
    Return: Filtered image.
    """

    # print(img.shape)
    img_padded = utils.zero_pad(img,1,1)
    # utils.cv2.imshow('res1',img)
    # print(img_padded)
    # utils.cv2.waitKey(0)
    # utils.cv2.destroyAllWindows()
    # print(img_padded.shape)
    temp_img = img

    #median_filtering
    for i in range(len(img_padded)-2):
        for j in range(len(img_padded[1])-2):
            pixel_arr = []
            for k in range(0,3):
                for l in range(0,3):
                    pixel_arr.append(img_padded[i+k][j+l])
            pixel_arr.sort()
            # print(pixel_arr)
            temp_img[i][j] = pixel_arr[4]
    return temp_img

    # utils.cv2.imshow('res1',temp_img)
    # utils.cv2.waitKey(0)
    # utils.cv2.destroyAllWindows()




def mse(img1, img2):
    """
    Calculate mean square error of two images.
    Arg: Two images to be compared.
    Return: Mean square error.
    """    
    # print(img1.shape)
    # print(img2.shape)
    mean = 0.0
    for i in range(len(img1[0])):
        for j in range(len(img1[1])):
            mean += (img1[i][j]-img2[i][j])**2
    mean = mean/(len(img1)*len(img1[1]))

    return mean
    

if __name__ == "__main__":
    img = utils.read_image('lenna-noise.png')
    gt = utils.read_image('lenna-denoise.png')

    result = median_filter(img)
    error = mse(gt, result)

    with open('results/task2.json', "w") as file:
        json.dump(error, file)
    utils.write_image(result,'results/task2_result.jpg')


