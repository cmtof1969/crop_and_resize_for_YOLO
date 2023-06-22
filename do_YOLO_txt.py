import os.path

# Calculate the area covering all bounding boxes
# Return values, see below
def CalcAreaCoveringAllBbox( filename ):
  # Count number of bounding boxes
  bbox_count = 0
  # open the file in read mode
  # This file is YOLO labeled .txt file
  file = open(filename, "r")

  x_most_left_top = 1.0
  y_most_left_top = 1.0
  x_most_right_bottom = 0.0
  y_most_right_bottom = 0.0

  # loop through each line in the file
  for line in file:
    # Count number of bounding boxes
    bbox_count += 1
    # split the line by space and store the numbers in a list
    numbers = line.split()
  
    # convert the first number to integer and the rest to float
    # Get the class number
    class_number = int(numbers[0])
    # Get the bounding box (X_center, Y_center, Width, Height)
    b_box = [float(n) for n in numbers[1:]]

    # Calculate left_top corner's (x,y)
    x_left_top = b_box[0] - 0.5 * b_box[2]
    y_left_top = b_box[1] - 0.5 * b_box[3]
    # Calculate right_bottom corner's (x,y)
    x_right_bottom = b_box[0] + 0.5 * b_box[2]
    y_right_bottom = b_box[1] + 0.5 * b_box[3]

    # Calculate most corners
    if x_most_left_top > x_left_top:
      x_most_left_top = x_left_top
    if y_most_left_top > y_left_top:
      y_most_left_top = y_left_top
    if x_most_right_bottom < x_right_bottom:
      x_most_right_bottom = x_right_bottom
    if y_most_right_bottom < y_right_bottom:
      y_most_right_bottom = y_right_bottom

    # do something with the numbers
    print(class_number, b_box)

    # close the file
  file.close()

  # show most corners
  print("most corners=",[x_most_left_top, y_most_left_top, x_most_right_bottom, y_most_right_bottom])
  # Return :
  #     (x, y) at left top corner, (x, y) at right bottom corner, bouding box numbers
  return x_most_left_top, y_most_left_top, x_most_right_bottom, y_most_right_bottom, bbox_count


# Test file existence
#
def testFileEXist( filename ):
  if os.path.isfile( filename ):
    return True
  else:
    return False

# filename = "../images/IMG_2583_80_of_heic.txt"
# if testFileEXist(filename) == True:
#   x1, y1, x2, y2, bbox = CalcAreaCoveringAllBbox( filename )
#   print(x1, y1, x2, y2, bbox)
# else:
#   print("The file does not exist or is not a regular file")

