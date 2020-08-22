# Procal
Simple CLI program to aid those learning propositional calculus.

![stability-wip](https://img.shields.io/badge/stability-work_in_progress-lightgrey.svg)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Generic badge](https://img.shields.io/badge/You%20didn%27t-ask%20for%20this-red.svg)](https://shields.io/)

## Features
### Truth table generator
```
$ .\procal "P or (P and ¬Q) and ¬Q" -tt
    +---+---+-----+-------------+-------------------+---------------------------+
    | P | Q | ¬Q  | (P and ¬Q)  | (P and ¬Q) and ¬Q |  P or ((P and ¬Q) and ¬Q) |
    +---+---+-----+-------------+-------------------+---------------------------+
    | F | F |  T  |      F      |         F         |             F             |
    | F | T |  F  |      F      |         F         |             F             |
    | T | F |  T  |      T      |         T         |             T             |
    | T | T |  F  |      F      |         F         |             T             |
    +---+---+-----+-------------+-------------------+---------------------------+

$ .\procal "P | (P & ¬Q) & P" -tt=0
    +---+---+---------------------+
    | P | Q | P | ((P & ¬Q) & P)  |
    +---+---+---------------------+
    | F | F |          F          |
    | F | T |          F          |
    | T | F |          T          |
    | T | T |          T          |
    +---+---+---------------------+
```
### Proof generator (Not yet implemented)
```
$ .\procal -D "(P <=> Q) <=> (¬P & ¬Q) | (P & Q)"
    (P ↔ Q) ↔ (¬P ∧ ¬Q) ∨ (P ∧ Q)

    1. (P ↔ Q)  ↔ (P → Q) ∧ (Q → P)                                 (By Material Equivalence)
    2.           ↔ (¬P ∨ Q) ∧ (¬Q ∨ P)                             (By Material Implication)
    3.           ↔ [(¬P ∨ Q) ∧ ¬Q] ∨ [(¬P ∨ Q) ∧ P]               (By Distributive Property of ∧ w/r to ∨)
    4.           ↔ [(¬P ∧ ¬Q) ∨ (Q ∧ ¬Q)] ∨ [(¬P ∧ P) ∨ (Q ∧ P)] (By Distributive Property of ∧ w/r to ∨)
    5.           ↔ [(¬P ∧ ¬Q) ∨ F] ∨ [F ∨ (Q ∧ P)]                (By Consistency)
    6.           ↔ (¬P ∧ ¬Q) ∨ (Q ∧ P)                             (By Dominance)

```

### And much more... (hopefully)

## FAQ

### Why?
Yes.

### Is it reliable?
60% of the time works every time.
