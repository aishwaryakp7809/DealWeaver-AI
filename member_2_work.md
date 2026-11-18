# DEALWEAVER AI -- Member 2 Work Documentation

## 1. Overview

**Role:** Member 2 -- Buyer Agent and Seller Agent

This document describes the rule-based Buyer Agent and Seller Agent
implemented for DEALWEAVER AI, the automated negotiation example that
connects them, and the tests used to verify their current behaviour.

The agents independently represent the buyer and seller. They exchange
offers through a Python negotiation loop and return structured
decisions.

## 2. Responsibilities and scope

### Buyer Agent

File: `agents/buyer_agent.py`

The Buyer Agent:

-   Stores the buyer's maximum budget and opening offer.
-   Makes the buyer's opening offer.
-   Evaluates offers received from the Seller Agent.
-   Calculates counteroffers using a gradual concession strategy.
-   Never proposes an amount above the buyer's maximum budget.
-   Can reject an individual offer without ending the negotiation.
-   Can withdraw from the negotiation.
-   Tracks its negotiation round and whether negotiation is active.
-   Can accept a Mediator suggestion as an optional input, while
    retaining independent control of its final decision.

### Seller Agent

File: `agents/seller_agent.py`

The Seller Agent:

-   Stores the seller's listed price and minimum acceptable price.
-   Makes the seller's opening asking price.
-   Evaluates offers received from the Buyer Agent.
-   Calculates counteroffers using a gradual concession strategy.
-   Never proposes or accepts an amount below the seller's minimum
    acceptable price.
-   Can reject an individual offer without ending the negotiation.
-   Can withdraw from the negotiation.
-   Tracks its negotiation round and whether negotiation is active.

### Automated negotiation example

File: `examples/agent_negotiation.py`

The example connects both agents and:

-   Starts both agents using supplied negotiation settings.
-   Exchanges offers automatically.
-   Records each action in a negotiation history.
-   Stops when an agent accepts, a no-deal condition is reached, or the
    negotiation otherwise ends.
-   Returns a structured result containing the status, final price,
    round count, reason, and history.

This is currently a local, rule-based simulation using one set of
example buyer and seller inputs. It is not yet a connected two-user
application or a live dashboard workflow.

## 3. Negotiation strategy and formulas

Both agents use a gradual concession schedule. The schedule determines
each agent's target price for the current round. The agent then
evaluates the other party's offer against that target.

Let:

-   \(r\) = current negotiation round
-   \(N\) = maximum number of rounds
-   (B_0) = buyer's opening offer
-   (B\_{`\max`{=tex}}) = buyer's maximum budget
-   (S_0) = seller's listed price
-   (S\_{`\min`{=tex}}) = seller's minimum acceptable price

For (N \> 1), the progress value is:

\[ Progress = `\min`{=tex}`\left`{=tex}(`\frac{r-1}{N-1}`{=tex},
1`\right`{=tex}) \]

For (N = 1), the progress value is set to 1.

### Buyer target price

\[ BuyerTarget = B_0 + (B\_{`\max`{=tex}}-B_0)`\times `{=tex}Progress \]

The buyer's target gradually increases from the opening offer towards
the maximum budget.

### Seller target price

\[ SellerTarget = S_0 - (S_0-S\_{`\min`{=tex}})`\times `{=tex}Progress
\]

The seller's target gradually decreases from the listed price towards
the minimum acceptable price.

These are target schedules, not guaranteed transaction prices. Each
agent still evaluates the offer received from the other party. The
agents' strategies can be made more adaptive in a later integration
phase.

## 4. Decision format

Both agents return a dictionary with the same basic structure:

``` python
{
    "action": "counter",
    "price": 7750.0,
    "reason": "Buyer calculated a counteroffer using its own strategy.",
    "round": 2
}
```

Current actions:

  -----------------------------------------------------------------------
  Action                              Meaning
  ----------------------------------- -----------------------------------
  `accept`                            Accept the other party's offer and
                                      end the negotiation successfully.

  `reject`                            Reject the current offer. The
                                      negotiation remains active.

  `counter`                           Make a counteroffer and continue
                                      negotiating.

  `no_deal`                           End the negotiation without an
                                      agreement.
  -----------------------------------------------------------------------

A `reject` decision is not the same as withdrawing. The `withdraw()`
method ends the negotiation. The negotiation can also end when the
maximum number of rounds is reached or when the Mediator confirms that
no feasible deal exists.

## 5. Mediator integration interface

