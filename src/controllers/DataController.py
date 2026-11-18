from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os


class DataController(BaseController):

    def __init__(self):

        super().__init__()

    def validate_uploaded_data(self, file: UploadFile):

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.app_settings.FILE_MAX_SIZE:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value

    def generate_unique_file_path(self, original_file_name: str, project_id: str):

        project_path = ProjectController().get_project_path(project_id=project_id)

        random_key = self.generate_random_string()

        cleaned_file_name = self.get_clean_file_name(original_file_name=original_file_name)

        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_file_name
        )

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name
            )

        return new_file_path, random_key + "_" + cleaned_file_name

    @staticmethod
    def get_clean_file_name(original_file_name: str):

        # replace spaces with underscores first, otherwise the regex removes them
        cleaned_file_name = original_file_name.strip().replace(" ", "_")

        # keep only letters, digits, underscore, dot and dash
        cleaned_file_name = re.sub(r"[^\w.\-]", "", cleaned_file_name)

        return cleaned_file_name
