from bucket_fill import fill

def test_true_seeds():  
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (4,4)) is None)
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (0,0)) is None)
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (10,0)) is None)
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (10,10)) is None)
    
def test_false_seeds():
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (400,4)) is not None)
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = ("Hello",0)) is not None)
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (4.4,6)) is not None)
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (-1,10)) is not None)
    assert (validate_seed_point(image = load_image("data/smiley.txt"), seed_point = (10,1)) is not None)

test_true_seeds()
test_false_seeds()

print(get_bordering_pixels(load_image("data/snake.txt"), (2,1)))


def test_pattern():
    pass


if __name__ == '__main__':
    # This is just an example. Feel free to change this to whatever suits you.
    test_pattern()
