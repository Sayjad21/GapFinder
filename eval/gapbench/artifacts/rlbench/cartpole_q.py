"""Tabular Q-learning on a discretised CartPole. Reports greedy evaluation reward."""
import argparse
import json
import math
import os
import random


def parse():
    p = argparse.ArgumentParser()
    p.add_argument("--episodes", type=int, default=400)
    p.add_argument("--gamma", type=float, default=0.99)
    p.add_argument("--lr", type=float, default=0.1)
    p.add_argument("--lr_schedule", choices=["const", "linear", "inv"], default="const")
    p.add_argument("--eps_start", type=float, default=1.0)
    p.add_argument("--eps_end", type=float, default=0.05)
    p.add_argument("--eps_decay", type=float, default=0.99)
    p.add_argument("--theta_bins", type=int, default=6)
    p.add_argument("--omega_bins", type=int, default=6)
    p.add_argument("--reward_norm", choices=["off", "on"], default="off")
    p.add_argument("--max_steps", type=int, default=200)
    p.add_argument("--init_q", type=float, default=0.0)
    p.add_argument("--seeds", type=int, default=10)
    p.add_argument("--eval_episodes", type=int, default=20)
    p.add_argument("--out", default="out/result.json")
    return p.parse_args()


class CartPole:
    g, mc, mp, l, f, dt = 9.8, 1.0, 0.1, 0.5, 10.0, 0.02

    def __init__(self, rng):
        self.rng = rng

    def reset(self):
        self.s = [self.rng.uniform(-0.05, 0.05) for _ in range(4)]
        return self.s

    def step(self, a):
        x, xd, th, thd = self.s
        force = self.f if a == 1 else -self.f
        ct, st = math.cos(th), math.sin(th)
        tm = self.mc + self.mp
        tmp = (force + self.mp * self.l * thd * thd * st) / tm
        tha = (self.g * st - ct * tmp) / (self.l * (4.0 / 3.0 - self.mp * ct * ct / tm))
        xa = tmp - self.mp * self.l * tha * ct / tm
        x, xd = x + self.dt * xd, xd + self.dt * xa
        th, thd = th + self.dt * thd, thd + self.dt * tha
        self.s = [x, xd, th, thd]
        done = abs(x) > 2.4 or abs(th) > 12 * math.pi / 180
        return self.s, 1.0, done


def discretise(s, tb, ob):
    th = min(max(s[2], -0.21), 0.21)
    om = min(max(s[3], -2.0), 2.0)
    return (min(int((th + 0.21) / 0.42 * tb), tb - 1), min(int((om + 2.0) / 4.0 * ob), ob - 1))


def run_seed(a, seed):
    rng = random.Random(seed)
    env = CartPole(rng)
    q = {}
    eps = a.eps_start
    scale = 1.0 / a.max_steps if a.reward_norm == "on" else 1.0
    for ep in range(a.episodes):
        if a.lr_schedule == "linear":
            lr = a.lr * (1 - ep / a.episodes) + 1e-3
        elif a.lr_schedule == "inv":
            lr = a.lr / (1 + ep / 50)
        else:
            lr = a.lr
        s = discretise(env.reset(), a.theta_bins, a.omega_bins)
        for _ in range(a.max_steps):
            qs = q.setdefault(s, [a.init_q, a.init_q])
            act = rng.randrange(2) if rng.random() < eps else (0 if qs[0] >= qs[1] else 1)
            obs, r, done = env.step(act)
            s2 = discretise(obs, a.theta_bins, a.omega_bins)
            q2 = q.setdefault(s2, [a.init_q, a.init_q])
            target = r * scale + (0.0 if done else a.gamma * max(q2))
            qs[act] += lr * (target - qs[act])
            s = s2
            if done:
                break
        eps = max(a.eps_end, eps * a.eps_decay)
    total = 0.0
    for _ in range(a.eval_episodes):
        s = discretise(env.reset(), a.theta_bins, a.omega_bins)
        for t in range(a.max_steps):
            qs = q.get(s, [0.0, 0.0])
            obs, r, done = env.step(0 if qs[0] >= qs[1] else 1)
            total += r
            s = discretise(obs, a.theta_bins, a.omega_bins)
            if done:
                break
    return total / a.eval_episodes


def main():
    a = parse()
    # seeds differ per run unless pinned, as across real reruns
    tag = os.environ.get("RUN_TAG", "")
    base = int(os.environ.get("RL_SEED_BASE", int(tag[:6], 16) if tag else 0))
    rewards = [run_seed(a, base + i) for i in range(a.seeds)]
    mean = sum(rewards) / len(rewards)
    res = {"mean_reward": round(mean, 3), "min_reward": round(min(rewards), 3), "max_reward": round(max(rewards), 3)}
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w") as f:
        f.write(json.dumps(res) + "\n")
    print(json.dumps(res))


if __name__ == "__main__":
    main()
