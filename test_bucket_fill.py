from bucket_fill import fill, validate_seed_point, show_image, load_image, stringify_image, get_bordering_pixels, example_fill

def test_true_seeds():  
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (4,4)) is True)
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (0,0)) is True)
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (10,0)) is True)
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (10,10)) is True)
    
def test_false_seeds():
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (400,4)) is False)
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = ("Hello",0)) is False)
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (4.4,6)) is False)
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (-1,10)) is False)
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (10,1)) is False)

test_true_seeds() # should stay silent
test_false_seeds() # should print error messages

def test_bordering_pixels():

    # Let's check for a single pixel with no neighbours
    expected_result = {"left_pixel": {"position": None, "value": None},
            "up_pixel": {"position": None, "value": None},
            "right_pixel": {"position": None, "value": None},
            "down_pixel": {"position": None, "value": None}}
            
    result = get_bordering_pixels(load_image("data/single_pixel.txt"), (0,0))
    assert(result == expected_result)
    
test_bordering_pixels() # should stay silent

def test_fill_fails():
    assert (load_image("data/smiley.txt") == fill(load_image("data/smiley.txt"), (6,6))) # boundary
    assert (load_image("data/single_pixel.txt") == fill(load_image("data/single_pixel.txt"), (1,1))) # outside the grid
    assert (load_image("data/chessboard.txt") == fill(load_image("data/chessboard.txt"), (4.4,3))) # non-integer seed point

test_fill_fails() # should stay silent

def test_pattern():
    fill(image = load_image("data/bar.txt"), seed_point = (7,3))
    fill(image = load_image("data/smiley.txt"), seed_point = (5,6))
    fill(image = load_image("data/snake.txt"), seed_point = (0,0))
    fill(image = load_image("data/big_square.txt"), seed_point = (0,0))
    fill(image = load_image("data/chessboard.txt"), seed_point = (0,0))
    fill(image = load_image("data/diamond.txt"), seed_point = (2,2))
    fill(image = load_image("data/filled_grid.txt"), seed_point = (0,0)) # should print error message
    fill(image = load_image("data/line.txt"), seed_point = (0,4))
    fill(image = load_image("data/single_pixel.txt"), seed_point = (0,0))
    
if __name__ == '__main__':
    # Let's try filling in some pictures!
    test_pattern()
