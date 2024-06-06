import cv2
import numpy as np

vals = []

def on_mouse(event, x, y, flags, param):
    # Check if the event was the left mouse button being clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the BGR pixel value at the clicked location
        pixel = frame[y, x]

        # Convert BGR to HSV and print the pixel value
        hsv_pixel = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)
        print("HSV:", hsv_pixel[0][0])
        # Append the pixel value to the values list
        vals.append(hsv_pixel[0][0])

def get_thresh_from_vals(vals: np.array) -> np.array:
    # Calculate the minimum and maximum values for each channel
    min_h, min_s, min_v = np.min(vals, axis=0)
    max_h, max_s, max_v = np.max(vals, axis=0)
    lower_color = [min_h, min_s, min_v]
    upper_color = [max_h, max_s, max_v]
    # Output the results
    print(f"lower bound: {lower_color}")
    print(f"upper bound: {upper_color}")
    return lower_color, upper_color


# Open a connection to the webcam (you may need to change the index)
cap = cv2.VideoCapture('sources\\Laser_Identify.mp4')

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame = cv2.resize(frame, (1280, 720))
    cv2.imshow('frame', frame)

    # Set the callback function for mouse events
    cv2.setMouseCallback('frame', on_mouse)  # Make sure 'Frame' matches the window name in cv2.imshow
    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break

# Release the capture when everything is done
cap.release()
cv2.destroyAllWindows()
low, up = get_thresh_from_vals(vals)