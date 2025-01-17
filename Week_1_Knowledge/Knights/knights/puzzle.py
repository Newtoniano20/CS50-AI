from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Puzzle 0 Knowledge
    Biconditional(AKnight, And(AKnave, AKnight)),
    # General Knowledge
    Or(And(AKnave, Not(AKnight)), And(AKnight, Not(AKnave))),
    Or(And(BKnave, Not(BKnight)), And(BKnight, Not(BKnave))),
    Or(And(CKnave, Not(CKnight)), And(CKnight, Not(CKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Puzzle 1 Knowledge
    Biconditional(AKnight, And(AKnave, BKnave)), # If A is truthful
    Biconditional(AKnave, And(Not(AKnight), Not(BKnave))), # If A is lying

    # General Knowledge
    Or(And(AKnave, Not(AKnight)), And(AKnight, Not(AKnave))),
    Or(And(BKnave, Not(BKnight)), And(BKnight, Not(BKnave))),
    Or(And(CKnave, Not(CKnight)), And(CKnight, Not(CKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Puzzle 2 Knowledge
    Implication(AKnight, BKnight), # A would be truthful
    Implication(AKnave, BKnight), # A would be lying
    Biconditional(BKnight, AKnave), # B Would be truthful
    Implication(BKnave, AKnave), # B would be lying

    # General Knowledge
    Or(And(AKnave, Not(AKnight)), And(AKnight, Not(AKnave))),
    Or(And(BKnave, Not(BKnight)), And(BKnight, Not(BKnave))),
    Or(And(CKnave, Not(CKnight)), And(CKnight, Not(CKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Puzzle 3 Knowledge
    Or(AKnave, AKnight),
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    Biconditional(BKnight, CKnave),
    Biconditional(CKnight, AKnight),
    Biconditional(AKnave, CKnave),

    # General Knowledge
    Or(And(AKnave, Not(AKnight)), And(AKnight, Not(AKnave))),
    Or(And(BKnave, Not(BKnight)), And(BKnight, Not(BKnave))),
    Or(And(CKnave, Not(CKnight)), And(CKnight, Not(CKnave)))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
