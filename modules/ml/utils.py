import json
import logging
import random
import string
from collections import defaultdict
from typing import Any, Dict, List

from modules.ml.constants import META_MAPPING

logger = logging.getLogger(__name__)


def random_string(length: int = 10) -> str:
    """
    return a random string of lowercase letters and digits with a given length
    """
    return "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(length)]
    )


def meta_parser(meta_key: str, meta_dict: dict):
    meta_value = None
    for k in META_MAPPING[meta_key]:
        try:
            meta_value = meta_dict[k]
        except:
            pass
    if meta_value is None:
        raise ValueError
    return meta_value
