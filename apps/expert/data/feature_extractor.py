from __future__ import annotations

import json
import os
from os import PathLike
from typing import Dict, List, Tuple, Any

import numpy as np
from tqdm.auto import tqdm
import pandas as pd
import torch
from apps.expert.data.annotation.speech_to_text import (
    get_all_words,
    get_phrases,
    get_sentences,
    transcribe_video,
)
from apps.expert.data.detection.face_detector import FaceDetector
from apps.expert.data.video_reader import VideoReader


class FeatureExtractor:
    """Extracting data from a video presentation.

    The FeatureExtractor extracts information about a speaker from a video presentation.
    Enabled speech recognition module for obtaining stripped phrases of the speaker and
    the full text of the speech.

    Returns:
        str: Path to the folder with the results of recognition modules.

    Raises:
        NotImplementedError: If 'language' is not equal to 'en' or 'ru'.
        Warning: If failed to detect faces. Recommended to change 'min_detection_confidence'.

    Example:
        >>> test_video_path: str = "test_video.mp4"
        >>> extractor = FeatureExtractor(video_path=test_video_path)
        >>> extractor.get_features()
    """

    def __init__(
        self,
        video_path: str | PathLike,
        cache_capacity: int = 10,
        device: torch.device | None = None,
        stt_mode: str = "server",
        model_selection: int = 0,
        min_detection_confidence: float = 0.5,
        max_num_faces: int = 1,
        lang: str = "ru",
        output_dir: str | PathLike | None = None,
    ) -> None:
        """
        Initialization of audio, text and video models parameters.

        Args:
            video_path (str | PathLike): Path to local video file.
            cache_capacity (int, optional): Buffer size for storing frames. Defaults to 10.
            device (torch.device | None, optional): Device type on local machine (GPU recommended). Defaults to None.
            stt_mode (str, optional): Model configuration for speech recognition ['server', 'local']. Defaults to 'server'.
            model_selection (int, optional): 0 or 1. 0 to select a short-range model that works best
                for faces within 2 meters from the camera, and 1 for a full-range model best for
                faces within 5 meters. Defaults to 0.
            min_detection_confidence (float, optional): Minimum confidence value ([0.0, 1.0]) for face
                detection to be considered successful. Defaults to 0.5.
            max_num_faces (int, optional): Maximum number of faces to detect. Defaults to 10.
            lang (str, optional): Speech language for text processing ['ru', 'en']. Defaults to 'en'.
            output_dir (str | Pathlike | None, optional): Path to the folder for saving results. Defaults to None.
        """
        self.video_path = video_path
        self.cache_capacity = cache_capacity
        self.stt_mode = stt_mode
        self.video = VideoReader(
            filename=video_path, cache_capacity=self.cache_capacity
        )

        self._device = torch.device("cpu")
        if device is not None:
            self._device = device

        self.model_selection = model_selection
        self.min_detection_confidence = min_detection_confidence
        self.max_num_faces = max_num_faces
        self.detector = FaceDetector(
            model_selection=0,
            min_detection_confidence=self.min_detection_confidence,
            max_num_faces=self.max_num_faces,
        )
        self.deep_detector = FaceDetector(
            model_selection=1,
            min_detection_confidence=self.min_detection_confidence,
            max_num_faces=self.max_num_faces,
        )

        if lang not in ["en", "ru"]:
            raise NotImplementedError("'lang' must be 'en' or 'ru'.")
        self.lang = lang

        if output_dir is not None:
            self.temp_path = output_dir
        else:
            basename = os.path.splitext(os.path.basename(video_path))[0]
            self.temp_path = os.path.join("temp", basename)
        if not os.path.exists(self.temp_path):
            os.makedirs(self.temp_path)

        self.stamps: list[Tuple[float, float]] = []
        self.transcription: dict[str, Any] = dict()
        self.full_text = ""
        self.face_features = []
        self.annotations = []

    @property
    def device(self) -> torch.device:
        """Check the device type.

        Returns:
            torch.device: Device type on local machine.
        """
        return self._device

    def analyze_speech(self) -> List:
        """Method for processing audio signal from video."""

        self.transcription = transcribe_video(
            video_path=self.video_path,
            lang=self.lang,
            model=self.stt_mode,
            device=self._device,
        )

        self.stamps = self.transcription["stamps"]
        self.full_text = self.transcription["full_text"]
        self.transcribed_text = self.transcription["transcribed_text"]
        self.sentences = self.transcription["sentences"]

        with open(os.path.join(self.temp_path, "diarization.json"), "w") as filename:
            json.dump(self.stamps, filename)
        with open(os.path.join(self.temp_path, "transcription.json"), "w") as filename:
            json.dump(self.transcribed_text, filename)
        with open(
            os.path.join(self.temp_path, "text.txt"), "w", encoding="utf-8"
        ) as filename:
            filename.write(self.full_text)
        with open(os.path.join(self.temp_path, "sentences.json"), "w") as filename:
            json.dump(self.sentences, filename)

        self.phrases = get_phrases(self.transcribed_text)
        with open(os.path.join(self.temp_path, "phrases.json"), "w") as filename:
            json.dump(self.phrases, filename)

        return self.stamps

    def get_features(self) -> str:
        """Method for extracting features from video.

        Returns:
            str: Path to the folder with the results of recognition modules.
        """
        self.stamps = self.analyze_speech()
        fps = self.video.fps

        for stamp in tqdm(self.stamps):
            start_sec, finish_sec = stamp
            start_frame, finish_frame = (
                int(-(-start_sec * fps // 1)),
                int(-(-finish_sec * fps // 1)),
            )
            # Avoiding out-of-range error after diarization.
            finish_frame = (
                finish_frame if finish_frame <= len(self.video) else len(self.video)
            )
            for frame_idx in range(start_frame, finish_frame, int(fps)):
                face_batch = self.detector.detect(self.video[frame_idx])

                # Recording if face was detected.
                if face_batch is not None:
                    for face_location in face_batch:
                        self.face_features.append(
                            {
                                "speaker_by_video": 0,
                                "speaker_by_audio": "SPEAKER_00",
                                "video_path": self.video_path,
                                "time_sec": int(-(-frame_idx // fps)),
                                "frame_index": frame_idx,
                                "face_bbox": face_location,
                            }
                        )
                else:
                    face_batch = self.deep_detector.detect(self.video[frame_idx])
                    # Recording if face was detected.
                    if face_batch is not None:
                        for face_location in face_batch:
                            self.face_features.append(
                                {
                                    "speaker_by_video": 0,
                                    "speaker_by_audio": "SPEAKER_00",
                                    "video_path": self.video_path,
                                    "time_sec": int(-(-frame_idx // fps)),
                                    "frame_index": frame_idx,
                                    "face_bbox": face_location,
                                }
                            )

        if len(self.face_features) == 0:
            raise Warning(
                "Failed to detect faces. Try to change 'min_detection_confidence' manually."
            )

        self.face_features = pd.DataFrame(self.face_features)
        self.face_features.to_json(
            os.path.join(self.temp_path, "features.json"), orient="records"
        )

        return self.temp_path
