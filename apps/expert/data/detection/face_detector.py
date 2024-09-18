from __future__ import annotations

from typing import List

import mediapipe
import numpy as np


class FaceDetector:
    """Face detection and embedding implementation.

    FaceDetector processes an BGR image and returns a list of the detected face embeddings and bounding boxes.

    Example:
        >>> face_detector = FaceDetector(model_selection=0, min_detection_confidence=0.9)
    """

    def __init__(
        self,
        model_selection: int = 0,
        min_detection_confidence: float = 0.5,
        max_num_faces: int = 1,
    ) -> None:
        """
        Args:
            model_selection (int, optional): 0 or 1. 0 to select a short-range model that works
                best for faces within 2 meters from the camera, and 1 for a full-range
                model best for faces within 5 meters. Defaults to 0.
            min_detection_confidence (float, optional): Minimum confidence value ([0.0, 1.0]) for face
                detection to be considered successful. Defaults to 0.75.
            max_num_faces (int, optional): Maximum number of faces to detect. Defaults to 10.
        """
        super().__init__()

        self.max_num_faces = max_num_faces
        face_detector = mediapipe.solutions.face_detection
        self.face_detector = face_detector.FaceDetection(
            model_selection=model_selection,
            min_detection_confidence=min_detection_confidence,
        )

    def detect(self, image: np.ndarray) -> List:
        """
        Args:
            image (np.ndarray): RGB image represented as numpy ndarray.

        Returns:
            List: List with detected face locations.
        """

        face_array = []
        image_height, image_width = image.shape[:2]
        prediction = self.face_detector.process(image)

        if prediction.detections:
            for n, idx in zip(
                range(self.max_num_faces), range(len(prediction.detections))
            ):
                bounding_box = prediction.detections[
                    idx
                ].location_data.relative_bounding_box
                face_location = [
                    [
                        int(bounding_box.xmin * image_width),
                        int(bounding_box.ymin * image_height),
                    ],
                    [
                        int(bounding_box.width * image_width),
                        int(bounding_box.height * image_height),
                    ],
                ]

                if sum([sum(loc) for loc in face_location]) == sum(
                    [sum(map(abs, loc)) for loc in face_location]
                ):
                    face_array.append(face_location)

        return face_array
