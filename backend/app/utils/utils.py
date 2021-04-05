import dataclasses
import logging
import json
from typing import Dict, List

from tqdm import tqdm


def save_as_json(content: List[Dict], output_path: str) -> None:
    with open(output_path, "w") as output_file:
        print("Saving files")
        for line in tqdm(content):
            json.dump(dataclasses.asdict(line), output_file)
            output_file.write("\n")


def get_logger():
    logger = logging.getLogger(__name__)
    LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s (%(funcName)s@%(filename)s:%(lineno)s)"
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    return logger
