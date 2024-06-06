import cv2
import numpy as np
import time

class Identificador:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def run(self):
        # while True:
            # ret, frame = self.cap.read()
            frame = cv2.imread('.\sources\img.png')
            mask = create_color_mask(frame)
            centers = find_centers(mask)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)


            for center in centers:
                if center is not None:
                    cv2.circle(mask, center, 5, (0, 0, 255), -1)
            
            height, width = mask.shape[:2]
            cv2.line(mask, (0, 0), (width - 1, height - 1), (0, 0, 255), 2)  # Linha vermelha com espessura 2

            cv2.imshow('frame', mask)

            key: int = cv2.waitKey(1)

            if key == ord('q'):
                return
            time.sleep(2000)
                # break

def find_centers(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    centers = []
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centers.append((cX, cY))
        else:
            centers.append(None)
    return centers

def create_color_mask(frame):
    try:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_color, upper_color = ([50, 40, 50], [90, 255, 255])

        color_mask = cv2.inRange(hsv, np.array(lower_color), np.array(upper_color))

        result = cv2.bitwise_and(frame, frame, mask=color_mask)

        return color_mask

    except Exception as e:
        print(f"Error creating color mask: {e}")
        return None


if __name__ == "__main__":
    ide = Identificador()

    ide.run()