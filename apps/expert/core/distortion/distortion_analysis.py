from __future__ import annotations

import json
import os
from os import PathLike
from typing import Optional, Tuple, Union

import pandas as pd
import torch

from apps.expert.core.distortion.dist_model import DistortionModel
from apps.expert.data.annotation.speech_to_text import get_phrases


class DistortionDetector:
    """Determination of expert congitive distortions.

    Args:
        transcription_path (str | PathLike): Path to JSON file with text transcription.
        diarization_path (str | PathLike): Path to JSON file with diarization information.
        face_image (str | PathLike): Path to face image selected by user.
        features_path (str | PathLike): Path to JSON file with information about detected faces.
        video_path (str | PathLike): Path to local video file.
        lang (str, optional): Speech language for text processing ['ru', 'en']. Defaults to 'en'.
        duration: Length of intervals for extracting features. Defaults to 10.
        device (torch.device | None, optional): Device type on local machine (GPU recommended). Defaults to None.
        output_dir (str | Pathlike | None, optional): Path to the folder for saving results. Defaults to None.
        return_path (bool): Flag to define the return mode for get_congruence. True is for path, False is for dict. Defaults to False

    Returns:
        Tuple[str, str]: Paths to the divided and aggreagated reports.

    Raises:
        NotImplementedError: If 'lang' is not equal to 'en' or 'ru'.

    Example:
        >>> import torch
        >>> dist_detector = DistortionDetector(
                video_path="test_video.mp4",
                features_path="temp/test_video/features.json",
                transcription_path="temp/test_video/transcription.json",
                diarization_path="temp/test_video/diarization.json",
                device=torch.device("cuda:0"),
            )
        >>> dist_detector.get_distortion()
        ("temp/test_video/div_distortions.json", "temp/test_video/agg_distortions.json")
    """

    def __init__(
        self,
        transcription_path: Union[str, PathLike],
        diarization_path: Union[str, PathLike],
        features_path: Union[str, PathLike],
        video_path: Union[str, PathLike],
        lang: Optional[str] = "en",
        duration: Optional[int] = 10,
        device: Optional[Union[torch.device, None]] = None,
        output_dir: Optional[Union[str, PathLike]] = None,
        return_path: bool = False,
    ) -> None:
        if lang not in ["en", "ru"]:
            raise NotImplementedError("'lang' must be 'en' or 'ru'.")

        self.lang = lang
        self.video_path = video_path
        self.features_path = features_path
        self.transcription_path = transcription_path
        self.duration = duration

        self._device = torch.device("cpu")
        if device is not None:
            self._device = device

        with open(diarization_path, "r") as file:
            self.stamps = json.load(file)

        with open(transcription_path, "r") as file:
            self.words = json.load(file)

        self.dist_mod = DistortionModel(lang=self.lang, device=self._device)

        if output_dir is not None:
            self.temp_path = output_dir
        else:
            basename = os.path.splitext(os.path.basename(video_path))[0]
            self.temp_path = os.path.join("temp", basename)
        if not os.path.exists(self.temp_path):
            os.makedirs(self.temp_path)

        self.return_path = return_path

    @property
    def device(self) -> torch.device:
        """Check the device type.

        Returns:
            torch.device: Device type on local machine.
        """
        return self._device

    def get_distortion(self) -> Tuple[str, str]:
        phrases = get_phrases(self.words, duration=self.duration)
        data = pd.DataFrame(data=phrases)
        div_report = []

        for start_sec, finish_sec in self.stamps:
            for row in range(len(data)):
                if (
                    data["time_start"][row] > start_sec - 5
                    and data["time_end"][row] < finish_sec + 5
                ):
                    text = data["text"][row]
                    pred = self.dist_mod.predict(text)
                    dct = {
                        "time_sec": float(
                            data["time_start"][row] - data["time_start"][row] % 10
                        ),
                        "text": text,
                    }
                    for line in pred:
                        dct[line["label"]] = line["score"]
                    div_report.append(dct)

        div_report = pd.DataFrame(data=div_report)
        div_report = (
            div_report.drop_duplicates(subset=["time_sec"])
            .sort_values(by="time_sec")
            .reset_index(drop=True)
            .fillna(0)
        )
        agg_report = div_report.iloc[:, 2:].sum() / len(div_report)

        div_report_path = os.path.join(self.temp_path, "div_distortions.json")
        div_report.to_json(div_report_path, orient="records")
        agg_report_path = os.path.join(self.temp_path, "agg_distortions.json")
        agg_report = [agg_report.to_dict()]

        with open(agg_report_path, "w") as filename:
            json.dump(agg_report, filename)

        if self.return_path:
            return div_report_path, agg_report_path
        else:
            return {
                "distortions_divided": div_report.to_dict(orient="records"),
                "distortions_aggregated": agg_report,
            }
