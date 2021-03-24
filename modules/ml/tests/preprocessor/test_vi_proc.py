import pytest
from qcore.asserts import assert_raises

from modules.ml.preprocessor.vi_preprocessor import ViPreProcessor


def test_basic_cleaning_1():
    """Conduct basic cleaning and compare result"""
    processor = ViPreProcessor()
    text = (
        "Cho đến thời điểm này, có thể nói, "
        + "Klopp là một trong những đối thủ lớn nhất của Mourinho."
    )

    expected = (
        "cho đến thời_điểm này, có_thể nói, "
        + "klopp là một trong những đối_thủ lớn nhất của mourinho."
    )

    out = processor.clean({"text": text})
    assert expected == out["text"]


def test_basic_cleaning_2():
    """Test if output of clean function is dict and contains key 'text'"""
    processor = ViPreProcessor()
    text = (
        "Cho đến thời điểm này, có thể nói, "
        + "Klopp là một trong những đối thủ lớn nhất của Mourinho."
    )

    out = processor.clean({"text": text})
    assert isinstance(out, dict) and "text" in out


@pytest.mark.parametrize("srsb", [True, False])
def test_not_implemented_splitby_in_split(srsb):
    """Test if code could raise exception for invalid args:
    'split_by' and 'split_respect_sentence_boundary'
    """
    processor = ViPreProcessor(
        split_by="dummy_string", split_respect_sentence_boundary=srsb
    )
    assert_raises(lambda: processor.split({"text": "dummy"}), NotImplementedError)


def test_invalid_split_length():
    """Test if code could raise exception for invalid args:
    'split_length'
    """
    processor = ViPreProcessor(split_length=None)
    assert_raises(lambda: processor.split({"text": "dummy"}), ValueError)
