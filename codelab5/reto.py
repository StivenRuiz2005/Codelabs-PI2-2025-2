from ultralytics import YOLO
import cv2
import json
import matplotlib.pyplot as plt
import torch
from ultralytics.nn.tasks import DetectionModel
import time

torch.serialization.add_safe_globals([DetectionModel])

model = YOLO("yolov8n.pt")

print("Iniciando grabacion de 10 segundos")
cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('video_grabado.mp4', fourcc, 20.0, (640, 480))

start_time = time.time()
while (time.time() - start_time) < 10:
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (640, 480))
        out.write(frame)
        cv2.putText(frame, f"Grabando: {10 - int(time.time() - start_time)}s", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('Grabando...', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
out.release()
cv2.destroyAllWindows()
print("✓ Video grabado: video_grabado.mp4")

print("\nProcesando video con YOLO...")
cap = cv2.VideoCapture('video_grabado.mp4')

detecciones_json = []
frame_num = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detectar objetos
    results = model(frame, verbose=False)
    
    frame_data = {
        "frame": frame_num,
        "detecciones": []
    }
    
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            clase_nombre = r.names[cls]
            
            frame_data["detecciones"].append({
                "clase": clase_nombre,
                "confianza": round(conf, 2),
                "bbox": [round(x1), round(y1), round(x2), round(y2)]
            })
    
    detecciones_json.append(frame_data)
    frame_num += 1

cap.release()
print(f"✓ Procesados {frame_num} frames")

with open('detecciones.json', 'w', encoding='utf-8') as f:
    json.dump(detecciones_json, f, indent=2, ensure_ascii=False)
print("✓ Detecciones guardadas en: detecciones.json")

personas_por_frame = []
frames = []

for frame_data in detecciones_json:
    num_personas = sum(1 for det in frame_data["detecciones"] if det["clase"] == "person")
    personas_por_frame.append(num_personas)
    frames.append(frame_data["frame"])

plt.figure(figsize=(12, 6))
plt.plot(frames, personas_por_frame, marker='o', linestyle='-', linewidth=2, markersize=4)
plt.xlabel('Frame', fontsize=12)
plt.ylabel('Número de Personas', fontsize=12)
plt.title('Detección de Personas por Frame (YOLO)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('grafico_personas.png', dpi=300, bbox_inches='tight')
plt.show()


print("\n" + "="*50)
print("RESUMEN:")
print(f"Total de frames procesados: {len(frames)}")
print(f"Promedio de personas por frame: {sum(personas_por_frame)/len(personas_por_frame):.2f}")
print(f"Máximo de personas en un frame: {max(personas_por_frame)}")
print(f"Total de detecciones: {sum(len(f['detecciones']) for f in detecciones_json)}")
print("="*50)