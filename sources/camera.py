import cv2
import threading
import os
from dotenv import load_dotenv

load_dotenv()

VIDEO_SRC = os.getenv('VIDEO_SRC')

class Camera:
    def __init__(self):
        try:
            # self._camera = cv2.VideoCapture(VIDEO_SRC)
            self._camera = cv2.VideoCapture(1)
        except:
            self._camera

        self._lock = threading.Lock()
        
    def __del__(self):
        self._camera.release()
        cv2.destroyAllWindows()
        print("Objeto Camera destruído")

    def read(self):
        with self._lock:
            con, cap = self._camera.read()

            if not con:
                raise ConnectionError(f"A conexão com a câmera {VIDEO_SRC} foi perdida!")

            return cap

if __name__ == "__main__":
    cam = Camera()

    while True:
        cv2.imshow("UniRecognition", cam.read())
        cv2.waitKey(1)