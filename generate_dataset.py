import argparse
import numpy as np
import PIL.Image as Image
from PIL import ImageDraw
import random
import os

"""
Script to generate simple images for a synthetic dataset for testing categorization techniques with deep CNNs
User will provide parameters to generate the image files such that they represent prototypical token objects and
unusual token objects. The user can manually enter these parameters or the script can choose them somewhat randomly.
The final output will be a set of N images of shapes which have statistical similarities with each other. For example
75% of circles are green, 10% are red, and 15% are blue, and maybe 70% of circles are solid, 20% are striped, and
5% are blank or something. Important to note that the color and texture are conditionally independent.

The output will be placed into a directory with a text file listing the statistical properties of the prototypes. Since
the properties of the non-prototypes may vary from set to set we will have to just ask for a name for the set from the
user to make things a bit easier.
"""


def percentage_float(x):
    """
    Converts a string to a float and requires it to be between 0 and 1 inclusive
    :param x: Something that can be cast to float
    :return: The converted float
    """
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]" % x)
    return x


def random_stats(args):
    """
    Creates reasonable random statistics to generate prototypes. Saves them in the arguments object
    :param args: The namespace object returned by parse_args()
    :returns: The modified namespace object with values inserted for all of the shape statistics
    """
    return args


def create_shape_set(shape, count, prototype_color, percent_color, prototype_texture, percent_texture,
                     directory, color_choices, texture_choices, image_size):
    """
    Creates and saves a set of shapes
    :param shape: The shape to generate
    :param count: The number of images to generate
    :param prototype_color: The color of the prototypical shape
    :param percent_color: The percent of shapes that are that color
    :param prototype_texture: Ditto
    :param percent_texture: Ditto
    :param directory: The directory to save the images to
    :param color_choices: List of possible colors
    :param texture_choices: List of possible textures
    :param image_size: The width and height of each output image
    """
    for x in xrange(0, count):
        # Determine color of this particular square
        if np.random.uniform() < percent_color:
            color = prototype_color
        else:
            color = random.choice(color_choices)

        # Ditto for texture
        if np.random.uniform() < percent_texture:
            texture = prototype_texture
        else:
            texture = random.choice(texture_choices)

        # Create the square image object
        if shape == "square":
            image = create_square(color, texture, image_size)
        elif shape == "circle":
            image = create_circle(color, texture, image_size)
        elif shape == "triangle":
            image = create_triangle(color, texture, image_size)
        else:
            raise IOError("Shape {} incorrect".format(shape))
        assert image == type(Image)

        # Save the square image to the correct directory
        fname = "{}/{}_{}".format(directory, shape, x)
        with open(fname, "w") as fp:
            image.save(fp)


def create_circle(color, texture, image_size):
    """
    Makes a circle in the given color
    :param color: "red" "green" "blue" or "black"
    :return: Image object containing a circle
    """
    im = Image.new("RGB", (image_size, image_size), "white")
    circle = ImageDraw.Draw(im)
    top_left = (5, 5)
    bottom_right = (image_size - 5, image_size - 5)
    if texture == "solid":
        circle.ellipse([top_left, bottom_right], color, color)
    else:
        circle.ellipse([top_left, bottom_right], color, color)
    del circle
    im.show()
    return None


def create_square(color, texture, image_size):
    """
    Creates a square in the given color
    :param color: "red" "green" "blue" or "black"
    :return: Image object containing a square
    """
    return None


def create_triangle(color, texture, image_size):
    """
    Creates a triangle in the given color
    :param color: "red" "green" "blue" or "black"
    :return: Image object containing a triangle
    """
    return None


