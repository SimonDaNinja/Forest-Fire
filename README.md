# Forest-Fire

This is a simple simulation of a forest fire model.

In each timestep, empty cells grow a tree with a certain probability.

In each timestep, there is a certain probability that a match will be dropped on a tile with a tree, removing the tree
and replacing it with fire.

When a tile has fire on it, all von neumann neighbours with trees on them will have their tree removed and replaced with fire,
*in the same timestep*.

At the beginning of every timestep, before trees are grown, and matches dropped, all cells with fire will be set to empty.
