import pytest

from gapfinder.search.evidence import EvidenceSearch, supporting_sentence


def test_supporting_sentence_needs_value_and_knob():
    text = ("We ran all experiments with a compaction rate limit of 30 MB/s. Throughput was stable. "
            "The value 30 appears elsewhere too.")
    assert "rate limit of 30" in supporting_sentence(text, "rate_limit_mb", "30")
    assert supporting_sentence("Throughput was 30 kops.", "rate_limit_mb", "30") is None  # value, no knob
    assert supporting_sentence("The rate limit was high.", "rate_limit_mb", "30") is None  # knob, no value
    assert supporting_sentence("limit 300 MB", "rate_limit_mb", "30") is None  # 30 inside 300 doesn't count


async def test_find_caches_and_grounds(tmp_path):
    calls = []

    async def fake(payload):
        calls.append(payload)
        return {"results": [{"url": "https://github.com/x/y/issues/7", "title": "t",
                             "content": "Note: the paper's runs used --rate_limit_mb 30 on all nodes."}]}

    es = EvidenceSearch("RusKey RocksDB", anchors=["github.com/x/y"], transport=fake, cache_dir=tmp_path)
    ev = await es.find("rate_limit_mb", "30")
    assert ev.kind == "web" and ev.ref.endswith("/issues/7") and "rate_limit_mb 30" in ev.quote
    await es.find("rate_limit_mb", "30")
    assert len(calls) == 1 and es.queries == 1  # second lookup served from the cache


async def test_disabled_without_key(tmp_path, monkeypatch):
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    es = EvidenceSearch("x", api_key=None, cache_dir=tmp_path)
    assert not es.enabled and await es.find("k", "1") is None


def test_regression_generic_value_and_short_words_do_not_match():
    """Live Tavily result that was wrongly accepted as evidence for direct_io=true."""
    blog = 'db = rocksdb.DB("path/to/db", rocksdb.Options(create_if_missing=True)) =."path/to/db".'
    assert supporting_sentence(blog, "direct_io", "true") is None
    assert supporting_sentence("We set direct_io=true for all runs.", "direct_io", "true")
    assert supporting_sentence("All runs enable direct io = true.", "direct_io", "true")


async def test_anchor_required(tmp_path):
    async def fake(payload):
        return {"results": [{"url": "https://blog.example/rocksdb", "title": "RocksDB tuning",
                             "content": "We used a rate limit of 30 MB/s via rate_limit_mb 30."}]}

    es = EvidenceSearch("RusKey", anchors=["ruskey"], transport=fake, cache_dir=tmp_path)
    assert await es.find("rate_limit_mb", "30") is None  # true sentence, but not about RusKey


def test_value_at_sentence_end_and_decimal_prefix():
    from gapfinder.ledger.schemas import Assumption
    from gapfinder.search.verify import plausible

    a = Assumption(id="A1", knob="lr", layer="config", paper_value="unstated", prior_score=0.5,
                   evidence=[{"kind": "paper", "ref": "p.2", "quote": "The learning rate lr is 0.05."}])
    assert plausible(a, "0.05").supported  # value at the end of a sentence
    assert not plausible(a, "0.0").supported  # a prefix of 0.05 is not the value


def test_choices_list_is_not_evidence_of_use():
    from gapfinder.ledger.schemas import Assumption
    from gapfinder.search.verify import plausible

    q = 'p.add_argument("--normalize", choices=["none", "zscore", "minmax"], default="none")'
    a = Assumption(id="A1", knob="normalize", layer="config", paper_value="unstated", prior_score=0.5,
                   evidence=[{"kind": "code", "ref": "train.py:15", "quote": q}])
    assert not plausible(a, "zscore").supported
    from gapfinder.ledger.schemas import Evidence

    b = a.model_copy(update={"evidence": [Evidence(kind="code", ref="run.sh:3", quote="python train.py --normalize zscore")]})
    assert plausible(b, "zscore").supported
