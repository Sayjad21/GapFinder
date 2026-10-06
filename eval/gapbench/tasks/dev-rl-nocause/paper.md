# Stable Tabular Control on CartPole

## Abstract
We show that a small tabular Q-learner is stable across seeds on CartPole:
its worst seed still balances for 69.1 steps on average.

## Experimental setup
Classic CartPole, episodes capped at 200 steps. Six pole-angle and six
angular-velocity bins. Epsilon-greedy Q-learning with discount 0.99, constant
learning rate 0.1, epsilon from 1.0 decaying by 0.99 per episode to 0.05,
zero-initialised Q-values, unnormalised rewards. 400 training episodes; greedy
evaluation over 20 episodes; 10 seeds.

## Results
Figure 1: mean reward 118.9; worst seed 69.1.
