"""Plan D1.6: data-pipeline mutants (gapfinder/search/mutation.py), on a new toy pipeline."""

import textwrap

from gapfinder.search.mutation import find_mutants

DATA = textwrap.dedent('''\
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from torch.utils.data import DataLoader
    def load(min_count=5, val_ratio=0.1):
        X = list(range(100))
        X_train, X_test = train_test_split(X, test_size=0.2, random_state=0)
        n_val = int(0.15 * len(X_train))
        users = [u for u in X if u > 7]
        return X, X_train, X_test, users
    def run(X, X_train, X_test):
        scaler = StandardScaler().fit(X)
        enc = StandardScaler().fit(X_train[idx])
        test_loader = DataLoader(X_test, batch_size=64)
        train_loader = DataLoader(X_train, batch_size=64, shuffle=True)
        return scaler, test_loader
    def filter_users(df):
        return df[df.n_inter >= 10]
    ''')


def _muts(tmp_path, hints=None):
    (tmp_path / "data.py").write_text(DATA, encoding="utf-8")
    return find_mutants(tmp_path, [], files=[tmp_path / "data.py"], limit=200, hints=hints)


def test_data_pipeline_mutants(tmp_path):
    ms = _muts(tmp_path)
    got = {(m.line, m.after) for m in ms if "data pipeline" in m.tags}
    assert (6, "0.8") in got and (6, "0.25") in got  # test_size: the complement first, then the common fractions
    assert (7, "0.85") in got  # 0.15 * len(X_train)
    assert (4, "0.9") in got and (4, "6") in got and (4, "10") in got  # parameter defaults: val_ratio, min_count
    assert (11, "StandardScaler().fit(X_train)") in got  # fit on everything -> on the train split
    assert (12, "StandardScaler().fit(X_train)") in got  # fit on the train rows -> on the whole array
    assert (13, "DataLoader(X_test, batch_size=64, drop_last=True)") in got
    assert not any(m.line == 13 and "shuffle" in m.after for m in ms)  # an evaluation loader isn't shuffled
    assert (14, "DataLoader(X_train, batch_size=64, shuffle=True, drop_last=True)") in got
    assert (8, "8") in got and (8, "u >= 7") in got and (8, "3.5") not in got  # odd counts are never halved
    assert (17, "5") in got and (17, "df.n_inter > 10") in got
    assert not any("StandardScaler().fit(X)) /" in m.after for m in ms)  # a scaler is not a number


def test_a_flagged_line_comes_first(tmp_path):
    first = _muts(tmp_path, hints={"data.py": {17}})[0]
    assert first.line == 17 and "filter threshold" in first.tags
