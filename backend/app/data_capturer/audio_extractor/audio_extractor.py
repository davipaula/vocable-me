import logging
import os

import ffmpeg

from data_capturer.audio_extractor.video_captions_selector import (
    select_video_captions,
)
from tqdm import tqdm

BUFFER_IN_SECONDS = 1

logger = logging.getLogger(__name__)
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s (%(funcName)s@%(filename)s:%(lineno)s)"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def run():
    video_captions = select_video_captions()
    split_audio_files(video_captions)

    print("Audio extractor is running")


def split_audio_files(video_captions):
    os.chdir("/app/app/data/raw/audio/")
    raw_audio_path = "./"
    output_path = "/app/app/data/processed/audio/"

    if video_captions is None:
        # TODO if no video captions are provided, extract sentences of all audios
        raise NotImplementedError

    # Extract audio of these words
    for caption in tqdm(video_captions):
        video_title = caption[0].split(".")[0]
        video_filename = video_title + ".mp3"

        if not os.path.isfile(video_filename):
            # Not every caption contains an audio file.
            logger.info(f"File {video_filename} does not exist!")

            continue

        start_caption_time = caption[1]["start"]
        end_caption_time = caption[1]["end"]

        output_name = _format_output_filename(
            video_filename, start_caption_time, end_caption_time
        )

        start_in_seconds = (
            _get_time_in_seconds(start_caption_time) - BUFFER_IN_SECONDS
        )
        end_in_seconds = (
            _get_time_in_seconds(end_caption_time) + BUFFER_IN_SECONDS
        )

        # "atrim" means "audio trim". This is needed because we're working with audio tracks only
        input_file = ffmpeg.input(raw_audio_path + video_filename).filter(
            "atrim", start=start_in_seconds, end=end_in_seconds
        )

        output, _ = (
            input_file.output(output_path + output_name)
            .overwrite_output()
            .run(quiet=True)
        )


def _format_output_filename(
    video_filename, start_caption_time, end_caption_time
):
    start = _format_time(start_caption_time)
    end = _format_time(end_caption_time)

    return f"{start}-{end}-{video_filename}"


def _format_time(time_str: str) -> str:
    return time_str.split(".")[0].replace(":", "_")


def _get_time_in_seconds(caption_timestamp: str) -> int:
    # The standard format is 'HH:MM:SS.MS'
    caption_timestamp_split = caption_timestamp.split(":")[:3]

    caption_hours_in_seconds = int(caption_timestamp_split[0]) * 60 * 60
    caption_minutes_in_seconds = int(caption_timestamp_split[1]) * 60
    caption_seconds = int(caption_timestamp_split[2].split(".")[0])

    return (
        caption_hours_in_seconds + caption_minutes_in_seconds + caption_seconds
    )


if __name__ == "__main__":
    run()