def run():
    """
    Parses the arguments and generates the image data. Saves files as it goes to conserve RAM
    If stats are not specified they will be generate
    """

    # Parse the command line arguments
    color_choices = {"red", "green", "blue", "black"}
    texture_choices = {"striped", "solid", "blank"}
    parser = argparse.ArgumentParser(prog="generate_dataset.py",
                                     description="Script to generate prototype images for research on category "
                                                 "development. Generates images which conform to certain statistics "
                                                 "in order to test hypotheses about prototype theory. "
                                                 "NOTE: Pass an arguments file prefixed with @ as an arg "
                                                 "to include the arguments listed in that file. Each argument and value"
                                                 " should be on separate lines.",
                                     epilog="(Again, you may want to use a file instead)",
                                     fromfile_prefix_chars="@")
    parser.add_argument("--output-directory",
                        help="The directory to save the dataset to.")
    parser.add_argument("--dataset-name",
                        help="Colloquial name for this dataset. Will be the name of the final output directory.")
    parser.add_argument("--random-stats",
                        help="Script will generate sensible statistics for shapes at random. All shapes will be used."
                             " If this argument is set, the script will ignore any manual statistics that follow!",
                        action="store_true")
    parser.add_argument("--image-size",
                        help="Size (in pixels) of each image. Images are square so just enter one number",
                        type=int)

    square_group = parser.add_argument_group("Square Statistics")
    square_group.add_argument("--square-color",
                              help="The color of the prototypical square",
                              choices=color_choices)
    square_group.add_argument("--square-percent-color",
                              help="The percent of squares that are the previous color. The rest will be random. "
                                   "Value must be in range [0.0, 1.0]",
                              type=percentage_float)
    square_group.add_argument("--square-texture",
                              help="The texture of the prototypical square",
                              choices=texture_choices)
    square_group.add_argument("--square-percent-texture",
                              help="The percent of squares that are the previous texture. The rest will be random. "
                                   "Value must be in range [0.0, 1.0]",
                              type=percentage_float)
    square_group.add_argument("--square-number",
                              help="The number of squares we should generate as output",
                              type=int)

    circle_group = parser.add_argument_group("Circle Statistics")
    circle_group.add_argument("--circle-color",
                              help="The color of the prototypical circle",
                              choices=color_choices)
    circle_group.add_argument("--circle-percent-color",
                              help="The percent of circles that are the previous color. The rest will be random. "
                                   "Value must be in range [0.0, 1.0]",
                              type=percentage_float)
    circle_group.add_argument("--circle-texture",
                              help="The texture of the prototypical circle",
                              choices=texture_choices)
    circle_group.add_argument("--circle-percent-texture",
                              help="The percent of circles that are the previous texture. The rest will be random. "
                                   "Value must be in range [0.0, 1.0]",
                              type=percentage_float)
    circle_group.add_argument("--circle-number",
                              help="The number of circles we should generate as output",
                              type=int)

    triangle_group = parser.add_argument_group("Triangle Statistics")
    triangle_group.add_argument("--triangle-color",
                                help="The color of the prototypical triangle",
                                choices=color_choices)
    triangle_group.add_argument("--triangle-percent-color",
                                help="The percent of triangles that are the previous color. The rest will be random. "
                                     "Value must be in range [0.0, 1.0]",
                                type=percentage_float)
    triangle_group.add_argument("--triangle-texture",
                                help="The texture of the prototypical triangle",
                                choices=texture_choices)
    triangle_group.add_argument("--triangle-percent-texture",
                                help="The percent of triangles that are the previous texture. The rest will be random. "
                                     "Value must be in range [0.0, 1.0]",
                                type=percentage_float)
    triangle_group.add_argument("--triangle-number",
                                help="The number of triangles we should generate as output",
                                type=int)

    args = parser.parse_args()

    # Generate stats if user did not specify them
    if args.random_stats:
        args = random_stats(args)

    # Convert the sets to lists to make things easier later
    color_choices = list(color_choices)
    texture_choices = list(texture_choices)

    # Set up the directory structure
    directory = args.output_directory + "/" + args.dataset_name
    try:
        os.makedirs(directory)
    except OSError:
        print "Unable to create directory"
        exit(1)

    # Make some squares
    #create_shape_set("square", args.square_number, args.square_color, args.square_percent_color, args.square_texture,
    #                 args.square_percent_texture, directory, color_choices, texture_choices, args.image_size)

    # Make some circles
    create_shape_set("circle", args.circle_number, args.circle_color, args.circle_percent_color, args.circle_texture,
                     args.circle_percent_texture, directory, color_choices, texture_choices, args.image_size)

    # Make some triangles
    create_shape_set("triangle", args.triangle_number, args.triangle_color, args.triangle_percent_color,
                     args.triangle_texture, args.triangle_percent_texture,
                     directory, color_choices, texture_choices, args.image_size)


if __name__ == "__main__":
    run()
