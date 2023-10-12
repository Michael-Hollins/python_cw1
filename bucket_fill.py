""" Coursework 1: Bucket Fill
"""

def load_image(filename):
    """ Load image from file made of 0 (unfilled pixels) and 1 (boundary pixels) and 2 (filled pixel)

    Example of content of filename:

0 0 0 0 1 1 0 0 0 0
0 0 1 1 0 0 1 1 0 0
0 1 1 0 0 1 0 1 1 0
1 1 0 0 1 0 1 0 1 1
1 0 0 1 0 0 1 0 0 1
1 0 0 1 0 0 1 0 0 1
1 1 0 1 0 0 1 0 1 1
0 1 1 0 1 1 0 1 1 0
0 0 1 1 0 0 1 1 0 0
0 0 0 0 1 1 0 0 0 0

    Args:
        filename (str) : path to file containing the image representation

    Returns:
        list : a 2D representation of the filled image, where
               0 represents an unfilled pixel,
               1 represents a boundary pixel
               2 represents a filled pixel
    """

    image = []
    with open(filename) as imagefile:
        for line in imagefile:
            if line.strip():
                row = list(map(int, line.strip().split()))
                image.append(row)
    return image


def stringify_image(image):
    """ Convert image representation into a human-friendly string representation

    Args:
        image (list) : list of lists of 0 (unfilled pixel), 1 (boundary pixel) and 2 (filled pixel)

    Returns:
        str : a human-friendly string representation of the image
    """
    
    if image is None:
        return ""

    # The variable "mapping" defines how to display each type of pixel.
    mapping = {
        0: " ",
        1: "*",
        2: "0"
    }

    image_str = ""
    if image:
        image_str += "+ " + "- " * len(image[0]) + "+\n"
    for row in image:
        image_str += "| "
        for pixel in row:
            image_str += mapping.get(pixel, "?") + " "
        image_str += "|"
        image_str += "\n"
    if image:
        image_str += "+ " + "- " * len(image[0]) + "+\n" 
        
    return image_str


def show_image(image):
    """ Show image in terminal

    Args:
        image (list) : list of lists of 0 (unfilled pixel), 1 (boundary pixel) and 2 (filled pixel)
    """
    print(stringify_image(image))


def validate_seed_point(image, seed_point):
    """ Check that the starting seed given is valid. If so, return True, else False.
    
    Invalid starting seeds would be out of the grid range, non-integer values and
    starting on a boundary value. This function is a series of logical tests. If 
    all pass, the function returns True, otherwise it's False.
    
    Args:
        image (list) : a 2D nested list representation of an image, where
                       0 represents an unfilled pixel, and
                       1 represents a boundary pixel
        seed_point (tuple) : a 2-element tuple representing the (row, col) 
                       coordinates of the seed point to start filling
                       
    Returns:
        (bool) : true if all tests pass, else false

    """
    
    # Grid range
    n_rows = len(image)
    n_cols = len(image[0])
    
    # Seed values
    seed_row = seed_point[0]
    seed_col = seed_point[1]
    
    # First, check integer values
    seed_row_is_integer = isinstance(seed_row, int)
    seed_col_is_integer = isinstance(seed_col, int)
    if not (seed_row_is_integer and seed_col_is_integer):
        print("Starting point is not a tuple of integers.")
        return False
    
    # Second, check we're in the grid
    seed_row_in_grid = seed_row in list(range(0, n_rows))
    seed_col_in_grid = seed_col in list(range(0, n_cols))
    if not (seed_row_in_grid and seed_col_in_grid):
        print("Starting point is outside the grid range.")
        return False       
    
    # Third, check we're on an unfilled pixel
    if not image[seed_row][seed_col] == 0:
        print("Starting point is on a boundary.")
        return False
        
    return True
 
