import logging
import os
from typing import List

import ffmpeg

from data_capturer.audio_extractor.video_captions_selector import (
    select_video_captions,
)
from tqdm import tqdm

from db.video_caption import VideoCaption

HOURS_IN_SECONDS = 360
MINUTES_IN_SECONDS = 60

BUFFER_IN_SECONDS = 1

logger = logging.getLogger(__name__)
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s (%(funcName)s@%(filename)s:%(lineno)s)"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def run():
    video_captions = select_video_captions()
    split_audio_files(video_captions)

    print("Audio extractor is running")


def split_audio_files(video_captions: List[VideoCaption]):
    os.chdir("/app/app/data/raw/audio/")
    raw_audio_path = "./"
    output_path = "/app/app/data/processed/audio/"

    if video_captions is None:
        # TODO if no video captions are provided, extract sentences of all audios
        raise NotImplementedError

    # Extract audio of these words
    for caption in tqdm(video_captions):
        original_filename = caption.get_original_filename()
        if not os.path.isfile(original_filename):
            # Not every text contains an audio file.
            logger.info(f"File {original_filename} does not exist!")
            continue

        start_in_seconds = (
            _get_time_in_seconds(caption.start_time) - BUFFER_IN_SECONDS
        )
        end_in_seconds = (
            _get_time_in_seconds(caption.end_time) + BUFFER_IN_SECONDS
        )

        # "atrim" means "audio trim". This is needed because we're working with audio tracks only
        input_file = ffmpeg.input(raw_audio_path + original_filename).filter(
            "atrim", start=start_in_seconds, end=end_in_seconds
        )

        output, _ = (
            input_file.output(output_path + caption.get_output_filename())
            .overwrite_output()
            .run(quiet=True)
        )


def _get_time_in_seconds(caption_timestamp: str) -> int:
    # The standard format is 'HH:MM:SS.MS'
    caption_timestamp_split = caption_timestamp.split(":")

    caption_hours_in_seconds = (
        int(caption_timestamp_split[0]) * HOURS_IN_SECONDS
    )
    caption_minutes_in_seconds = (
        int(caption_timestamp_split[1]) * MINUTES_IN_SECONDS
    )
    caption_seconds = int(caption_timestamp_split[2].split(".")[0])

    return (
        caption_hours_in_seconds + caption_minutes_in_seconds + caption_seconds
    )


if __name__ == "__main__":
    run()
