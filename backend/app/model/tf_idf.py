import logging
import os
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer

# Bad hack to access the files
# TODO fix it
from model.settings import TF_IDF_MODEL_PATH
from model.utils import get_captions_as_json, get_captions_text

os.chdir(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s (%(funcName)s@%(filename)s:%(lineno)s)"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def train() -> None:
    captions = get_captions_as_json()

    # TODO preprocess text: noise removal, stop-word removal, lemmatization
    captions_text = get_captions_text(captions)

    logger.info("Training model over corpus")
    tf_idf_vectors = TfidfVectorizer(
        analyzer="word", min_df=0, max_df=0.8, stop_words="english"
    )
    tf_idf_model = tf_idf_vectors.fit(captions_text)

    logger.info("Training finished. Saving model")
    pickle.dump(tf_idf_model, open(TF_IDF_MODEL_PATH, "wb"))

    logger.info("Model saved successfully")


if __name__ == "__main__":
    train()
