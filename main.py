from pathlib import Path
from copy_move_detection import CM_Detection

input_path_str = "Inputs/dataset_example_blur.png"
output_path_str = "Outputs/"
block_size = 32


input_img_path = Path(input_path_str)   
output_path = Path(output_path_str)


if not input_img_path.exists() or not output_path.exists():     #if any of the input image or the output path doesn't exists
    print("Path does'nt exist!!!")
    exit(1)

img_name = input_img_path.name


image_inst = CM_Detection(input_img_path, img_name, output_path, block_size)    #creating an instance of the class CM_Detection named image_inst
output_img_path = image_inst.run()      # the method run() is called from the instance and the output image path is stored

print("Output Image Generated at: ", output_img_path)


