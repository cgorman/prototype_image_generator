import argparse
import numpy as np
import PIL

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


def create_shape(shape, color, texture=None):
    """
    Creates an instance of a shape with the given properties
    :param shape: The shape to generate. "square", "circle", or "triangle"
    :param color: The color of the shape and its texture. "red", "green", "blue", "black"
    :param texture: The texture to apply to the shape. "solid", "striped" or None
    :return: An image object
    """
    pass


def create_circle(color):
    """
    Makes a circle in the given color
    :param color: "red" "green" "blue" or "black"
    :return: Image object containing a circle
    """
    pass


def create_square(color):
    """
    Creates a square in the given color
    :param color: "red" "green" "blue" or "black"
    :return: Image object containing a square
    """
    pass


def create_triangle(color):
    """
    Creates a triangle in the given color
    :param color: "red" "green" "blue" or "black"
    :return: Image object containing a triangle
    """
    pass


def apply_texture(image, texture):
    """
    Applies the given texture to the image
    :param image: The image object to modify
    :param texture: The texture to apply. "solid" or "striped"
    :return: The modified image
    """
    pass


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
                                                 "in order to test hypotheses about prototype theory.")
    parser.add_argument("--output-directory",
                        help="The directory to save the dataset to.")
    parser.add_argument("--dataset-name",
                        help="Colloquial name for this dataset. Will be the name of the final output directory.")
    parser.add_argument("--random-stats",
                        hellp="Script will generate sensible statistics for shapes at random. All shapes will be used."
                              " If this argument is set, the script will ignore any manual statistics that follow!",
                        action="store_true")

    square_group = parser.add_argument_group("Square Statistics")
    square_group.add_argument("--square-color",
                              help="The color of the prototypical square",
                              choices=color_choices)
    square_group.add_argument("--square-percent-color",
                              help="The percent of squares that are the previous color. The rest will be random",
                              type=float)
    square_group.add_argument_group("--square-texture",
                                    help="The texture of the prototypical square",
                                    choices=texture_choices)
    square_group.add_argument("--square-percent-texture",
                              help="The percent of squares that are the previous texture. The rest will be random",
                              type=float)
    square_group.add_argument("--square-number",
                              help="The number of squares we should generate as output",
                              type=int)

    circle_group = parser.add_argument_group("Circle Statistics")

    pass


if __name__ == "__main__":
    run()
