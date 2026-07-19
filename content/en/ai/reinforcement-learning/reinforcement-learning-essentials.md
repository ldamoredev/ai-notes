---
title: "Reinforcement learning essentials"
description: States, actions, policies, returns, values, Bellman structure, exploration, and reward failure in one executable tabular model.
tags: [reinforcement-learning, mdp, bellman-equations, policies]
order: 1
updated: 2026-07-19
kind: overview
level: intermediate
status: current
prerequisites: [probability-likelihood-and-uncertainty]
last_verified: 2026-07-19
---
# Reinforcement learning essentials

Reinforcement learning studies sequential decisions whose consequences arrive over
time. The learner is not given the correct action for every situation. It observes
transitions and rewards, then tries to find a policy that maximizes expected future
return.

The central difficulty is causal credit under limited data: which earlier actions
made the later reward possible, and what should be tried when the current evidence is
incomplete?

## The Markov decision process

An MDP is commonly written \((\mathcal{S},\mathcal{A},P,R,\gamma)\):

- \(\mathcal{S}\): states.
- \(\mathcal{A}\): actions.
- \(P(s'\mid s,a)\): transition dynamics.
- \(R(s,a,s')\): reward signal.
- \(\gamma\in[0,1)\): discount factor.

The Markov assumption says the current state contains the information needed to
predict the next-state distribution given an action. A partially observed problem
violates that assumption unless history or belief state is included.

## Return, policy, and value

The discounted return from time \(t\) is:

\[
G_t=R_{t+1}+\gamma R_{t+2}+\gamma^2R_{t+3}+\cdots.
\]

A policy \(\pi(a\mid s)\) is a distribution over actions. The state value is:

\[
V^\pi(s)=\mathbb{E}_\pi[G_t\mid S_t=s],
\]

and the action value is:

\[
Q^\pi(s,a)=\mathbb{E}_\pi[G_t\mid S_t=s,A_t=a].
\]

Rewards are immediate observations; values are predictions of accumulated future
reward. Confusing them destroys the sequential structure.

## Bellman recursion

The optimal value obeys:

\[
V^*(s)=\max_a\sum_{s'}P(s'\mid s,a)
\left[R(s,a,s')+\gamma V^*(s')\right].
\]

This equation decomposes a long-horizon problem into one transition plus the value
of what follows. Dynamic programming uses known dynamics; model-free methods estimate
the same structure from experience.

## Executable artifact: value iteration

This deterministic three-state MDP has a short route and a looping action:

```python
states = ["start", "middle", "terminal"]
actions = {
    "start": [("advance", "middle", 0.0), ("wait", "start", -0.2)],
    "middle": [("finish", "terminal", 1.0), ("reset", "start", -0.1)],
    "terminal": [],
}
gamma = 0.9
value = {state: 0.0 for state in states}

for _ in range(50):
    updated = value.copy()
    for state in states:
        if actions[state]:
            updated[state] = max(
                reward + gamma * value[next_state]
                for _, next_state, reward in actions[state]
            )
    value = updated

policy = {
    state: max(
        actions[state],
        key=lambda item: item[2] + gamma * value[item[1]],
    )[0]
    for state in states if actions[state]
}
print(value)   # start is approximately 0.9; middle is 1.0
print(policy)  # advance, then finish
```

Change the waiting reward to positive `0.2`. With continuing discount, the loop may
become more attractive than completing the task. That is a tiny reward-specification
failure, not an optimization bug.

## Major algorithm families

| Family | Learns | Defining trade-off |
|---|---|---|
| Dynamic programming | values/policy from known model | exact sweeps require dynamics and state coverage |
| Monte Carlo | returns from complete episodes | unbiased target, often high variance |
| Temporal difference | bootstrapped values | lower variance, biased moving target |
| Q-learning | off-policy action values | can reuse behavior data; unstable with approximation |
| Policy gradient | policy parameters directly | handles stochastic/continuous actions; high variance |
| Actor-critic | policy plus learned value baseline | practical balance, more coupled failure modes |
| Model-based RL | dynamics plus planning/policy | data efficiency versus model bias |

## Exploration and coverage

Exploitation chooses the action that currently looks best. Exploration collects
information about alternatives. Epsilon-greedy is a baseline, not a universal
solution: directed uncertainty bonuses, entropy regularization, posterior sampling,
or structured exploration can use data more efficiently.

Offline RL adds a hard constraint. The learner cannot query the environment and must
avoid actions whose outcomes are unsupported by the dataset. A high predicted value
outside data coverage is often extrapolation error.

## Reward is a measurement, not the goal

An optimizer follows the reward that is implemented. Proxy gaps create specification
gaming: agents may exploit simulator bugs, terminate early, manipulate the evaluator,
or find behaviors the designer omitted. More optimization pressure can make a weak
proxy less aligned with the intended outcome.

RLHF uses this same framework with learned or rule-based preference signals. It does
not remove reward misspecification, distribution shift, or the need for evaluation.

## Failure modes

- Sparse and delayed reward makes credit assignment statistically difficult.
- Off-policy learning plus function approximation plus bootstrapping can diverge.
- Results are sensitive to seeds, environment versions, wrappers, and termination
  semantics.
- Simulator success may not transfer when real dynamics differ.
- Average return hides catastrophic tails and unsafe exploratory behavior.
- Benchmark reuse can turn environment-specific tuning into false generality.

## Production lens

Record environment and wrapper versions, observation/action preprocessing, episode
termination versus truncation, seeds, policy checkpoints, and evaluation policy.
Report return distributions, constraint violations, sample count, wall time, and
compute—not only the best seed. Separate online exploration permissions from offline
training; the risk boundary is a product decision.

## Exercises

1. Calculate `V(start)` by hand for the optimal two-step path.
2. Sweep the loop reward and discount factor; identify when waiting becomes optimal.
3. Replace deterministic transitions with a 20% reset probability and update the
   Bellman backup.
4. Write down one product goal and three proxy rewards; list how each could be gamed.

**Connects to:** [[ai/mathematics-for-ai/probability-likelihood-and-uncertainty|probability and uncertainty]] · [[ai/fine-tuning-and-alignment/rlhf-with-ppo|RLHF with PPO]] · [[ai/agents-and-tools/autonomy-and-control|autonomy and control]] · [[ai/ai-safety-and-security/excessive-agency|excessive agency]]

## Sources

- [Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html) — the canonical treatment of MDPs, values, TD learning, control, and approximation.
- [Algorithms for Reinforcement Learning](https://sites.ualberta.ca/~szepesva/papers/RLAlgsInMDPs.pdf) — a concise mathematical reference for core algorithms.
- [OpenAI Spinning Up](https://spinningup.openai.com/en/latest/) — equations, implementation guidance, and reproducibility advice for deep RL.
- [Deep Reinforcement Learning that Matters](https://arxiv.org/abs/1709.06560) — empirical evidence and recommendations for reliable experimental reporting.
- [Concrete Problems in AI Safety](https://arxiv.org/abs/1606.06565) — reward hacking, safe exploration, and distribution shift as practical safety problems.
