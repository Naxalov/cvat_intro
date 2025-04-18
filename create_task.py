from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Iterable, List

from dotenv import load_dotenv
from cvat_sdk.api_client import ApiClient, Configuration, exceptions, models


def open_images(paths: Iterable[str | Path]) -> List[object]:
    """
    Resolve each path, open in binary mode, and return the handles.

    Args:
        paths (Iterable[str | Path]): A list of paths to open.

    Returns:
        List[object]: A list of file handles for the opened images.

    Raises:
        FileNotFoundError: If no valid images are supplied.
    """
    handles: List[object] = []  # List to store file handles

    for p in paths:
        p = Path(p).expanduser().resolve()  # Resolve the path
        if not p.is_file():
            print(f"⚠️  File not found: {p}")  # Warning for missing file
            continue
        handles.append(p.open("rb"))  # Open file in binary mode and append

    if not handles:
        raise FileNotFoundError("No valid images supplied")  # Error if no images

    return handles  # Return the list of file handles


def create_task_and_upload(
    project_id: int,
    task_name: str,
    image_paths: Iterable[str | Path],
    *,
    image_quality: int = 80,
) -> None:
    """Create a task inside *project_id* and immediately attach *image_paths*."""
    load_dotenv()

    cfg = Configuration(
        host=os.getenv("CVAT_HOST"),
        username=os.getenv("CVAT_USERNAME"),
        password=os.getenv("CVAT_PASSWORD"),
    )



    file_handles = open_images(image_paths)

    try:
        with ApiClient(cfg) as client:
            # 1 Create the task shell inside the project
            task,_ = client.tasks_api.create(
                models.TaskWriteRequest(
                    name=task_name,
                    project_id=project_id,
                    segment_size=50,  
                    overlap=10,
                ),
                x_organization=os.getenv("CVAT_ORGANIZATION"),
            )
    

            # 2 Prepare the data payload
            data_req = models.DataRequest(
                image_quality=image_quality,
                client_files=file_handles,
         
            )

            # 3 Upload the images in the same session
            client.tasks_api.create_data(
                id=task.id,
                data_request=data_req,
                _content_type="multipart/form-data",
            )

            print(
                f"✅ Task {task.id} ('{task.name}') created in project {project_id} "
                f"with {len(file_handles)} image(s) attached."
            )

    except exceptions.ApiException as err:
        print(f"❌ CVAT API error: {err}")
    finally:
        for f in file_handles:
            f.close()


if __name__ == "__main__":
    PROJECT_ID = 17                          # 🔁 ← your existing project ID
    TASK_NAME  = "FACE 2"         # descriptive name
    IMAGES_FOLDER     = '/Users/naxalov/github/cradle/face-recognition-benchmark/images'

    IMAGES = [str(p) for p in Path(IMAGES_FOLDER).glob("*.jpg")]

    
    create_task_and_upload(PROJECT_ID, TASK_NAME, IMAGES)
