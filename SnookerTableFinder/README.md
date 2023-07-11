# Snooker Table Perspective Transformation

This script performs a perspective transformation on an image of a snooker table to provide a top-down view.

## Prompt
```shell
Find the binary mask that best describes the snooker table green area using HSV. The mask should be a trapezium, since it is a prospectively transformed rectangle. Find cross-sections of the four best-fit lines of this trapezium. Draw  the best-fit lines in red, the cross-sections in green and the diagonals of the trapezium in yellow. Minimize the delta between initial green mask found and the area described by the trapezium.
```

## Setup

1. Ensure that you have Python 3 installed on your machine. You can download Python from [here](https://www.python.org/downloads/).

2. (Optional) It's often good practice to create a virtual environment for your projects to avoid conflicts between dependencies for different projects. If you have `virtualenv` installed, you can create a new environment with:

```bash
   virtualenv .venv
   # Linux/Mac
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate

   pip install -r requirements.txt

   python perspective_table.py <input_image>
```
