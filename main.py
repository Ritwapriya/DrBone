from models.detector import run_yolo
from utils.ai_doctor import generate_zone_report
from reports.report_generator import create_pdf_report
from config.settings import MODEL_PATH, LOGO_PATH, FONT_PATH
from utils.pdf_styles import register_fonts
import datetime

register_fonts(FONT_PATH)

image_path = "test/test.jpg"

# Run YOLO
img_clean_path, img_detailed_path, report_data = run_yolo(MODEL_PATH, image_path)

# Generate AI notes
for entry in report_data:
    entry["AI Doctor Notes"] = generate_zone_report(entry)

# Save PDF
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
pdf_name = f"logs/test/fracture_report_{timestamp}.pdf"

create_pdf_report(report_data, img_clean_path, img_detailed_path, LOGO_PATH, pdf_name)

print(f"\n✅ Report saved successfully: {pdf_name}")
