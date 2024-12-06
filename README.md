This script was created to save time when writing the 3rd assignment in Discrete Mathematics 🧮

It performs logical operations represented as Unicode strings (`g5(x, y, z) = (x ∨ y ∨ z) ∧ (x̅ ∨ y) ∧ (x ∨ z)`) that can have only two states (on/off). This solves 1\3 problems required in the report, so it is planned to create two more scripts for solving perfect disjunctive normal form (pDnf) and perfect conjunctive normal form (dCnf).

Used Python (Miniconda🐍) with product.<b>itertools</b> (`as cartesian product of the user-input iterables`), <b>tabulate</b> (`as gui-cli preproccesor`), <b>re</b> (`for Replace logical negation`), <b>unicodedata</b> (`for normalising`)
