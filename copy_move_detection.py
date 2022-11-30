from sub_block import subBlock

from PIL import Image
from threading import Thread
import numpy as np
import imageio
import tqdm
import math
import time

class Box(object):
    # This is a class to store the feature vectors 
    def __init__(self):
        self.container = []
        return

    def get_length(self):
        return self.container.__len__()

    def append_block(self, newData):
        self.container.append(newData)
        return

    def sort_by_features(self):
        self.container = sorted(self.container, key=lambda x:(x[1], x[2]))
        return


class CM_Detection(object):
    def __init__(self, input_img_path, img_name, output_path, block_size):
        
        # Threshold values from the research paper "Robust Detection of Region-Duplication Forgery in Digital Image"
        self.P = (1.80, 1.80, 1.80, 0.0125, 0.0125, 0.0125, 0.0125)
        self.t1 = 2.80
        self.t2 = 0.02


        print("Detected image: ", img_name)
        print("Parameters and variables initialization.... ")

        # image parameter
        self.img_output_path = output_path
        self.img_name = img_name
        self.img = Image.open(input_img_path)
        self.img_width, self.img_height = self.img.size  

        if self.img.mode != 'L':  # The given image is not grayscale
            self.is_rgb = True
            self.img = self.img.convert('RGB')      #converting from BGR to RGB
            rgb_values = self.img.load()
            self.grayscale_img = self.img.convert('L')  # creates a grayscale version of current image to be used later
            grayscale_values = self.grayscale_img.load()

            for y in range(0, self.img_height):
                for x in range(0, self.img_width):
                    R, G, B = rgb_values[x, y]
                    grayscale_values[x, y] = int(0.299 * R) + int(0.587 * G) + int(0.114 * B)

        else:               #The given image is already in grayscale
            self.is_rgb = False
            self.img = self.img.convert('L')

        # Threshold proposed in our algorithm
        self.N = self.img_width * self.img_height
        self.block_size = block_size
        self.b = self.block_size * self.block_size            # b here is the number of pixels in a subblock
        self.Nb = (self.img_width - self.block_size + 1) * (self.img_height - self.block_size + 1)
        self.Nn = 2         # Nn is the number of neighboring blocks to be evaluated
        self.Nf = 188       # Nf is the minimum treshold of the offset's frequency
        self.Nd = 50        # Nd is the minimum treshold of the offset's magnitude


        self.features = Box()       # features is an object of the class that stores all the feature vectors
        self.offsets = {}           # offsets is a dictionary that stores the offsets for two different feature vectors


    def run(self):
        #calling the function "compute_CFeatures" to compute the characteristic features all the sub blocks
        self.compute_CFeatures()           

        #calling the function "sort_features" to sort the feature vectors in lexicographical order
        self.sort_features()                

        # the function "analyze" to compare the adjacent feature vectors with the predefined thresholds
        self.analyze()                      

        #the function "reconstruct" generates an copy-move attacked image and a marked image. It outputs the path of the marked img
        output_img_path = self.reconstruct() 

        return output_img_path


    def compute_CFeatures(self):
        print("Computing the characteristic features....")

        blocks_along_horizontal = self.img_width - self.block_size      # Number of subblocks to be computed in each row
        blocks_along_vertical = self.img_height - self.block_size       # Number of subBlocks to be computed in each column

        if self.is_rgb:
            for x in tqdm.tqdm(range(0, blocks_along_horizontal + 1, 1)):
                for y in range(0, blocks_along_vertical + 1, 1):
                    rgb_block = self.img.crop((x, y, x + self.block_size, y + self.block_size))
                    grayscale_block = self.grayscale_img.crop((x, y, x + self.block_size, y + self.block_size))

                    img_block = subBlock(grayscale_block, rgb_block, x, y, self.block_size)      
                    self.features.append_block(img_block.compute_block_data())      # calculated and storing the feature vector in the object of Box() features.

        else:
            for x in range(blocks_along_horizontal + 1):
                for y in range(blocks_along_vertical + 1):
                    grayscale_block = self.img.crop((x, y, x + self.block_size, y + self.block_size))
                    img_block = subBlock(grayscale_block, None, x, y, self.block_size)
                    # curr_block = Thread(target=img_block.compute_block_data, args=()).start()
                    self.features.append_block(img_block.compute_block_data())      # calculated and storing the feature vector in the object of Box() features.
                        

    def sort_features(self):
        print("Sorting the feature vectors....")
                                    
        self.features.sort_by_features()        #sorting the feature vectors by their features
    

    def analyze(self):
        print("Pairing image blocks....")

        count = 0
        time.sleep(0.1)
        features_size = self.features.get_length()

        for first_block in tqdm.tqdm(range(features_size - 1)):
            second_block = first_block + 1

            rcvd = self.is_valid(first_block, second_block)
            flag = rcvd[0]

            if flag:
                diff = rcvd[1]
                self.add_dict(self.features.container[first_block][0], self.features.container[second_block][0], diff)
                count = count + 1

    
    def is_valid(self, first_block, second_block):
            # This function checks if the two selected blocks satisfies the proposed thresholds from the two papers.
        if abs(first_block - second_block) < self.Nn:
            feature1 = self.features.container[first_block][1]
            feature2 = self.features.container[second_block][1]

            # check the validity of characteristic features according to the second paper
            if abs(feature1[0] - feature2[0]) < self.P[0]:
                if abs(feature1[1] - feature2[1]) < self.P[1]:
                    if abs(feature1[2] - feature2[2]) < self.P[2]:
                        if abs(feature1[3] - feature2[3]) < self.P[3]:
                            if abs(feature1[4] - feature2[4]) < self.P[4]:
                                if abs(feature1[5] - feature2[5]) < self.P[5]:
                                    if abs(feature1[6] - feature2[6]) < self.P[6]:
                                        if abs(feature1[0] - feature2[0]) + abs(feature1[1] - feature2[1]) + abs(feature1[2] - feature2[2]) < self.t1:
                                            if abs(feature1[3] - feature2[3]) + abs(feature1[4] - feature2[4]) + abs(feature1[5] - feature2[5]) + abs(feature1[6] - feature2[6]) < self.t2:

                                                # compute the pair's offset
                                                coordinate1 = self.features.container[first_block][0]
                                                coordinate2 = self.features.container[second_block][0]

                                                # Non Absolute Robust Detection Method
                                                offset = (
                                                    coordinate1[0] - coordinate2[0],
                                                    coordinate1[1] - coordinate2[1]
                                                )

                                                # compute the pair's magnitude
                                                magnitude = np.sqrt(math.pow(offset[0], 2) + math.pow(offset[1], 2))
                                                if magnitude >= self.Nd:
                                                    return 1, offset
        return 0,


    def add_dict(self, coordinate1, coordinate2, diff):
        # this function adds the given coordinates into the dictionary "offsets"
        if diff in self.offsets:
            self.offsets[diff].append(coordinate1)
            self.offsets[diff].append(coordinate2)
        
        else:
            self.offsets[diff] = [coordinate1, coordinate2]


    def check_location(self, img, x, y):
        #This function helps us in detecting the edge of the copy-move attacked region
        if img[x+1, y] == 0 or img[x - 1, y] == 0 or img[x, y + 1] == 0 or img[x, y - 1] == 0:
            return True
        elif img[x - 1, y + 1] == 0 or img[x + 1, y + 1] == 0 or img[x - 1, y - 1] == 0 or img[x + 1, y - 1] == 0:
            return True
        else:
            return False
    

    def reconstruct(self):
        
        #This function generates 2 images which shows us the area of copy-move attack.
        attacks_img = np.zeros((self.img_height, self.img_width))
        marked_img = np.array(self.img.convert('RGB'))

        diff_sorted = sorted(self.offsets, key = lambda key: len(self.offsets[key]), reverse = True)

        pair_found = False

        for key in diff_sorted:
            if self.offsets[key].__len__() < self.Nf * 2:
                break

            if not pair_found:
                print('Found pair(s) of possible copy-move attacks')
                pair_found = True

            print(key, self.offsets[key].__len__())

            for i in range(self.offsets[key].__len__()):
                for j in range(self.offsets[key][i][1], self.offsets[key][i][1] + self.block_size):
                    for k in range(self.offsets[key][i][0], self.offsets[key][i][0] + self.block_size):
                        attacks_img[j][k] = 255

        
        if not pair_found:
            print('No probable copy-move attacks found')

        
        for x in range(2, self.img_height - 2):
            for y in range(2, self.img_width - 2):
                if attacks_img[x, y] == 255 and self.check_location(attacks_img, x, y) == True:

                    # creating the edge line, respectively left-upper, right-upper, left-down, right-down
                    line_color = [255, 0, 0]
                    if attacks_img[x - 1, y] == 0 and attacks_img[x, y - 1] == 0 and attacks_img[x - 1, y - 1] == 0:
                        marked_img[x - 2:x, y] = line_color
                        marked_img[x, y - 2:y] = line_color
                        marked_img[x - 2:x, y - 2:y] = line_color
                    elif attacks_img[x + 1, y] == 0 and attacks_img[x, y - 1] == 0 and attacks_img[x + 1, y - 1] == 0:
                        marked_img[x + 1:x + 3, y] = line_color
                        marked_img[x, y - 2:y] = line_color
                        marked_img[x + 1:x + 3, y - 2:y] = line_color
                    elif attacks_img[x - 1, y] == 0 and attacks_img[x, y + 1] == 0 and attacks_img[x - 1, y + 1] == 0:
                        marked_img[x - 2:x, y] = line_color
                        marked_img[x, y + 1:y + 3] = line_color
                        marked_img[x - 2:x, y + 1:y + 3] = line_color
                    elif attacks_img[x + 1, y] == 0 and attacks_img[x, y + 1] == 0 and attacks_img[x + 1, y + 1] == 0:
                        marked_img[x + 1:x + 3, y] = line_color
                        marked_img[x, y + 1:y + 3] = line_color
                        marked_img[x + 1:x + 3, y + 1:y + 3] = line_color

                    # creating the straigh line, respectively upper, down, left, right line
                    elif attacks_img[x, y + 1] == 0:
                        marked_img[x, y + 1:y + 3] = line_color
                    elif attacks_img[x, y - 1] == 0:
                        marked_img[x, y - 2:y] = line_color
                    elif attacks_img[x - 1, y] == 0:
                        marked_img[x - 2:x, y] = line_color
                    elif attacks_img[x + 1, y] == 0:
                        marked_img[x + 1:x + 3, y] = line_color
                    
        
        print("Reconstructing Image....")
        timestamp = time.strftime("%Y%m%d_%H%M%S")

        attacked_img_file_path = self.img_output_path + timestamp + "_attacked_" + self.img_name  #the path of the attacked image
        marked_img_file_path = self.img_output_path + timestamp + "_marked_" + self.img_name      #the path of the mared image

        #This makes these images in the given path
        imageio.imwrite(attacked_img_file_path, attacks_img)
        imageio.imwrite(marked_img_file_path, marked_img)



        return marked_img_file_path


        






        