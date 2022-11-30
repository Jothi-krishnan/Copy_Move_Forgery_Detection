import numpy as np
from sklearn.decomposition import PCA

class subBlock(object):
    def __init__(self, grayscale_img_block, rgb_img_block, x, y, block_size):
            #This class initialises with a RBG image and a grayscale image along with the pixel point (x, y) of the original image
        self.grayscale_img = grayscale_img_block  
        self.grayscale_values = self.grayscale_img.load()

        if rgb_img_block is not None:       # If the orginal image is RBG
            self.rgb_img = rgb_img_block
            self.rgb_values = self.rgb_img.load()
            self.is_rgb = True
        else:           #If the original image is a grayscale image
            self.is_rgb = False

        self.coordinate = (x, y)
        self.block_size = block_size

    def compute_block_data(self):
            #This function computes the feature vector of the given sub block
        block_data_list = []
        block_data_list.append(self.coordinate)
        block_data_list.append(self.compute_characteristic_features(precision=4))
        block_data_list.append(self.compute_pca(precision=6))
        return block_data_list

    def compute_characteristic_features(self, precision):

        characteristic_feature_list = []

        #Compute c1, c2, c3 according to the image's R, G and B color plane 

        if self.is_rgb:
            R_sum = 0
            G_sum = 0
            B_sum = 0
            for y in range(0, self.block_size):  # sum of the each pixel value
                for x in range(0, self.block_size):
                    r, g, b = self.rgb_values[x, y]
                    R_sum += r
                    G_sum += g
                    B_sum += b

            total_pixels = self.block_size * self.block_size
            c1 = R_sum / (total_pixels)  # c1, c2 and c3 stores the mean from each of the colorspaces
            c2 = G_sum / (total_pixels)
            c3 = B_sum / (total_pixels)

            #appending the values c1, c2 and c3 to the list "characteristic_feature_list"
            characteristic_feature_list.append(c1)
            characteristic_feature_list.append(c2)
            characteristic_feature_list.append(c3)

        else:
            #if our image is a grayscale image
            characteristic_feature_list.append(0)
            characteristic_feature_list.append(0)
            characteristic_feature_list.append(0)

        
        # variable to compute characteristic features
        c4_part1 = 0
        c4_part2 = 0
        c5_part1 = 0
        c5_part2 = 0
        c6_part1 = 0
        c6_part2 = 0
        c7_part1 = 0
        c7_part2 = 0


        #Computing  c4, c5, c6 and c7 
        for y in range(0, self.block_size):  # compute the part 1 and part 2 of each feature characteristic
            for x in range(0, self.block_size):
                r, g, b = self.rgb_values[x, y]
                # compute c4
                if y <= self.block_size / 2:
                    c4_part1 += self.grayscale_values[x, y]
                else:
                    c4_part2 += self.grayscale_values[x, y]
               #compute c5
                if x <= self.block_size / 2:
                    c5_part1 += self.grayscale_values[x, y]
                else:
                    c5_part2 += self.grayscale_values[x, y]
                #compute c6
                if x - y >= 0:
                    c6_part1 += self.grayscale_values[x, y]
                else:
                    c6_part2 += self.grayscale_values[x, y]
                #compute c7
                if x + y <= self.block_size:
                    c7_part1 += self.grayscale_values[x, y]
                else:
                    c7_part2 += self.grayscale_values[x, y]

        c4 = float(c4_part1)/float(c4_part1 + c4_part2)
        c5 = float(c5_part1)/float(c5_part1 + c5_part2)
        c6 = float(c6_part1)/float(c6_part1 + c6_part2)
        c7 = float(c7_part1)/float(c7_part1 + c7_part2)
        characteristic_feature_list.append(c4)
        characteristic_feature_list.append(c5)
        characteristic_feature_list.append(c6)
        characteristic_feature_list.append(c7)

        # precise_result = [round(element, precision) for element in characteristic_feature_list]
        precise_values = []
        for elem in characteristic_feature_list:
            precise_values.append(round(elem, precision))
        return precise_values

    def compute_pca(self, precision):

        pca_module = PCA(n_components=1)
        if self.is_rgb:
            image_array = np.array(self.rgb_img)    #image_array is a 3d matrix with 3 different planes R, G and B
            red_plane = image_array[:, :, 0]        #red_plane is a 2d matrix that has the R component of each of the pixel of the image
            green_plane = image_array[:, :, 1]      #green_plane is a 2d matrix that has the G component of each of the pixel of the image
            blue_plane = image_array[:, :, 2]       #blue_plane is a 2d matrix that has the B component of each of the pixel of the image

            transformed_array = np.concatenate((red_plane, np.concatenate((green_plane, blue_plane), axis=0)), axis=0)
            pca_module.fit_transform(transformed_array)
            PCA_components = pca_module.components_
        
            #storing the final values in a list
            precise_values = []
            for elem in list(PCA_components.flatten()):
                precise_values.append(round(elem, precision))

            return precise_values

        else:
            #If the given image is a grayscale image
            image_array = np.array(self.grayscale_img)
            pca_module.fit_transform(image_array)
            PCA_components = pca_module.components_
            
            #storing the final values in a list
            precise_values = []
            for elem in list(PCA_components.flatten()):
                precise_values.append(round(elem, precision))

            return precise_values

    
  
        