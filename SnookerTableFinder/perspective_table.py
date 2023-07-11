import cv2
import numpy as np

def process_image(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to HSV
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define range for green color in HSV
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])

    # Create a binary mask for the green area
    mask = cv2.inRange(img_hsv, lower_green, upper_green)

    # Find the contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours by area and keep the largest one
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

    # Approximate the contour with a polygon
    epsilon = 0.02 * cv2.arcLength(contours[0], True)
    approx = cv2.approxPolyDP(contours[0], epsilon, True)

    # Get the coordinates of the vertices
    vertices = approx.squeeze()

    # Sort the points based on their x-coordinates
    vertices = vertices[vertices[:, 0].argsort()]

    # From the sorted array, the point with the smaller y-coordinate comes first
    if vertices[0, 1] > vertices[1, 1]:
        vertices[0], vertices[1] = vertices[1], vertices[0].copy()

    if vertices[2, 1] < vertices[3, 1]:
        vertices[2], vertices[3] = vertices[3], vertices[2].copy()

    # Define dimensions of a standard snooker table
    length = 1200  # in arbitrary units, keeping aspect ratio
    width = 600  # in arbitrary units, keeping aspect ratio

    # Define the target points for the perspective transformation
    target_pts = np.float32([[0, 0], [length, 0], [length, width], [0, width]])

    # Perform the perspective transform
    M = cv2.getPerspectiveTransform(np.float32(vertices), target_pts)
    img_transformed = cv2.warpPerspective(img, M, (length, width))

    # Save the transformed image
    cv2.imwrite('transformed_image.png', img_transformed)

if __name__ == "__main__":
    import sys
    process_image(sys.argv[1])
