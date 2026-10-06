"""Logistic regression with mini-batch SGD on a synthetic tabular dataset. Reports test metrics."""
import argparse
import json
import math
import os
import random


def parse():
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=1200)
    p.add_argument("--positive_rate", type=float, default=0.3)
    p.add_argument("--label_noise", type=float, default=0.05)
    p.add_argument("--split", type=float, default=0.8)
    p.add_argument("--normalize", choices=["none", "zscore", "minmax"], default="none")
    p.add_argument("--epochs", type=int, default=15)
    p.add_argument("--batch_size", type=int, default=32)
    p.add_argument("--lr", type=float, default=0.05)
    p.add_argument("--lr_schedule", choices=["const", "step", "cosine"], default="const")
    p.add_argument("--weight_decay", type=float, default=0.0)
    p.add_argument("--class_weight", choices=["none", "balanced"], default="none")
    p.add_argument("--threshold", type=float, default=0.5)
    p.add_argument("--data_seed", type=int, default=7)
    p.add_argument("--out", default="out/result.json")
    return p.parse_args()


SCALES = [1.0, 1.0, 50.0, 0.02, 400.0, 1.0, 5.0, 0.5]
WEIGHTS = [1.2, -0.8, 0.6, 0.9, -0.5, 0.0, 0.4, 0.0]


def make_data(a):
    rng = random.Random(a.data_seed)
    X, y = [], []
    for _ in range(a.n):
        z = [rng.gauss(0, 1) for _ in SCALES]
        logit = sum(w * v for w, v in zip(WEIGHTS, z)) + math.log(a.positive_rate / (1 - a.positive_rate))
        label = 1 if rng.random() < 1 / (1 + math.exp(-logit)) else 0
        if rng.random() < a.label_noise:
            label = 1 - label
        X.append([v * s for v, s in zip(z, SCALES)])
        y.append(label)
    k = int(a.split * a.n)
    return X[:k], y[:k], X[k:], y[k:]


def normaliser(Xtr, how):
    d = len(Xtr[0])
    if how == "zscore":
        mu = [sum(r[j] for r in Xtr) / len(Xtr) for j in range(d)]
        sd = [math.sqrt(sum((r[j] - mu[j]) ** 2 for r in Xtr) / len(Xtr)) or 1.0 for j in range(d)]
        return lambda r: [(r[j] - mu[j]) / sd[j] for j in range(d)]
    if how == "minmax":
        lo = [min(r[j] for r in Xtr) for j in range(d)]
        hi = [max(r[j] for r in Xtr) for j in range(d)]
        return lambda r: [(r[j] - lo[j]) / ((hi[j] - lo[j]) or 1.0) for j in range(d)]
    return lambda r: r


def sigmoid(t):
    t = max(min(t, 35.0), -35.0)
    return 1 / (1 + math.exp(-t))


def main():
    a = parse()
    tag = os.environ.get("RUN_TAG", "")
    rng = random.Random(int(tag[:6], 16) if tag else 0)  # shuffling and init differ per run
    Xtr, ytr, Xte, yte = make_data(a)
    f = normaliser(Xtr, a.normalize)
    Xtr, Xte = [f(r) for r in Xtr], [f(r) for r in Xte]
    d = len(Xtr[0])
    w, b = [rng.gauss(0, 0.01) for _ in range(d)], 0.0
    pos = sum(ytr) / len(ytr)
    cw = {1: 0.5 / pos, 0: 0.5 / (1 - pos)} if a.class_weight == "balanced" else {1: 1.0, 0: 1.0}
    idx = list(range(len(Xtr)))
    steps = a.epochs * math.ceil(len(idx) / a.batch_size)
    step = 0
    for ep in range(a.epochs):
        rng.shuffle(idx)
        for s0 in range(0, len(idx), a.batch_size):
            if a.lr_schedule == "step":
                lr = a.lr * (0.1 if ep >= a.epochs * 2 // 3 else 1.0)
            elif a.lr_schedule == "cosine":
                lr = a.lr * 0.5 * (1 + math.cos(math.pi * step / steps))
            else:
                lr = a.lr
            batch = idx[s0:s0 + a.batch_size]
            gw, gb = [0.0] * d, 0.0
            for i in batch:
                err = (sigmoid(sum(wj * xj for wj, xj in zip(w, Xtr[i])) + b) - ytr[i]) * cw[ytr[i]]
                for j in range(d):
                    gw[j] += err * Xtr[i][j]
                gb += err
            m = len(batch)
            w = [wj - lr * (gj / m + a.weight_decay * wj) for wj, gj in zip(w, gw)]
            b -= lr * gb / m
            step += 1
    pred = [1 if sigmoid(sum(wj * xj for wj, xj in zip(w, r)) + b) >= a.threshold else 0 for r in Xte]
    acc = sum(p == t for p, t in zip(pred, yte)) / len(yte)
    tp = sum(p == 1 and t == 1 for p, t in zip(pred, yte))
    tn = sum(p == 0 and t == 0 for p, t in zip(pred, yte))
    npos, nneg = sum(yte), len(yte) - sum(yte)
    bal = 0.5 * (tp / max(npos, 1) + tn / max(nneg, 1))
    res = {"test_accuracy": round(acc, 4), "balanced_accuracy": round(bal, 4)}
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w") as fh:
        fh.write(json.dumps(res) + "\n")
    print(json.dumps(res))


if __name__ == "__main__":
    main()
