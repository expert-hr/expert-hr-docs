from __future__ import annotations

import json
from os import PathLike
from typing import Dict, List

import pandas as pd
import torch
from torch import nn

from apps.expert.core.congruence.text_emotions.text_model import TextModel
from apps.expert.data.annotation.speech_to_text import between_timestamps


def get_text_emotions(
    words_path: str,
    video_length: int,
    device: torch.device | None = None,
    duration: int = 10,
) -> List:
    """Classification of expert emotions in text.

    Args:
        words_path (str): Path to JSON file with text transcription.
        device (torch.device | None, optional): Device type on local machine (GPU recommended). Defaults to None.
        duration: Length of intervals for extracting features. Defaults to 10.
    """
    softmax = nn.Softmax(dim=1)
    emo_model = TextModel(device=device)
    with open(words_path, "r") as file:
        words = json.load(file)
    data = pd.DataFrame()

    for row in range(0, video_length, duration):
        phrase = between_timestamps(words, row, row + duration)
        data.loc[row, "time_sec"] = row
        if phrase:
            emotion_dict = emo_model.predict(phrase)
            lim_emotions = softmax(
                torch.Tensor(
                    [
                        [
                            emotion_dict["anger"],
                            emotion_dict["neutral"],
                            emotion_dict["happiness"],
                        ]
                    ]
                )
            )[0].numpy()
            data.loc[row, "text"] = phrase
            data.loc[row, "text_anger"] = float(lim_emotions[0])
            data.loc[row, "text_neutral"] = float(lim_emotions[1])
            data.loc[row, "text_happiness"] = float(lim_emotions[2])
        else:
            data.loc[row, "text"] = phrase
            data.loc[row, "text_anger"] = 0.0
            data.loc[row, "text_neutral"] = 1.0
            data.loc[row, "text_happiness"] = 0.0

    return data.to_dict("records")
