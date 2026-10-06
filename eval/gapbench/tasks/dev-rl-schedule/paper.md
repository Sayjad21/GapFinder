# Tabular Q-Learning on CartPole Needs Only Twelve Bins

## Abstract
A tabular Q-learner over six pole-angle and six angular-velocity bins balances
CartPole for a mean of 139.3 steps after 400 training episodes.

## Experimental setup
We use the classic CartPole dynamics with episodes capped at 200 steps. States
are discretised into 6 pole-angle bins and 6 angular-velocity bins. The agent
is epsilon-greedy Q-learning with discount 0.99; epsilon starts at 1.0 and
decays by a factor of 0.99 per episode to a floor of 0.05. The learning rate
starts at 0.1 and decays as 0.1 / (1 + t/50) with training episode t. Q-values
are initialised to zero and rewards are used unnormalised. We train for 400
episodes and evaluate the greedy policy for 20 episodes, averaging over 10
random seeds.

## Results
Figure 2 (final evaluation): mean reward 139.3, worst seed 29.1.
