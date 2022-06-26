# Matching Algorithm for StudyJio

## The goal

To allocate $5n$ users into $n$ groups of five members into a somewhat *good allocation*. (For now, we assume that the number of users we have is a multiple of 5.)

## Definition of a 'good allocation'

The quality of an allocation is calculated as follows:

```
split the users into groups according to the allocation
for each group in allocation.groups:
    for every pair of members (m1, m2) in group.members:
        pair_compatibility = calculate_compatibility(m1, m2)
        remember pair_compatibility
    group_compatibility = the average value of all `pair_compatibility`s
    remember group_compatibility
allocation_quality = the average value of all `group_compatibility`s
return allocation_quality
```

## Compatibility between two users

To calculate the compatibility between two users,

1. $50$ points are given for each module in common.
2. $-100$ to $100$ points are given depending on how similar their learning styles are.
3. $5$ points are deducted for each kilometer of distance between them.

For example,

* Two people reading the same six modules, sharing identical learning styles, and living at the same place are very compatible with each other. ($400$ points)
* Two people who have no modules in common, who have opposite learning styles, and who live $50 \text{km}$ from each other are incompatible with each other. ($-350$ points)

# Genetic Algorithm Details

## Chromosome

A chromosome is an array that represents an allocation of the group members.

For example, the chromosome `[0, 0, 0, 0, 1, 0, 1, 1, 1, 1]` states that the users with `user_ID`s 0, 1, 2, 3, and 5 should form one group (with `group_ID` 0), whilc the rest with `user_ID`s 4, 6, 7, 8, 9 should form another group (with `group_ID` 1).

## Chromosome Invariants

1. Each chromosome should have a length of $5n$.
2. Each integer $i \in [0, n - 1]$ should appear in the chromosome exactly $5$ times.
3. $i < j \implies$ The first occurrence of $i$ is before the first occurrence of $j$.

Invariant 3 ensures that each allocation is represented by a unique chromosome.

For example, 

`[0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]`

and

`[1, 1, 1, 1, 1, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0]`

represent the same allocation, but only the former is valid.

Currently, the functions `repair_chromosome(chromosome)` and `validate_chromosome(chromosome)` has been written to enforce Invariants 1 and 2, whereas `reorder_chromosome(chromosome)` has been written to enforce Invariant 3.

## Chromosome Operations

During the course of the simulation, the chromosomes undergo the following changes.

### Mutation

Swap the values of two randomly chosen genes (numbers $\in [0, n-1]$) in the chromosome, with the hope that this produces a better allocation.



**This is implemented, but not used due to a mysterious `TypeError`.**
**`swap_mutation()` from the `pygad` library is used instead.**

### Crossover

The allocations of two chromosomes are combined.

**This is not yet implemented.**
