from __future__ import annotations

from dataclasses import dataclass
import json


@dataclass(slots=True)
class ExternalMLDetectionService:
    """
    Полезный сервис (Adaptee или Service)
    Этот класс можно считать будущим клиентом к реальному ML-сервису
    """

    def analyze_image(self, image_path: str, threshold: float) -> dict:
        # В реальном проекте здесь был бы HTTP-запрос к ml_service с передаче изображения, 
        # а в ответе JSON с предсказаниями. Вот пример такого JSON:
        raw_json_response = """
        {
            "model_version": "detector-v1.0",
            "request_id": "req-12345",
            "predictions": [
                {
                    "class_code": "RS",
                    "score": 0.93,
                    "box": {
                        "left": 10,
                        "top": 15,
                        "right": 90,
                        "bottom": 60
                    }
                },
                {
                    "class_code": "SC",
                    "score": 0.81,
                    "box": {
                        "left": 120,
                        "top": 45,
                        "right": 210,
                        "bottom": 95
                    }
                },
            ],
            "meta": {
                "image_path": "sample_sheet_001.jpg",
                "inference_time_ms": 47
            }
        }
        """

        payload = json.loads(raw_json_response)

        filtered_predictions = [
            item
            for item in payload["predictions"]
            if item["score"] >= threshold
        ]

        return {
            "model_version": payload["model_version"],
            "request_id": payload["request_id"],
            "predictions": filtered_predictions,
            "meta": payload["meta"],
        }