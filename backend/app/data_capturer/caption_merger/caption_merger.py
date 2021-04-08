from typing import List

import spacy


def merge_captions(sentences: List[str]):
    nlp = spacy.load("en_core_web_sm")

    final_sentences = []
    merged_sentence = []

    for index, sentence in enumerate(sentences):
        doc = nlp(sentence)

        for sent in doc.sents:
            if sent[-1].is_punct or index == len(sentences) - 1:
                merged_sentence.append(sent.text)
                final_sentences.append(" ".join(merged_sentence))

                merged_sentence = []
                continue

            merged_sentence.append(sent.text)

    print(final_sentences)


if __name__ == "__main__":
    sentences = [
        "This is a text with a punctuation.",
        "This is a text without punctuation",
        "and this is the continuation of the text",
        "and this is the final part.",
        "This is the final U.K. sentence, without punctuation",
    ]

    merge_captions(sentences)
