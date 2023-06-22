import cv2
import do_YOLO_txt as yotxt # chiaming self-made
import os
import os.path
import random
from pathlib import Path


def CropAndResize( img_fn, txt_fn ):
    # Calculate All Bounding Box Area (ABBA) in normalized numbers
    x1, y1, x2, y2, bbx_cnt = yotxt.CalcAreaCoveringAllBbox(txt_fn)
    # Calculate ABBA's width and height in normalized numbers
    abba_width = x2 - x1
    abba_height = y2 - y1
    # Set ABBA expansion factor, ABBA add WEXP% of width, HEXP% of height
    #
    #                 0.5 * WEXP%
    #                    |   |
    #          @-------------@---
    #          |      w  |   |  0.5 * HEXP% 
    #          |   +-----+ --|---
    #          |   |ABBA | h |
    #          |   |     |   |
    #          |   +-----+   |
    #          |             |
    #          @-------------@
    WEXP = 30
    HEXP = 30
    # Calculate expanded,
    #      (x1, y1) at left top corner, (x2, y2) at right bottom corner, bouding box numbers
    #       x1, y1, x2, y2 are in normalized numbers
    x1_exp = x1 - 0.5 * (abba_width * WEXP) / 100
    y1_exp = y1 - 0.5 * (abba_height * HEXP) / 100
    x2_exp = x2 + 0.5 * (abba_width * WEXP) / 100
    y2_exp = y2 + 0.5 * (abba_height * HEXP) / 100
    if x1_exp < 0:
        x1_exp = 0
    if y1_exp < 0:
        y1_exp = 0
    if x2_exp > 1:
        x2_exp = 1
    if y2_exp > 1:
        y2_exp = 1
    print(x1_exp, y1_exp, x2_exp, y2_exp, abba_width, abba_height)


    img = cv2.imread(img_fn)
    img_width = img.shape[1]
    img_height = img.shape[0]
    print(img_width, img_height)

    # Calculate expanded ABBA in absolute numbers
    x1_exp_abs = int(x1_exp * img_width)
    y1_exp_abs = int(y1_exp * img_height)
    x2_exp_abs = int(x2_exp * img_width)
    y2_exp_abs = int(y2_exp * img_height)

    # Crop the img
    img_crop = img[y1_exp_abs:y2_exp_abs, x1_exp_abs:x2_exp_abs]

    # Calculate cropped width, height
    crop_width = x2_exp_abs - x1_exp_abs + 1
    crop_height = y2_exp_abs - y1_exp_abs + 1

    # Set resize image size
    IMGSZ = 640 
    if crop_width > crop_height:
        resz_width = IMGSZ
        resz_height = int((crop_height * IMGSZ) / crop_width)
    else:
        resz_height = IMGSZ
        resz_width = int((crop_width*IMGSZ) / crop_height)

    # Resize the cropped img
    img_c_and_r = cv2.resize(img_crop,(resz_width, resz_height))

    # cv2.imshow(img_fn, img)
    # cv2.imshow("Croped", img_crop)
    # cv2.imshow("crop and resize", img_c_and_r)
    # cv2.imwrite("cropped.jpg", img_crop)
    # cv2.imwrite("crop and resize.jpg", img_c_and_r)
    # cv2.waitKey(1000)

    # cv2.destroyAllWindows()

    return img_c_and_r

#######################
#     Main routine    #
#######################
# Give the source directory
src_dir_name = '../images'

# Search for all  '*.txt'
files = Path(src_dir_name).glob('*.txt')

# Set data item names
purposes = ['train', 'val', 'test']
# Set component items
components = ['images', 'labels']

# Set data item constants
TRAIN = 0
VAL = 1
TEST = 2
TRAIN_POPULATION = 0.8
VAL_POPULATION = 0.1
TEST_POPULATION = 0.1

# Deinfe probabilities & values
probabilities = [TRAIN_POPULATION, VAL_POPULATION, TEST_POPULATION]
purpose_values = [TRAIN, VAL, TEST]

# Set some flag
dir_made = False
count = 0
# for all img & txt files we got
for f in files:
    # get file name 
    txt_fn = f.name
    # Delete extention 'txt'
    temp = txt_fn.strip("txt")
    # Make labelImg annotated jpg file name '*.jpg'
    img_fn = temp+"jpg"
    # Make txt file path & img file path
    txt_path = src_dir_name + '/' + txt_fn
    img_path = src_dir_name + '/' + img_fn
    
    # Test img path's file existence
    if yotxt.testFileEXist(img_path) == False:
        # Except the "classes.txt" file
        continue
    
    print(txt_path, img_path)

    # Call crop & resize, and get result image
    result_img = CropAndResize( img_path, txt_path )
    # Use '$ mv ./mnnk_images/Mnnk*.jpg ./mnnk_images/train/Mnnk*.jpg' to move the annotated jpg files 
    # os.rename(source_path, destination_path)

    # Make a new images directory to save,
    #  original txt files and croped&resized img files
    if dir_made == False:
        # Set the flag
        dir_made = True
        
        # For each of 'images' and 'labels'
        # img_dest_dir = './images'
        # txt_dest_dir = './labels'
        for component in components:
            # Make dir './images' and './labels'
            try:
                os.mkdir('./' + component)
            except FileExistsError as fxe:
                print("FileExistsError, "+'./'+component)
                print("Program aborted!")
                exit(0)
            # os.system('mkdir ./' + component)
            
            # Change dir to './images' and './lables'
            os.chdir('./' + component)
            # os.system('cd ./' + component)
            
            # For each of 'train', 'val', 'test'
            for purpose in purposes:
                # Make dir 'train', 'val', 'test'
                try:
                    os.mkdir('./' + purpose)
                except FileExistsError as fxe:
                    print("FileExistsError, "+'./'+purpose)
                    print("Program aborted!")
                    exit(0)
                # os.system('mkdir ./' + purpose)
                
            # Return to upper dir of './images' and './labels'
            print('cd ../')
            os.chdir('../')
            # os.system('cd ../')

    # Generate a random number between 0 and 1
    random_value = random.random()
    # Initialize a cumulative probability
    cumulative_prob = 0
    # Loop through the values and probabilities
    for purpose_value, prob in zip(purpose_values, probabilities):
        # Add the probability to the cumulative probability
        cumulative_prob += prob
        # If the random number is less than or equal to the cumulative probability
        if random_value <= cumulative_prob:
            # The purpose_value is determined
            # Break out of the loop
            break

    # os.system('echo 1 > ./' + components[0] + '/' + purposes[purpose_value] + '/bb' + str(count) + '.txt')
    # os.system('echo 1 > ./' + components[1] + '/' + purposes[purpose_value] + '/kk' + str(count) + '.txt')
    count += 1

    # Copy .txt file to './labels/{purposes[purpose_value]}/'
    cli_str = 'cp ' + txt_path + ' ' + './' + components[1] + '/' + purposes[purpose_value] + '/' + txt_fn
    result = os.system(cli_str)
    if result != 0:
        print("os.system() failed, ", cli_str)
        exit(0)

    # Write cropped image to './images/{purposes[purpose_value]}/'
    dest_img_path = './'+components[0]+'/'+purposes[purpose_value]+'/'+img_fn
    cv2.imwrite(dest_img_path, result_img)

    # img_dest_path = img_dest_dir + '/' + img_fn
    # print(img_dest_path)
    # cv2.imwrite( img_dest_path, result_img )
    