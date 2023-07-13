import cv2
import numpy as np
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
import argparse
import os

def plot_transform(mask, vertices, cross_sections, img):
    img_lines = img.copy()
    for i in range(4):
        p1, p2 = vertices[i], vertices[(i+1)%4]
        img_lines = cv2.line(img_lines, tuple(p1), tuple(p2), (0, 0, 255), 3)

    # Draw the cross-sections in green
    for i in range(4):
        p1, p2 = cross_sections[i], cross_sections[(i+1)%4]
        img_lines = cv2.line(img_lines, tuple(p1.astype(int)), tuple(p2.astype(int)), (0, 255, 0), 3)
    # Draw the diagonals of the trapezium in yellow
    img_lines = cv2.line(img_lines, tuple(vertices[0]), tuple(vertices[2]), (0, 255, 255), 3)
    img_lines = cv2.line(img_lines, tuple(vertices[1]), tuple(vertices[3]), (0, 255, 255), 3)

    # Create the destination points for the perspective transformation
    dst_pts = np.array([[0, 0], [3569, 0], [3569, 1778], [0, 1778]], dtype=np.float32)

    # Perform the perspective transformation
    M = cv2.getPerspectiveTransform(vertices.astype(np.float32), dst_pts)
    img_transformed = cv2.warpPerspective(img, M, (1778, 3569))

    # Show the original image with lines and cross-sections, and the transformed image
    axs[0].imshow(cv2.cvtColor(img_lines, cv2.COLOR_BGR2RGB))
    axs[0].set_title('Original image with lines and cross-sections')
    axs[1].imshow(cv2.cvtColor(img_transformed, cv2.COLOR_BGR2RGB))
    axs[1].set_title('Perspective transformed image')
    plt.show()

def transform_image(input_path, output_dir):
    # Load the image
    img = cv2.imread(input_path)

    # Convert the image to HSV
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Create a binary mask for the green color
    green_low = np.array([30, 100, 100])
    green_high = np.array([85, 255, 255])
    mask = cv2.inRange(hsv_img, green_low, green_high)

    # Apply Otsu's thresholding method
    thresh_val = threshold_otsu(mask)
    binary_mask = mask > thresh_val

    # Find the largest contour in the mask, which should correspond to the table
    contours, _ = cv2.findContours(binary_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)

    # Approximate the contour to a polygon
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx_contour = cv2.approxPolyDP(largest_contour, epsilon, True)

    # The polygon should be a trapezium, so it should have 4 vertices
    if len(approx_contour) != 4:
        raise ValueError('The largest contour does not correspond to a trapezium')

    vertices = approx_contour.squeeze()
    # Sort the points based on their x-coordinates
    vertices = vertices[vertices[:, 0].argsort()]

    # From the sorted array, the point with the smaller y-coordinate comes first
    if vertices[0, 1] > vertices[1, 1]:
        vertices[0], vertices[1] = vertices[1], vertices[0].copy()

    if vertices[2, 1] < vertices[3, 1]:
        vertices[2], vertices[3] = vertices[3], vertices[2].copy()

    # Find the best-fit lines for the trapezium
    lines = np.empty((4, 3))
    for i in range(4):
        p1, p2 = vertices[i], vertices[(i+1)%4]
        lines[i, :2] = p2 - p1
        lines[i, 2] = -np.cross(p1, p2)

    # Calculate the cross-sections of the lines
    cross_sections = np.empty((4, 2))
    for i in range(4):
        cross_sections[i] = np.cross(lines[i], lines[(i+1)%4])[:2] / np.cross(lines[i], lines[(i+1)%4])[2]

    # Define dimensions of a standard snooker table
    length = 1200  # in arbitrary units, keeping aspect ratio
    width = 600  # in arbitrary units, keeping aspect ratio

    # Define the target points for the perspective transformation
    target_pts = np.float32([[0, 0], [length, 0], [length, width], [0, width]])

    # Perform the perspective transform
    M = cv2.getPerspectiveTransform(np.float32(vertices), target_pts)
    img_transformed = cv2.warpPerspective(img, M, (length, width))

    # # Save the transformed image
    if output_dir is not None:
        output_path = os.path.join(output_dir, 'transformed_image.jpg')
        cv2.imwrite(output_path, img_transformed)
    else:
        plot_transform(mask, vertices, cross_sections, img)

def transform_video(input_path, output_dir=None):
    # Open the video file
    cap = cv2.VideoCapture(input_path)

    # Loop over the frames of the video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        transform_image(frame, None)

    # Release the video file
    cap.release()

def main():
    # Define the command-line arguments
    parser = argparse.ArgumentParser(description='Perform a perspective transformation on an image or video of a snooker table.')
    parser.add_argument('input_path', help='Path to the input image or video file.')
    parser.add_argument('output_dir', help='Directory where the output will be saved.')
    parser.add_argument('--video', action='store_true', help='Set this flag if the input is a video.')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Perform the perspective transformation
    if args.video:
        transform_video(args.input_path, args.output_dir)
    else:
        transform_image(args.input_path, args.output_dir)

if __name__ == '__main__':
    main()
