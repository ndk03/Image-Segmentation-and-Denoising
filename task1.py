import utils
import numpy as np
import json
import time


def kmeans(img,k):
    """
    Implement kmeans clustering on the given image.
    Steps:
    (1) Random initialize the centers.
    (2) Calculate distances and update centers, stop when centers do not change.
    (3) Iterate all initializations and return the best result.
    Arg: Input image;
         Number of K. 
    Return: Clustering center values;
            Clustering labels of all pixels;
            Minimum summation of distance between each pixel and its center.  
    """
    img_copy = img
    #flattening the image to make operations simpler
    img = img.flatten() 
    #to find unique intensity values
    unique_pixels = np.unique(img) 
    #intialising the centers,labels and the distance
    centers = []
    labels = np.zeros(shape = (len(img), 1))
    sumdistance = 2**30
    interations = 0

    #calculate all combination of centroid foe k = 2
    possible_centroids = []
    for i in range(len(unique_pixels)):
    	for j in range(i+1,len(unique_pixels)):
    		possible_centroids.append([unique_pixels[i],unique_pixels[j]])

    while(interations<=500):
        #random selection of from possible centroid list
        c = possible_centroids[np.random.randint(len(possible_centroids))]
        interations+=1
        c1 = c[1] 
        c2 = c[0] 
        l = np.zeros(shape = (len(img), 1))
        sum = 0
        while(True):
            sum = 0 
            pixel_c1 = []
            pixel_c2 = []
            for p in range(len(img)):
                distance1 = abs(float(img[p]) - float(c1))
                distance2 = abs(float(img[p]) - float(c2))

                if(distance1 <= distance2):
                    sum += distance1
                    pixel_c1.append(img[p])
                else:
                    l[p] = 1
                    sum += distance2
                    pixel_c2.append(img[p])
            new_c1 = np.mean(pixel_c1)
            new_c2 = np.mean(pixel_c2)
            #updating the new centroids if the previous value is same as the new value
            if(c1 == new_c1 and c2 == new_c2):
                break
            c1 = new_c1
            c2 = new_c2
        if(sum < sumdistance):
            sumdistance = sum
            labels = l
            centers = [c1, c2]
        	
        labels = labels.reshape(img_copy.shape)
    return centers, labels, sumdistance

def visualize(centers,labels):
    """
    Convert the image to segmentation map replacing each pixel value with its center.
    Arg: Clustering center values;
         Clustering labels of all pixels. 
    Return: Segmentation map.
    """
    for i in range(labels.shape[0]):
    	for j in range(labels.shape[1]):
    		if(labels[i][j] == 0):
    			labels[i][j] = centers[0]/255.0
    		else:
    			labels[i][j] = centers[1]/255.0

    return labels
    
if __name__ == "__main__":
    img = utils.read_image('lenna.png')
    k = 2

    start_time = time.time()
    centers, labels, sumdistance = kmeans(img,k)
    result = visualize(centers, labels)
    end_time = time.time()

    running_time = end_time - start_time
    print(running_time)

    centers = list(centers)
    with open('results/task1.json', "w") as jsonFile:
        jsonFile.write(json.dumps({"centers":centers, "distance":sumdistance, "time":running_time}))
    utils.write_image(result, 'results/task1_result.jpg')
