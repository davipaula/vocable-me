import json
import logging
from typing import Dict, List

from data_capturer.text_processor.text_processor import TextProcessor
from model.settings import CAPTION_DATASET_PATH

logger = logging.getLogger(__name__)
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s (%(funcName)s@%(filename)s:%(lineno)s)"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def get_captions_text(captions: List[Dict[str, List]]) -> List[str]:
    normalized_dataset = []
    text_processor = TextProcessor()

    logger.info("Getting captions")
    for index, caption in enumerate(captions):
        normalized_captions = [
            sentence["text"] for sentence in caption["captions"]
        ]

        normalized_dataset.append(" ".join(normalized_captions))

    logger.info("Cleaning captions")

    # Ideally we should store the captions with the text clean.
    # However, as the steps needed to are not clear yet, I decided to perform the cleaning here.
    # It has a big negative impact in the performance
    return text_processor.clean_texts(normalized_dataset)


def get_captions_as_json() -> List[Dict]:
    with open(CAPTION_DATASET_PATH, "r") as json_file:
        json_list = list(json_file)

    return [json.loads(json_str) for json_str in json_list]
