"""
Public API of the administration module
"""

from __future__ import annotations
from typing import TYPE_CHECKING


class CameraConfigService:
    """Camera settings management"""

    def get_or_create_settings():
        pass

    def update_settings():
        pass


class DefectTypeService:
    """Defect catalog management"""

    def list_defect_types() :
        pass

    def add_defect_type():
        pass

    def get_other_defect_images():
        pass


class ModelVersionService:
    """ML model version lifecycle"""

    def list_versions():
        pass

    def get_active_version():
        pass

    def deploy_version():
        pass

    def rollback():
        pass

    def set_confidence_threshold():
        pass


class RetrainingService:
    """Model fine-tuning workflow"""

    def initiate_retraining():
        pass

    def get_job():
        pass
