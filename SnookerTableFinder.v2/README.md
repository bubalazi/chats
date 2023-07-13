
```
PROMPT: 
Find the binary mask that best describes the snooker table green area using HSV and Otsu's method. Assume the mask is a trapezium, since it is a prospectively transformed rectangle. Find cross-sections of the four best-fit lines of this trapezium. Draw  the best-fit lines in red, the cross-sections in green and the diagonals of the trapezium in yellow.  Knowing the dimensions of a standard snooker table, perform the perspective transform and produce a top-down view. Pay attention ordering of the vertices used for the perspective transformation. The vertices should be in the order: top-left, top-right, bottom-right, bottom-left. Finally produce a complete project structure including a README with setup and run instructions, a command line interface and the requirements file.
```

# Snooker Table Perspective Transformation

This project performs a perspective transformation on an image of a snooker table.

## Setup

1. Clone this repository.
2. Install the required Python packages: `pip install -r requirements.txt`
3. Run the script: `python -m src.transform /path/to/image.jpg /path/to/output/dir`

The transformed image will be saved as 'transformed_image.jpg' in the output directory.

## Requirements

- Python 3.7 or later
- OpenCV
- NumPy
- scikit-image
- matplotlib
