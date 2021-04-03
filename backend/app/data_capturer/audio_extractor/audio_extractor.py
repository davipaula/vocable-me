import json
import logging
import os
from typing import Dict, List, Set

import ffmpeg

from app.data_capturer.audio_extractor.video_captions_selector import (
    select_video_captions,
)
from tqdm import tqdm

from app.db.video_caption import VideoCaption

HOURS_IN_SECONDS = 360
MINUTES_IN_SECONDS = 60

BUFFER_IN_SECONDS = 1

OUTPUT_PATH = "/app/app/data/processed/audio/"

logger = logging.getLogger(__name__)
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s (%(funcName)s@%(filename)s:%(lineno)s)"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def run():
    logger.info("Retrieving data from DB")
    video_captions = select_video_captions()
    logger.info(
        f"""Data retrieved from DB. \n
    Videos to process: {len(video_captions)} \n
     Starting audio extraction"""
    )

    split_audio_files(video_captions)


def split_audio_files(video_captions: List[VideoCaption]):
    os.chdir("/app/app/data/raw/audio/")
    raw_audio_path = "./"

    if video_captions is None:
        # TODO if no video captions are provided, extract sentences of all audios
        raise NotImplementedError

    # Extract audio of these words
    output_files = []
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

        try:
            # "atrim" means "audio trim". This is needed because we're working with audio tracks only
            input_file = ffmpeg.input(
                raw_audio_path + original_filename
            ).filter("atrim", start=start_in_seconds, end=end_in_seconds)

            output, _ = (
                input_file.output(OUTPUT_PATH + caption.get_output_filename())
                .overwrite_output()
                .run(quiet=True)
            )
        except ffmpeg.Error as e:
            logger.error(
                f"Error processing file {original_filename}. \n"
                f"Error: {e.stderr}"
                f"Error output: {e.stdout}"
            )

            continue

        output_files.append(
            {
                "video_id": caption.video_id,
                "start_time": caption.start_time,
                "end_time": caption.end_time,
                "filename": caption.get_output_filename(),
            }
        )

    _save_available_audio_files(output_files)


def _save_available_audio_files(output_files: List[Dict]):
    """
    This is a temporary solution ("gambiarra" in Brazilian Portuguese). Not all captions have audios, so we are saving
    the title of the audios in a file. This will be used to filter the response we're
    sending to the front-end.

    Now that all the steps to provide the data to the front-end are clear, we should create a pipeline for our data,
    so we execute sequentially the steps needed to provide the data and save the final results in an appropriate place
    (probably DB). This will be the source of truth for the data we will provide to the front-end.
    """
    # TODO save this info into a DB table
    with open(os.path.join(OUTPUT_PATH, "available_audios.jsonl"), "w+") as f:
        print("Saving files")
        for line in tqdm(output_files):
            json.dump(line, f)
            f.write("\n")


def get_available_audio_files() -> List[Dict]:
    with open(
        os.path.join(OUTPUT_PATH, "available_audios.jsonl"), "r"
    ) as json_file:
        json_list = list(json_file)

    return [json.loads(json_str) for json_str in json_list]


def get_processed_video_ids() -> List[str]:
    audio_files = get_available_audio_files()

    return [f"'{audio_file['video_id']}'" for audio_file in audio_files]


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


def rewrite_output_files():
    available_audio_files = []
    for file in os.listdir(OUTPUT_PATH):
        if file.endswith(".mp3"):
            file_name_parts = file.split("-")
            start_time = file_name_parts[0].replace("_", ":")
            end_time = file_name_parts[1].replace("_", ":")
            video_id = file_name_parts[2].split(".")[0] + ".en.vtt"

            available_audio_files.append(
                {
                    "video_id": video_id,
                    "start_time": start_time,
                    "end_time": end_time,
                    "filename": file,
                }
            )

    _save_available_audio_files(available_audio_files)


if __name__ == "__main__":
    run()
