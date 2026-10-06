import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "eval" / "gapbench"))

from leakage import leaks  # noqa: E402


def test_leak_patterns():
    assert leaks("we run train.py --normalize zscore", "normalize", "zscore", near=False)
    assert leaks("threshold: 0.3", "threshold", "0.3", near=False)
    assert leaks("inputs are normalized ... the normalize step uses zscore scaling", "normalize", "zscore", near=True)
    assert not leaks("a decision threshold equal to the positive rate", "threshold", "0.3", near=True)
    assert not leaks('choices=["none", "zscore", "minmax"]', "normalize", "zscore", near=False)