def get_bordering_pixels(image, coords):
   """ We zoom in on a pixel and get the characteristics of its neigbbours.
   
   If the pixel's neighbours (up, down, left, right) would be outside the bounds
   of the image, return None for its position and value.
   
   Args:
        image (list) : a 2D nested list representation of an image, where
                       0 represents an unfilled pixel, and
                       1 represents a boundary pixel
        coords (tuple) : a 2-element tuple representing the (row, col) 
                       coordinates of the seed point to start filling
                       
    Returns:
        (dict) : Nested dictionary, keyed by left, up, down, or right.
                 Pixel properties are its position and its value. If it's
                 out of bounds it returns None for both of these.
   
   """
   
   n_rows = len(image)
   n_cols = len(image[0])
    
   row = coords[0]
   col = coords[1]
   
   if col-1 not in list(range(n_cols)):
       left_pixel = None
       left_pixel_val = None
   else:
       left_pixel = (row, col-1)
       left_pixel_val = image[row][col-1]
        
   if col+1 not in list(range(n_cols)):
       right_pixel = None
       right_pixel_val = None
   else:
       right_pixel = (row, col+1)
       right_pixel_val = image[row][col+1]
        
   if row-1 not in list(range(n_rows)):
       up_pixel = None
       up_pixel_val = None
   else:
       up_pixel = (row-1, col)
       up_pixel_val = image[row-1][col]
        
   if row+1 not in list(range(n_rows)):
       down_pixel = None
       down_pixel_val = None
   else:
       down_pixel = (row+1, col)
       down_pixel_val = image[row+1][col]
          
   return {"left_pixel": {"position": left_pixel, "value": left_pixel_val},
            "up_pixel": {"position": up_pixel, "value": up_pixel_val},
            "right_pixel": {"position": right_pixel, "value": right_pixel_val},
            "down_pixel": {"position": down_pixel, "value": down_pixel_val}} 


def fill_surrounding_pixels(image, coords):
    """ Recursive function to replace 0 with 2 by checking neighbours.
    
    We begin by getting the value of the pixel where we start. 
    If it's zero, we replace it with a two i.e. we fill in the pixel.    
    We then check the neighbouring pixels. If one has a zero value, move 
    to that pixel and start the process again by recursion. 
    We return the image when all surrounding pixels are filled or out of bounds.
    
    Args:
        image (list) : a 2D nested list representation of an image, where
                       0 represents an unfilled pixel, and
                       1 represents a boundary pixel
        coords (tuple) : a 2-element tuple representing the (row, col) 
                       coordinates of the seed point to start filling
                       
    Returns:
        (list) : The image filled out from the starting seed point.
    
    """
    
    # If the pixel value is unfilled, fill it.
    row = coords[0]
    col = coords[1]
    if image[row][col] == 0:
        image[row][col] = 2
    
    # Check the values and coordinates of adjacent pixels.
    adjacent_pixels = get_bordering_pixels(image, coords)
    
    # If any neighbouring pixels are unfilled, move to them and restart the process.
    for pixel in ["left_pixel", "up_pixel", "right_pixel", "down_pixel"]:     
        if adjacent_pixels[pixel]["value"] == 0:
            row = adjacent_pixels[pixel]["position"][0]
            col = adjacent_pixels[pixel]["position"][1]            
            fill_surrounding_pixels(coords = (row, col), image = image)
    
    # Otherwise, return the filled image
    return image      

    
def fill(image, seed_point):
    """ Fill the image from seed point to boundary

    the image should remain unchanged if:
    - the seed_point has a non-integer coordinate
    - the seed_point is on a boundary pixel
    - the seed_point is outside of the image

    Args:
        image (list) : a 2D nested list representation of an image, where
                       0 represents an unfilled pixel, and
                       1 represents a boundary pixel
        seed_point (tuple) : a 2-element tuple representing the (row, col) 
                       coordinates of the seed point to start filling

    Returns:
        list : a 2D representation of the filled image, where
               0 represents an unfilled pixel,
               1 represents a boundary pixel, and
               2 represents a filled pixel
    """

    # First, check we have a valid starting point. If not, return the image.
    if validate_seed_point(image, seed_point) is False:
        return image
    
    # If so, fill the empty pixels and return the new image
    image = fill_surrounding_pixels(image, seed_point)
    show_image(image)
    
def example_fill(image_example, seed_example):
    image = load_image(image_example)

    print("Before filling:")
    show_image(image)

    image = fill(image=image, seed_point=seed_example)

    print("-" * 25)
    print("After filling:")
    show_image(image)


if __name__ == '__main__':
    example_fill(image_example = "data/smiley.txt", seed_example = (5,6))
