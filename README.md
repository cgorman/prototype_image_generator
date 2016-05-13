# Prototype Image Generator

Script to generate image datasets which have statistical properties associated with prototypical individuals. The script generates a set of circles, triangles, and squares which have the properties of color and texture. For example, the prototypical circle may be green and solid or green and striped. Script also handles training and validation splitting. The output directory will have a training folder and, if you supply the argument, a validation folder.

N.B. the textures and colors are independent, so a token object can be the prototypical color without being the prototypical texture, even if they have the same probability (e.g. 80% of squares are black and 80% are striped)

I tried commenting everything but the methods to generate images are big and goofy so I apologize for that.

**FYI: Randomly generated stats have not been implemented yet**

## Usage
Script accepts arguments from a file. Simply separate each option with its input with a newline. Then call the script with `python generate_dataset.py @path/to/args.txt`

I recommend gzipping the output directory once you verify that it is what you wanted

The argument for subfolder lables is in place because Google's inception v3 training for TensorFlow expects that as input and it's easier to just have that as an option instead of rewriting their code

```
usage: generate_dataset.py [-h] [--output-directory OUTPUT_DIRECTORY]
                           [--dataset-name DATASET_NAME]
                           [--filetype {jpg,png}] [--random-stats]
                           [--image-size IMAGE_SIZE]
                           [--validation-split VALIDATION_SPLIT]
                           [--square-color {blue,green,black,red}]
                           [--square-percent-color SQUARE_PERCENT_COLOR]
                           [--square-texture {solid,striped,blank}]
                           [--square-percent-texture SQUARE_PERCENT_TEXTURE]
                           [--square-number SQUARE_NUMBER]
                           [--circle-color {blue,green,black,red}]
                           [--circle-percent-color CIRCLE_PERCENT_COLOR]
                           [--circle-texture {solid,striped,blank}]
                           [--circle-percent-texture CIRCLE_PERCENT_TEXTURE]
                           [--circle-number CIRCLE_NUMBER]
                           [--triangle-color {blue,green,black,red}]
                           [--triangle-percent-color TRIANGLE_PERCENT_COLOR]
                           [--triangle-texture {solid,striped,blank}]
                           [--triangle-percent-texture TRIANGLE_PERCENT_TEXTURE]
                           [--triangle-number TRIANGLE_NUMBER]

Script to generate prototype images for research on category development.
Generates images which conform to certain statistics in order to test
hypotheses about prototype theory. NOTE: Pass an arguments file prefixed with
@ as an arg to include the arguments listed in that file. Each argument and
value should be on separate lines.

optional arguments:
  -h, --help            show this help message and exit
  --output-directory OUTPUT_DIRECTORY
                        The directory to save the dataset to.
  --dataset-name DATASET_NAME
                        Colloquial name for this dataset. Will be the name of
                        the final output directory.
  --filetype {jpg,png}  What to save the output images as
  --random-stats        Script will generate sensible statistics for shapes at
                        random. All shapes will be used. If this argument is
                        set, the script will ignore any manual statistics that
                        follow!
  --image-size IMAGE_SIZE
                        Size (in pixels) of each image. Images are square so
                        just enter one number
  --validation-split VALIDATION_SPLIT
                        If set, this percentage of images will be put into the
                        validation directory. Value must be in range [0.0,
                        1.0]

Square Statistics:
  --square-color {blue,green,black,red}
                        The color of the prototypical square
  --square-percent-color SQUARE_PERCENT_COLOR
                        The percent of squares that are the previous color.
                        The rest will be random. Value must be in range [0.0,
                        1.0]
  --square-texture {solid,striped,blank}
                        The texture of the prototypical square
  --square-percent-texture SQUARE_PERCENT_TEXTURE
                        The percent of squares that are the previous texture.
                        The rest will be random. Value must be in range [0.0,
                        1.0]
  --square-number SQUARE_NUMBER
                        The number of squares we should generate as output

Circle Statistics:
  --circle-color {blue,green,black,red}
                        The color of the prototypical circle
  --circle-percent-color CIRCLE_PERCENT_COLOR
                        The percent of circles that are the previous color.
                        The rest will be random. Value must be in range [0.0,
                        1.0]
  --circle-texture {solid,striped,blank}
                        The texture of the prototypical circle
  --circle-percent-texture CIRCLE_PERCENT_TEXTURE
                        The percent of circles that are the previous texture.
                        The rest will be random. Value must be in range [0.0,
                        1.0]
  --circle-number CIRCLE_NUMBER
                        The number of circles we should generate as output

Triangle Statistics:
  --triangle-color {blue,green,black,red}
                        The color of the prototypical triangle
  --triangle-percent-color TRIANGLE_PERCENT_COLOR
                        The percent of triangles that are the previous color.
                        The rest will be random. Value must be in range [0.0,
                        1.0]
  --triangle-texture {solid,striped,blank}
                        The texture of the prototypical triangle
  --triangle-percent-texture TRIANGLE_PERCENT_TEXTURE
                        The percent of triangles that are the previous
                        texture. The rest will be random. Value must be in
                        range [0.0, 1.0]
  --triangle-number TRIANGLE_NUMBER
                        The number of triangles we should generate as output

(Again, you may want to use a file instead)
```
