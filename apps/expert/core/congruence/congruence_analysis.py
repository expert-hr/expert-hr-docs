from __future__ import annotations

import json
import os
from os import PathLike

import pandas as pd
import torch

from apps.expert.data.video_reader import VideoReader
from apps.expert.core.congruence.audio_emotions.audio_analysis import AudioAnalysis
from apps.expert.core.congruence.text_emotions.text_analysis import get_text_emotions
from apps.expert.core.congruence.video_emotions.video_analysis import (
    get_video_emotions,
)


def align_timestamps(time_sec):
    return time_sec - time_sec % 10


class CongruenceDetector:
    """Determination of expert emotions congruence.

    Args:
        video_path (str | PathLike): Path to local video file.
        features_path (str | PathLike): Path to JSON file with information about detected faces.
        transcription_path (str | PathLike): Path to JSON file with text transcription.
        diarization_path (str | PathLike): Path to JSON file with diarization information.
        lang (str, optional): Speech language for text processing ['ru', 'en']. Defaults to 'en'.
        duration (int, optional): Length of intervals for extracting features. Defaults to 10.
        sr (int, optional): Sample rate. Defaults to 16000.
        device (torch.device | None, optional): Device type on local machine (GPU recommended). Defaults to None.
        output_dir (str | Pathlike | None, optional): Path to the folder for saving results. Defaults to None.
        return_path (bool): Flag to define the return mode for get_congruence. True is for path, False is for dict. Defaults to False

    Returns:
        Tuple[str, str]: Paths to the emotion and congruence reports.

    Raises:
        NotImplementedError: If 'lang' is not equal to 'en' or 'ru'.

    Example:
        >>> import torch
        >>> cong_detector = CongruenceDetector(
                video_path="test_video.mp4",
                features_path="temp/test_video/features.json",
                transcription_path="temp/test_video/transcription.json",
                diarization_path="temp/test_video/diarization.json",
                device=torch.device("cuda:0"),
            )
        >>> cong_detector.get_congruence()
    """

    def __init__(
        self,
        video_path: str | PathLike,
        features_path: str | PathLike,
        transcription_path: str | PathLike,
        diarization_path: str | PathLike,
        lang: str = "en",
        duration: int = 10,
        sr: int = 44100,
        device: torch.device | None = None,
        output_dir: str | PathLike | None = None,
        return_path: bool = False,
    ):
        if lang not in ["en", "ru"]:
            raise NotImplementedError("'lang' must be 'en' or 'ru'.")

        self.lang = lang
        self.video_path = video_path
        self.features_path = features_path
        self.transcription_path = transcription_path
        self.duration = duration
        self.sr = sr

        video = VideoReader(self.video_path)
        self.video_length = int(video.frame_cnt / video.fps)
        self._device = torch.device("cpu")
        if device is not None:
            self._device = device

        with open(diarization_path, "r") as file:
            self.stamps = json.load(file)

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

    def get_video_state(self):
        video_data = get_video_emotions(
            video_path=self.video_path,
            features_path=self.features_path,
            device=self._device,
            video_length=self.video_length,
            duration=self.duration,
        )
        video_data = pd.DataFrame(data=video_data)
        video_data["time_sec"] = video_data["time_sec"].apply(align_timestamps)

        video_data = (
            video_data.drop_duplicates(subset=["time_sec"])
            .sort_values(by="time_sec")
            .reset_index(drop=True)
            .fillna(0)
        )

        return video_data

    def get_audio_state(self):
        audio_model = AudioAnalysis(
            video_path=self.video_path,
            stamps=self.stamps,
            sr=self.sr,
            duration=self.duration,
            device=self._device,
        )

        audio_data = audio_model.predict()
        audio_data = pd.DataFrame(data=audio_data)
        audio_data["time_sec"] = audio_data["time_sec"].apply(align_timestamps)

        audio_data = (
            audio_data.drop_duplicates(subset=["time_sec"])
            .sort_values(by="time_sec")
            .reset_index(drop=True)
            .fillna(0)
        )

        return audio_data

    def get_text_state(self):
        text_data = get_text_emotions(
            words_path=self.transcription_path,
            video_length=self.video_length,
            device=self._device,
            duration=self.duration,
        )
        text_data = pd.DataFrame(data=text_data)
        text_data["time_sec"] = text_data["time_sec"].apply(align_timestamps)

        text_data = (
            text_data.drop_duplicates(subset=["time_sec"])
            .sort_values(by="time_sec")
            .reset_index(drop=True)
            .fillna(0)
        )

        return text_data

    def get_congruence(self):
        video_data = self.get_video_state()
        audio_data = self.get_audio_state()
        text_data = self.get_text_state()

        cong_data = video_data.join(
            audio_data.set_index("time_sec"), how="inner", on="time_sec"
        )
        cong_data = cong_data.join(
            text_data.set_index("time_sec"), how="inner", on="time_sec"
        )
        cong_data = cong_data.sort_values(by="time_sec").reset_index(drop=True)

        neutral_std = cong_data.loc[
            :, ["video_neutral", "audio_neutral", "text_neutral"]
        ].std(axis=1)
        anger_std = cong_data.loc[:, ["video_anger", "audio_anger", "text_anger"]].std(
            axis=1
        )
        happiness_std = cong_data.loc[
            :, ["video_happiness", "audio_happiness", "text_happiness"]
        ].std(axis=1)
        # Calculate the sum of deviations between emotions and normalize the value.
        cong_data["congruence"] = (neutral_std + anger_std + happiness_std) / 1.5

        # Get and save data with all emotions.
        emotions_data = dict()
        emotions_data["video"] = video_data.to_dict(orient="records")
        emotions_data["audio"] = audio_data.to_dict(orient="records")
        emotions_data["text"] = text_data.to_dict(orient="records")

        with open(os.path.join(self.temp_path, "emotions.json"), "w") as filename:
            json.dump(emotions_data, filename)

        cong_data[["video_path", "time_sec", "congruence"]].to_json(
            os.path.join(self.temp_path, "congruence.json"),
            orient="records",
        )

        if self.return_path:
            return os.path.join(self.temp_path, "emotions.json"), os.path.join(
                self.temp_path, "congruence.json"
            )
        else:
            return {
                "emotions": emotions_data,
                "congruence": cong_data[
                    ["video_path", "time_sec", "congruence"]
                ].to_dict(orient="records"),
            }
