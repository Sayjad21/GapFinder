# Discretised Q-Learning for Pole Balancing

## Abstract
A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

## Experimental setup
Classic CartPole dynamics. States are discretised into 6 pole-angle bins and 6 angular-velocity bins. The agent is tabular Q-learning with discount 0.99. Exploration is epsilon-greedy; epsilon decays by a factor of 0.99 per episode and is floored at 0.05. Q-values are updated with a constant learning rate of 0.1. Q-values are initialised to zero. Rewards are used unnormalised. We train for 400 episodes and evaluate the greedy policy for 20 episodes, averaging over 10 random seeds.

## Results
Figure 1 (final evaluation): mean reward 94.9; worst seed 63.9.
