# models/detector.py

import cv2
import numpy as np
import datetime
import os
from ultralytics import YOLO
from utils.image_processing import analyze_contours

def run_yolo(model_path, image_path):
    model = YOLO(model_path)
    results = model.predict(source=image_path, imgsz=640, conf=0.25, save=False)

    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_clean, img_detailed = img.copy(), img.copy()

    gray_full = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    lap_var_full = cv2.Laplacian(gray_full, cv2.CV_64F).var()
    sharpness_full = round(min(100, (lap_var_full / 200.0) * 100), 2)

    report_data = []
    px_to_mm = 0.2645833333
    zone_id = 1

    for r in results:
        for box, conf in zip(r.boxes.xyxy, r.boxes.conf):
            x1, y1, x2, y2 = map(int, box[:4])
            confidence = float(conf)
            cv2.rectangle(img_clean, (x1, y1), (x2, y2), (0, 255, 0), 2)
            roi = img[y1:y2, x1:x2]
            entry = {"Zone": f"Fracture Zone {zone_id}"}
            contour_data = analyze_contours(roi, x1, y1, x2, y2, img_detailed, px_to_mm)
            entry.update(contour_data)

            U_model = 1 - confidence
            U_image = 1 - (sharpness_full / 100)
            shift_norm = min(entry["Shift (mm)"] / 50, 1) if entry["Shift (mm)"] else 0
            U_geom = 0.5 * shift_norm
            total_uncertainty = 100 * (0.4 * U_model + 0.3 * U_image + 0.3 * U_geom)

            entry["Uncertainty (%)"] = round(total_uncertainty, 2)
            report_data.append(entry)
            zone_id += 1

    # Save both images
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_path = f"logs/images/clean_{timestamp}.png"
    detailed_path = f"logs/test/detailed_{timestamp}.png"

    cv2.imwrite(clean_path, cv2.cvtColor(img_clean, cv2.COLOR_RGB2BGR))
    cv2.imwrite(detailed_path, cv2.cvtColor(img_detailed, cv2.COLOR_RGB2BGR))

    print(f"✅ Images saved: {clean_path}, {detailed_path}")
    return clean_path, detailed_path, report_data
