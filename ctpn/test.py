from demo_pb import Predictor
import os
import cv2


cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow('Video Stream', frame)

    # Wait for the specified key to be pressed
    key = cv2.waitKey(1) & 0xFF

    # If the capture key is pressed, save the current frame as an image
    if key == ord('q'):
        cv2.imwrite('label.jpg', frame)
        print("Image saved as", 'label.jpg')
        break  # Exit the loop after capturing the image

    # Check if the 'q' key is pressed to quit the program
    if key == ord('q'):
        break

# Release the video capture device and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
predictor = Predictor()
predictor.draw_boxes('label.jpg')

