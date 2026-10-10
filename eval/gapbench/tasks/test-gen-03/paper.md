# A Tabular Q-Learner Is Enough for CartPole

## Abstract
We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

## Experimental setup
Classic CartPole dynamics. States are discretised into 6 pole-angle bins and 6 angular-velocity bins. The agent is tabular Q-learning with discount 0.99. Exploration is epsilon-greedy; epsilon starts at 1.0, decays by a factor of 0.99 per episode and is floored at 0.05. Q-values are updated with a constant learning rate of 0.1. Q-values are initialised to zero. Rewards are used unnormalised. We train for 400 episodes and evaluate the greedy policy for 20 episodes, averaging over 10 random seeds.

## Results
Figure 1 (final evaluation): mean reward 302.1; worst seed 48.2.
