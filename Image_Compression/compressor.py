# Author: Alfredo Mejia
# Date  : 11/15/20
# Assign: Assignment 5
# Class : CS 6375.001
# Descrp: This program will use K-means clustering for image compression. This program will accept two arguments, one
#         for the name of the image and the other for the value of K. The second argument is optional as the default
#         values will be 2, 5, 10, 15, 20. It will first get K random RGB values, then it will use the squared euclidean
#         distance to create K clusters of RGB values. It will recalculate the mean and reform the K clusters. This will
#         repeat until the number of iterations is finished. In the end, the image will only contain K colors. It will
#         then display the image(s) to the same directory after data compression.
#
# Note  : The program will produce a warning due to overflow but numpy takes care of this, so everything is fine.
#######################################################################################################################

# Imports
from matplotlib import pyplot as io
import numpy as np
from PIL import Image
import sys
from random import randint


# Funct: Main
# Descr: This is the main method which performs k-means clustering. It accepts two arguments, one for the name of the
#         file and the other for the value of k
def main(filename, k_value):
    # Try to open the file and try to convert the k-value into an integer
    try:
        # Image to array
        img = io.imread(filename, format="png").copy()
        img = img * 255
        print(img)
        # String to int
        k_value = int(k_value)

    # Exit program if error occurs
    except Exception as e:
        print(e)
        sys.exit(-1)

    # Get K random means (RGB values)
    k_means = [img[randint(0, len(img) - 1)][randint(0, len(img[1]) - 1)] for i in range(k_value)]
    print(k_means)

    # For 10 iterations
    for i in range(10):
        # Create new clusters
        clusters = [[] for i in range(k_value)]

        # Create new image to output
        new_image = []

        # For each row in the image array
        for row_i in range(len(img)):
            # Create a new row in the output image
            new_image.append([])

            # For each pixel in the row of the input image
            for col_i, pix in enumerate(img[row_i]):
                # Calculate the squared euclidean
                k_dist = [((pix[0] - k[0]) ** 2 + (pix[1] - k[1]) ** 2 + (pix[2] - k[2]) ** 2) for k in k_means]

                # Get the smallest distance
                k_mean_index = k_dist.index(min(k_dist))

                # Append the pixel to the appropriate cluster
                clusters[k_mean_index].append(pix)

                # Add the k-mean value to the new image in the same position as the current pixel
                new_image[row_i].append(k_means[k_mean_index])

        # Aggregate the sums for each R, G, and B value for each cluster
        total_sum = [[sum(i) for i in zip(*group)] for group in clusters]

        # Get the mean for each R, G, and B value for each cluster
        new_k = [[round(total_sum[i][j] / len(clusters[i])) for j in range(len(total_sum[i]))] for i in
                   range(len(total_sum))]

        # If a cluster has an empty mean due to the cluster being empty then just add its previous mean
        new_k_means = [new_k[i] if len(new_k[i]) > 0 else k_means[i] for i in range(len(new_k))]

        # Update k_means for next iteration
        k_means = new_k_means

        print(k_means)

    # Output image
    output_img = Image.fromarray(np.array(new_image, dtype=np.uint8))
    output_img.save(filename[:-4] + "_Result_" + str(k_value) + "_Means.png")

