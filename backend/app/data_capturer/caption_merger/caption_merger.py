from typing import Dict, List

import spacy

FINAL_PUNCTUATION = [".", "!", "?"]

nlp = spacy.load("en_core_web_sm")


def merge_captions(captions: List[Dict]):

    tokenized_captions = [nlp(caption["text"]) for caption in captions]

    merged_fragments = []
    sentence_fragments = []
    current_start_timestamp = None
    for index, tokenized_caption in enumerate(tokenized_captions):
        sentence_fragments.append(tokenized_caption.text)

        if current_start_timestamp is None:
            current_start_timestamp = captions[index]["start"]

        if (
            tokenized_caption[-1].text in FINAL_PUNCTUATION
            or index == len(tokenized_captions) - 1
        ):
            merged_fragments.append(
                {
                    "start": current_start_timestamp,
                    "end": captions[index]["end"],
                    "text": " ".join(sentence_fragments),
                }
            )

            sentence_fragments = []
            current_start_timestamp = None

    return merged_fragments
