# Harness-side seed variation for blind-1 (see ../HARNESS.md). Installed into the image's site-packages
# with gf_seed.pth; it is not part of the artifact and no repo file is edited.
#
# FastGCN's entry scripts fix `seed = 123` and call np.random.seed(seed) and tf.set_random_seed(seed), so
# every repeat of a configuration would be bit-identical and the noise band would be zero. When
# GF_SEED_FROM_RUN_TAG=1 and RUN_TAG is set (GapFinder gives every run a fresh RUN_TAG), both calls get
# seed + crc32(RUN_TAG) % 100000 instead, so repeats differ the way reruns with other seeds do. With
# either variable unset nothing is changed. The effective seed is printed to stderr.
import os
import sys
import zlib

_tag = os.environ.get("RUN_TAG")
if _tag and os.environ.get("GF_SEED_FROM_RUN_TAG") == "1":
    _off = zlib.crc32(_tag.encode()) % 100000

    def _shift(s):
        return None if s is None else (int(s) + _off) % (2 ** 31)

    import numpy as _np

    _np_seed = _np.random.seed

    def _seed(s=None):
        sys.stderr.write("gf_seed: numpy seed %s -> %s\n" % (s, _shift(s)))
        return _np_seed(_shift(s))

    _np.random.seed = _seed

    import tensorflow as _tf

    _tf_seed = _tf.compat.v1.set_random_seed

    def _tf_set(s):
        sys.stderr.write("gf_seed: tf seed %s -> %s\n" % (s, _shift(s)))
        return _tf_seed(_shift(s))

    _tf.set_random_seed = _tf_set
    _tf.compat.v1.set_random_seed = _tf_set
