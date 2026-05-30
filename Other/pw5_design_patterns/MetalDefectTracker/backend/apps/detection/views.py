from django.shortcuts import render

# Create your views here.

from apps.detection.adapters import MLServiceAdapter
from apps.detection.external_client import ExternalMLDetectionService
from apps.detection.services import DetectionApplicationService



external_client = ExternalMLDetectionService()
adapter = MLServiceAdapter(external_client)
service = DetectionApplicationService(prediction_provider=adapter)

defects = service.detect(image_path="sample_sheet_001.jpg", threshold=0.8)

for defect in defects:
    print(defect.describe())