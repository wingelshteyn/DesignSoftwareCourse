"""
ml_service package - Quantum 2 (ML Inference Service).

Responsibilities:
  - Accept an image via HTTP POST (multipart/form-data)
  - Pre-process the image
  - Run defect detection via the loaded model (ONNX or PyTorch)
  - Return a JSON response with detected defects (type, bbox, confidence)

Deployed independently from Quantum 1 (Django monolith).
Kubernetes rolling-update enables zero-downtime model updates.
"""
