import cv2
import time

def create_color_mask(frame):
    # Esta é uma função de exemplo. Substitua-a pela sua implementação.
    # Por exemplo, um simples limiar binário:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    return mask

def find_centers(mask):
    # Esta é uma função de exemplo. Substitua-a pela sua implementação.
    # Por exemplo, encontrando contornos e calculando o centro:
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

def run():
    frame = cv2.imread('.\\sources\\img.png')
    mask = create_color_mask(frame)
    centers = find_centers(mask)

    for center in centers:
        if center is not None:
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # Desenhar a linha vermelha atravessando a imagem original
    height, width = frame.shape[:2]
    cv2.line(frame, (0, 0), (width - 1, height - 1), (0, 0, 255), 2)  # Linha vermelha com espessura 2

    cv2.imshow('frame', frame)

    key: int = cv2.waitKey(0)

    if key == ord('q'):
        return
    time.sleep(2000)

if __name__ == "__main__":
    run()
