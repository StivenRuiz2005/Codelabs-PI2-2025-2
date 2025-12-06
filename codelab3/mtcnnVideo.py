import cv2, dlib, time
import numpy as np

def run_test(upsample=0, max_frames=200):
    detector = dlib.get_frontal_face_detector()
    cap = cv2.VideoCapture("video_rostros.mp4")

    frames = 0
    t0 = time.time()
    total_faces = 0

    while frames < max_frames:
        ok, frame = cap.read()
        if not ok:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, upsample)
        total_faces += len(rects)

        frames += 1

    cap.release()
    fps = frames / (time.time() - t0)
    return fps, total_faces

fps0, faces0 = run_test(upsample=0)
fps1, faces1 = run_test(upsample=1)

print("=== RESULTADOS ===")
print(f"UPSAMPLE 0 -> FPS: {fps0:.2f}, ROSTROS DETECTADOS: {faces0}")
print(f"UPSAMPLE 1 -> FPS: {fps1:.2f}, ROSTROS DETECTADOS: {faces1}")