The Buyer Agent's `receive_offer()` method supports these optional
parameters:

``` python
buyer.receive_offer(
    seller_offer=9500,
    mediator_suggestion=7500,
    no_feasible_deal=False
)
```

-   `seller_offer`: the current offer received from the seller.
-   `mediator_suggestion`: an optional suggested target price from the
    Mediator.
-   `no_feasible_deal`: set to `True` only when the Mediator/backend has
    checked both parties' limits and confirmed that no feasible overlap
    exists.

The Buyer Agent evaluates a Mediator suggestion independently. The
suggestion does not override the buyer's maximum budget or the agent's
own target calculation.

The Seller Agent currently uses its own rule-based strategy and does not
yet accept a Mediator suggestion parameter. Its interface can be
extended after the team agrees on the shared integration contract.

## 6. Example negotiation

Example settings:

  Parameter                               Value
  ----------------------------------- ---------
  Buyer's maximum budget                ₹10,000
  Buyer's opening offer                  ₹7,000
  Seller's listed price                 ₹12,000
  Seller's minimum acceptable price      ₹8,000
  Maximum rounds                              5

Observed negotiation:

    Turn Agent    Action                Price
  ------ -------- ----------------- ---------
       1 Buyer    Opening counter      ₹7,000
       1 Seller   Opening counter     ₹12,000
       2 Buyer    Reject                  ---
       2 Seller   Counter             ₹11,000
       3 Buyer    Reject                  ---
       3 Seller   Counter             ₹10,000
       4 Buyer    Counter              ₹9,250
       4 Seller   Accept               ₹9,250

**Observed result:** Deal successful at ₹9,250 in 4 negotiation rounds.

The buyer's maximum budget and seller's minimum acceptable price are
both respected.

## 7. Project files

The Member 2 contribution currently includes:

``` text
DEALWEAVER_AI/
│
├── agents/
│   ├── buyer_agent.py
│   └── seller_agent.py
│
├── examples/
│   └── agent_negotiation.py
│
└── tests/
    ├── test_buyer_agent.py
    ├── test_seller_agent.py
    └── test_negotiation.py
```

The project may also contain other files and folders contributed by the
other team members.

## 8. How to run

Run commands from the main DEALWEAVER AI project directory.

### Run the automatic negotiation example

``` bash
python -m examples.agent_negotiation
```

### Run the Buyer Agent tests

``` bash
python -m pytest tests/test_buyer_agent.py -v
```

### Run the Seller Agent tests

``` bash
python -m pytest tests/test_seller_agent.py -v
```

### Run the combined negotiation tests

``` bash
python -m pytest tests/test_negotiation.py -v
```

### Run all project tests

``` bash
python -m pytest tests/ -v
```

Install pytest if required:

``` bash
pip install pytest
```

## 9. Test results

The following results were observed in the development environment:

  Test file                  Tests passed
  ------------------------ --------------
  `test_buyer_agent.py`                 7
  `test_seller_agent.py`               10
  `test_negotiation.py`                 5
  **Total**                        **22**

**Observed result: 22 passed, 0 failed.**

The test run displayed one `PytestRemovedIn10Warning` from the installed
AnyIO pytest plugin. It did not cause any test failures and was not an
error in the agent code.

These results describe the test run performed during development. Run
the commands again after any code changes.

## 10. Current limitations and future integration

The current implementation is a rule-based prototype. The following work
remains for later team integration:

1.  Agree on the final shared negotiation-state structure and function
    signatures with Member 3 and Member 4.
2.  Integrate Mediator feasibility checks and suggested prices.
3.  Connect the existing BiLSTM intent predictor through Member 3's
    Analyst module. The model predicts negotiation intent; it does not
    directly calculate prices.
4.  Consider using negotiation history and predicted intent to improve
    agent strategy.
5.  Connect the agents to the Streamlit interface and, if required, a
    shared backend for two separate users.
6.  Ensure private values (buyer's maximum budget and seller's minimum
    acceptable price) are not exposed to the other party.
7.  Add further tests for integration, repeated offers, invalid shared
    state, withdrawals, and edge cases.

## 11. Summary

Member 2 has implemented a rule-based Buyer Agent and Seller Agent,
created an automatic negotiation example, and verified the current
implementation with 22 passing tests.

The agents independently calculate counteroffers using gradual
concession formulas, respect their respective price boundaries, and
exchange structured decisions. The implementation is ready for review
and coordination with the Mediator, Analyst, and user-interface modules.
