import numpy as np
import os
from glob import glob
from tqdm.notebook import tqdm
from random import choice, choices, shuffle
from unicodedata import normalize as unicode_normalize
from scipy.optimize import linear_sum_assignment
import re
from .._config import TF_IDF, SENTENCE__SCORE_THRESH
import pickle
from ..log import get_logger

logger = get_logger(__name__)


_chars_vn = [
    'á', 'à', 'ả', 'ã', 'ạ', 'â', 'ấ', 'ầ', 'ẩ', 'ẫ', 'ậ', 'ă', 'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ',
    'ó', 'ò', 'ỏ', 'õ', 'ọ', 'ô', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ', 'ơ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ',
    'é', 'è', 'ẻ', 'ẽ', 'ẹ', 'ê', 'ế', 'ề', 'ể', 'ễ', 'ệ',
    'ú', 'ù', 'ủ', 'ũ', 'ụ', 'ư', 'ứ', 'ừ', 'ử', 'ữ', 'ự',
    'í', 'ì', 'ỉ', 'ĩ', 'ị',
    'ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ', 'đ',
]

tf_model = pickle.load(
    open(TF_IDF, "rb")
)
chars_vn = "".join(_chars_vn)
chars_vn = chars_vn + chars_vn.upper()
# regex pattern of valid character
pattern_chars_vn = f"[a-zA-Z{chars_vn} ]"
# regex pattern of invalid character
pattern_unchars_vn = f"[^a-zA-Z{chars_vn} ]"


def normalize_text(text, split=False):
    text = text.replace("<br>", "")
    text = unicode_normalize("NFC", text)
    text = text.lower()
    text = re.sub("```(.|\n|\r)*?```", "", text)
    text = re.sub("\s+", " ", text)
    text = re.sub("[-_:/]", " ", text)

    text = re.sub(r'http\S+', '', text)
    text = re.sub("\.+", ".", text)
    text = re.sub("[?!;…]", ".", text)
    text = text.replace("\n", ".")
    sents = text.split(".")
    sents = [re.sub(pattern_unchars_vn, '', sent.strip()) for sent in sents]
    norm_sents = [s for s in sents if s]

    if split is False:
        return ". ".join(norm_sents)
    return norm_sents


def get_sentence_similarity(s1, s2):
    """
        Use Jaccard similarity metric
    """
    w1 = s1.split()
    w2 = s2.split()
    intersect_w = [w for w in w1 if w in w2]
    union_len = len(w1) + len(w2) - len(intersect_w)
    if union_len <= 0:
        return 0
    score = len(intersect_w)/(union_len)
    score = 0 if score < 0 else score
    return score


def doc2vec(text):
    """
        Use pretrained TF-IDF model
    """
    try:
        text = normalize_text(text, split=False)
        return tf_model.transform([text])
    except Exception as e:
        logger.error(e)
        return None


def compute_doc_similarity(doc1, doc2, threshold=SENTENCE__SCORE_THRESH):
    """
    Compute similarity 2 document
    Solution: 
        split 2 document to 2 sentence list.
        Compute jaccard_score every pair of sentences between two document.
        Get the most similar sentence pairs with Hungarian algorithm
        Count valid_sentence_pairs
    """
    if not isinstance(doc1, str) or not isinstance(doc2, str):
        return 0
    sentences1 = normalize_text(doc1, split=True)
    sentences2 = normalize_text(doc2, split=True)
    w, h = len(sentences1), len(sentences2)

    # similarity_matrix[i,j] - similarity score of sentences_1[i] vs sentences_2[j]
    sim_matrix = np.zeros((h, w))
    for i, s1 in enumerate(sentences1):
        for j, s2 in enumerate(sentences2):
            sim_matrix[j, i] = get_sentence_similarity(s1, s2)

    # Hungarian algorithm
    matched_data = []
    row_ind, col_ind = linear_sum_assignment(sim_matrix, maximize=True)
    for r, c in zip(row_ind, col_ind):
        matched_data.append({
            'score': sim_matrix[r, c],
            's1': sentences1[c],
            's2': sentences2[r]
        })
    score_list = [e['score'] for e in matched_data]
    valid_score = list(filter(lambda x: x > threshold, score_list))
    summary_score = len(valid_score)/(max(w, h))
    return summary_score