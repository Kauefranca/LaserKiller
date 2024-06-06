import cv2
import threading
import numpy as np
import time
import os
import requests
import threading

from dotenv import load_dotenv
load_dotenv()

LASER_AREA = 100
ESP_CAM = os.getenv('ESP_CAM_IP')
VIDEO_SRC = ESP_CAM + ':81/stream'
LASER_STATE = False

class Identificador:
    def __init__(self):
        try:
            # self._camera = cv2.VideoCapture(VIDEO_SRC)
            self._camera = cv2.VideoCapture('sources\\Laser_Identify.mp4')
        except:
            self._camera = cv2.VideoCapture(1)

        self._lock = threading.Lock()

    def run(self):
        while True:
            con, frame = self._camera.read()
            key: int = cv2.waitKey(1)

            frame = processFrame(frame)

            if key == ord('q'):
                break

            cv2.imshow('frame', frame)

    def read(self):
        with self._lock:
            con, frame = self._camera.read()

            if not con:
                raise ConnectionError(f"A conexão com a câmera {VIDEO_SRC} foi perdida!")

            ret, jpeg = cv2.imencode('.jpg', processFrame(frame))

            return jpeg.tobytes()

    def __del__(self):
        self._camera.release()
        cv2.destroyAllWindows()
        print("Objeto Camera destruído")

def processFrame(frame):
    global LASER_STATE

    frame = cv2.resize(frame, (640, 640))
    height, width = frame.shape[:2]

    mask = create_color_mask(frame)
    centers = find_centers(mask)
    
    passed_line = False

    for center in centers:
        if center is not None:
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            if (center[1] > round((height / 2) - LASER_AREA) and center[1] < round((height / 2) + LASER_AREA)):
                passed_line = True

    if passed_line and not LASER_STATE:
        threading.Thread(target=send_request, args=(ESP_CAM + "/control?var=toggle-laser&val=1",)).start()
        LASER_STATE = True

    if not passed_line and LASER_STATE:
        threading.Thread(target=send_request, args=(ESP_CAM + "/control?var=toggle-laser&val=0",)).start()
        LASER_STATE = False

    result = cv2.line(frame, (0, round(height / 2)), (width, round(height / 2)), (0, 0, 255), 2)

    return result

def send_request(url):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao ligar o laser: {e}")

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

        lower_color, upper_color = ([57, 240, 55], [60, 255, 255]) # RANGE CORES VIDEO
        # lower_color, upper_color = ([75, 220, 120], [90, 255, 190]) # RANGE CORES IRL

        color_mask = cv2.inRange(hsv, np.array(lower_color), np.array(upper_color))

        result = cv2.bitwise_and(frame, frame, mask=color_mask)

        return color_mask

    except Exception as e:
        print(f"Error creating color mask: {e}")
        return None


if __name__ == "__main__":
    ide = Identificador()

    ide.run()