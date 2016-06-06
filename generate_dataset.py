import argparse
import numpy as np
import PIL.Image as Image
from PIL import ImageDraw
import random
import os


# A kind of global variable so we only need to generate as many stripe textures as there are colors
STRIPES = dict()


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


def create_shape_set(shape, filetype, count, prototype_color, percent_color, prototype_texture, percent_texture,
                     color_choices, texture_choices, image_size, validation_set, traindir, valdir):
    """
    Creates and saves a set of shapes
    :param shape: The shape to generate
    :param filetype: Either png or jpg
    :param count: The number of images to generate
    :param prototype_color: The color of the prototypical shape
    :param percent_color: The percent of shapes that are that color
    :param prototype_texture: Ditto
    :param percent_texture: Ditto
    :param color_choices: List of possible colors
    :param texture_choices: List of possible textures
    :param image_size: The width and height of each output image
    :param validation_set: The percentage of images to save into the validation folder
    :param traindir: The directory to save training data to
    :param valdir: The directory to save validation data to
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

        # Create the image to draw on
        image = Image.new("RGB", (image_size, image_size), "white")

        # Create the square image object
        if shape == "square":
            image = draw_square(image, color, texture)
        elif shape == "circle":
            image = draw_circle(image, color, texture)
        elif shape == "triangle":
            image = draw_triangle(image, color, texture)
        else:
            raise IOError("Shape {} incorrect".format(shape))

        # Save the image, dir/training/shape_number_color_texture.png, zero pad the outputs
        fname = "{0}/{1}_{2:0{3}d}_{4}_{5}.{6}".format(traindir,
                                                       shape, x, len(str(count - 1)),
                                                       color, texture, filetype)
        with open(fname, "w") as fp:
            image.save(fp)

    if validation_set > 0:
        # Take the newly saved files and put some of them into the validation directory
        validation_num = int(count * validation_set)
        split_validation_set(traindir, valdir, validation_num)


def split_validation_set(traindir, valdir, validation_num):
    """
    Move some number of files from the training directory into a newly created validation directory
    :param traindir: The directory the training data was saved to. Images will be moved from here to..
    :param valdir: ..here.
    :param validation_num: The number of files to move
    """
    # Get a list of all the files we just created with their full paths
    training_file_list = [os.path.join(traindir, f) for f in os.listdir(traindir) if f.endswith(".png")]
    # Get the random indices to pull from the training file list
    validation_idxs = random.sample(range(len(training_file_list)), validation_num)
    for index in validation_idxs:
        src = training_file_list[index]
        filename = os.path.basename(src)
        dest = os.path.join(valdir, filename)
        os.rename(src, dest)


def draw_circle(image, color, texture):
    """
    Makes a circle in the given color with the given texture applied to it
    :param image: The image object to draw on
    :param color: "red" "green" "blue" or "black"
    :param texture: "solid" "striped" or "blank"
    :return: Image object containing a circle
    """
    # Images are all square so just take the width and use it
    image_size = image.size[0]
    # Create the image to draw on
    output_image = Image.new("RGB", (image_size, image_size), "white")
    circle = ImageDraw.Draw(image)

    # Draw a circle the size of the image and apply the correct texture
    if texture == "solid":
        circle.ellipse([(5, 5), (image_size - 5, image_size - 5)], color, color)
    else:
        circle.ellipse([(5, 5), (image_size - 5, image_size - 5)], "white", color)

    if texture == "striped":
        # Rotate the stripe image a random amount and crop it down to the correct size
        stripes_size = image_size * 2
        angle = random.randint(0, 180)
        tmpimg = STRIPES[color].rotate(angle)
        # Make sure we are centered on the image so we don't get any of the rotation artifacts
        tmpimg = tmpimg.crop((stripes_size/4, stripes_size/4,
                              stripes_size - stripes_size/4, stripes_size - stripes_size/4))
        # Use the circle as a mask over the stripes
        mask = Image.new("1", (image_size, image_size), 0)  # Start with a black image
        mask_circle = ImageDraw.Draw(mask)
        mask_circle.ellipse([(7, 7), (image_size - 7, image_size - 7)], 1, 1)
        del mask_circle
        image = Image.composite(tmpimg, image, mask)

    # Delete the drawing object because that's what the docs say to do and who cares
    del circle
    # Randomly scale and move the circle to a new image
    scale_factor = random.uniform(1, 4)
    scale_params = (
        scale_factor, 0, 0,
        0, scale_factor, 0
    )
    image = image.transform((image_size, image_size), Image.AFFINE, scale_params)

    # Get the bounding box of the newly transformed circle
    box = image.getbbox()
    new_diameter = box[2] - box[0]
    # Use the bounding box to determine where the circle is allowed to be translated to
    translate_x = random.randint(new_diameter - image_size, 0)
    translate_y = random.randint(new_diameter - image_size, 0)
    translate_params = (
        1, 0, translate_x,
        0, 1, translate_y
    )
    image = image.transform((image_size, image_size), Image.AFFINE, translate_params)

    # Give the image a white background

    # Get the new bounding box of the newly transformed circle
    box = image.getbbox()
    # Create a new mask using the bounding box
    mask = Image.new("1", (image_size, image_size), 0)
    mask_box = ImageDraw.Draw(mask)
    mask_box.rectangle(box, 1, 0)
    del mask_box
    # Apply the mask to the circle
    output_image = Image.composite(image, output_image, mask)

    return output_image


def draw_square(image, color, texture):
    """
    Creates a square in the given color with the given texture applied to it
    :param image: The image object to draw on
    :param color: "red" "green" "blue" or "black"
    :param texture: "solid" "striped" or "blank"
    :return: Image object containing a square
    """
    # Images are all square so just take the width and use it
    image_size = image.size[0]
    # Create the image to draw on
    output_image = Image.new("RGB", (image_size, image_size), "white")
    square = ImageDraw.Draw(image)

    # Draw a square roughly the size of the image and apply the correct texture
    if texture == "solid":
        square.rectangle([(5, 5), (image_size - 5, image_size - 5)], color, color)
    else:
        for i in xrange(0, 5):
            # Draw multiple rectangles to get the correct line thickness. Ugh.
            square.rectangle([(10 + i, 10 + i), (image_size - 10 - i, image_size - 10 - i)], "white", color)

    if texture == "striped":
        # Rotate the stripe image a random amount and crop it down to the correct size
        stripes_size = image_size * 2
        angle = random.randint(0, 180)
        tmpimg = STRIPES[color].rotate(angle)
        # Make sure we are centered on the image so we don't get any of the rotation artifacts
        tmpimg = tmpimg.crop((stripes_size / 4, stripes_size / 4,
                              stripes_size - stripes_size / 4, stripes_size - stripes_size / 4))
        # Use the circle as a mask over the stripes
        mask = Image.new("1", (image_size, image_size), 0)  # Start with a black image
        mask_square = ImageDraw.Draw(mask)
        mask_square.rectangle([(15, 15), (image_size - 15, image_size - 15)], 1, 1)
        del mask_square
        image = Image.composite(tmpimg, image, mask)

    # Delete the drawing object because that's what the docs say to do and who cares
    del square
    # Randomly scale and move the square to a new image
    scale_factor = random.uniform(1, 4)
    scale_params = (
        scale_factor, 0, 0,
        0, scale_factor, 0
    )
    image = image.transform((image_size, image_size), Image.AFFINE, scale_params)

    # Get the bounding box of the newly transformed square
    box = image.getbbox()
    new_width = box[2] - box[0]
    # Use the bounding box to determine where the circle is allowed to be translated to
    translate_x = random.randint(new_width - image_size, 0)
    translate_y = random.randint(new_width - image_size, 0)
    translate_params = (
        1, 0, translate_x,
        0, 1, translate_y
    )
    image = image.transform((image_size, image_size), Image.AFFINE, translate_params)

    # Give the image a white background

    # Get the new bounding box of the newly transformed square
    box = image.getbbox()
    box = (box[0] + 1, box[1] + 1, box[2] - 1, box[3] - 1)
    # Create a new mask using the bounding box
    mask = Image.new("1", (image_size, image_size), 0)
    mask_box = ImageDraw.Draw(mask)
    mask_box.rectangle(box, 1, 0)
    del mask_box
    # Apply the mask to the square
    output_image = Image.composite(image, output_image, mask)
    return output_image


def draw_triangle(image, color, texture):
    """
    Creates a triangle in the given color with the given texture applied to it
    :param image: The image object to draw on
    :param color: "red" "green" "blue" or "black"
    :param texture: "solid" "striped" or "blank"
    :return: Image object containing a triangle
    """
    # Images are all square so just take the width and use it
    image_size = image.size[0]
    # Create the image to draw on
    output_image = Image.new("RGB", (image_size, image_size), "white")
    triangle = ImageDraw.Draw(image)
    top = (image_size / 2, 10)
    bottom_left = (10, image_size - 10)
    bottom_right = (image_size - 10, image_size - 10)

    # Draw a square roughly the size of the image and apply the correct texture
    triangle.polygon([top, bottom_left, bottom_right], color, color)
    if texture != "solid":
        # Nest a smaller triangle to simulate a bolder edge
        triangle.polygon([(top[0], top[1] + 10),
                          (bottom_left[0] + 5, bottom_left[1] - 5),
                          (bottom_right[0] - 5, bottom_right[1] - 5)],
                         "white", color)

    if texture == "striped":
        # Rotate the stripe image a random amount and crop it down to the correct size
        stripes_size = image_size * 2
        angle = random.randint(0, 180)
        tmpimg = STRIPES[color].rotate(angle)
        # Make sure we are centered on the image so we don't get any of the rotation artifacts
        tmpimg = tmpimg.crop((stripes_size / 4, stripes_size / 4,
                              stripes_size - stripes_size / 4, stripes_size - stripes_size / 4))
        # Use the circle as a mask over the stripes
        mask = Image.new("1", (image_size, image_size), 0)  # Start with a black image
        mask_triangle = ImageDraw.Draw(mask)
        mask_triangle.polygon([(top[0], top[1] + 10),
                               (bottom_left[0] + 5, bottom_left[1] - 5),
                               (bottom_right[0] - 5, bottom_right[1] - 5)],
                              1, 1)
        del mask_triangle
        image = Image.composite(tmpimg, image, mask)

    # Delete the drawing object because that's what the docs say to do and who cares
    del triangle
    # Randomly scale and move the square to a new image
    scale_factor = random.uniform(1, 4)
    scale_params = (
        scale_factor, 0, 0,
        0, scale_factor, 0
    )
    image = image.transform((image_size, image_size), Image.AFFINE, scale_params)

    # Get the bounding box of the newly transformed square
    box = image.getbbox()
    new_width = box[2] - box[0]
    # Use the bounding box to determine where the circle is allowed to be translated to
    translate_x = random.randint(new_width - image_size, 0)
    translate_y = random.randint(new_width - image_size, 0)
    translate_params = (
        1, 0, translate_x,
        0, 1, translate_y
    )
    image = image.transform((image_size, image_size), Image.AFFINE, translate_params)

    # Give the image a white background

    # Get the new bounding box of the newly transformed square
    box = image.getbbox()
    box = (box[0] + 1, box[1] + 1, box[2] - 1, box[3] - 1)
    # Create a new mask using the bounding box
    mask = Image.new("1", (image_size, image_size), 0)
    mask_box = ImageDraw.Draw(mask)
    mask_box.rectangle(box, 1, 0)
    del mask_box
    # Apply the mask to the square
    output_image = Image.composite(image, output_image, mask)
    return output_image


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
    parser.add_argument("--filetype",
                        help="What to save the output images as",
                        default="png",
                        choices=["jpg", "png"])
    parser.add_argument("--random-stats",
                        help="Script will generate sensible statistics for shapes at random. All shapes will be used."
                             " If this argument is set, the script will ignore any manual statistics that follow!",
                        action="store_true")
    parser.add_argument("--image-size",
                        help="Size (in pixels) of each image. Images are square so just enter one number",
                        type=int)
    parser.add_argument("--validation-split",
                        help="If set, this percentage of images will be put into the validation directory. "
                             "Value must be in range [0.0, 1.0]",
                        type=percentage_float,
                        default=0.0)

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
    directory = os.path.join(args.output_directory, args.dataset_name)
    traindir = os.path.join(directory, "training")
    valdir = None
    if args.validation_split > 0:
        valdir = os.path.join(directory, "validation")
    try:
        os.makedirs(directory)
        os.makedirs(traindir)
        os.makedirs(valdir)
    except OSError:
        print("Unable to create directories")
        exit(1)

    # Create the stripe images twice the size so we can rotate them without issue
    for color in color_choices:
        STRIPES[color] = Image.new("RGB", (args.image_size * 2, args.image_size * 2), "white")
        stripes = ImageDraw.Draw(STRIPES[color])
        for y in xrange(0, args.image_size * 2, 20):
            stripes.line([(0, y), (args.image_size * 2, y)], fill=color, width=3)
        del stripes

    # Make some squares
    create_shape_set("square", args.filetype, args.square_number, args.square_color,
                     args.square_percent_color, args.square_texture, args.square_percent_texture,
                     color_choices, texture_choices, args.image_size, args.validation_split, traindir, valdir)

    # Make some circles
    create_shape_set("circle", args.filetype, args.circle_number, args.circle_color,
                     args.circle_percent_color, args.circle_texture, args.circle_percent_texture,
                     color_choices, texture_choices, args.image_size, args.validation_split, traindir, valdir)

    # Make some triangles
    create_shape_set("triangle", args.filetype, args.triangle_number, args.triangle_color,
                     args.triangle_percent_color, args.triangle_texture, args.triangle_percent_texture,
                     color_choices, texture_choices, args.image_size, args.validation_split, traindir, valdir)


if __name__ == "__main__":
    run()
