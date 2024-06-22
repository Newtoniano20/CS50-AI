import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for v in self.crossword.variables:
            length = v.length
            inconsistent = []
            for x in self.domains[v]:
                if len(x) != length:
                    inconsistent.append(x)
            for x in inconsistent:
                self.domains[v].remove(x)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revise = False
        inconsistent = []
        constraint = self.crossword.overlaps[(x, y)] #ith of x , jth of y
        if constraint is None:
            return False
        for _x in self.domains[x]:
            found = False
            for _y in self.domains[y]:
                if _x[constraint[0]] == _y[constraint[1]]:
                    found = True
            if not found:
                revise = True
                inconsistent.append(_x)
        for _x in inconsistent:
            self.domains[x].remove(_x)
        return revise

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            arcs = list(self.crossword.overlaps.keys())
        while len(arcs) != 0:
            arc = arcs.pop()
            if self.revise(arc[0], arc[1]):
                if len(self.domains[arc[0]]) == 0:
                    return False
                neighbors = self.crossword.neighbors(arc[0])
                for z in neighbors:
                    if z == arc[1]:
                        pass
                    else:
                        arcs.append((z, arc[0]))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if assignment == {}:
            return False
        for v in self.crossword.variables:
            if v not in assignment:
                return False
            elif assignment[v] is None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Words follow binary constraint
        for key1, value1 in assignment.items():   
            for key2, value2 in assignment.items():
                if (key1, key2) in self.crossword.overlaps:
                    constraint = self.crossword.overlaps[(key1, key2)] #ith of x , jth of y
                    if constraint is None:
                        pass
                    elif value1[constraint[0]] != value2[constraint[1]]:
                        return False
        
        # two words are the same
        for key1, value1 in assignment.items():   
            for key2, value2 in assignment.items():
                if key1 != key2 and value1 == value2:
                    return False
        
        # inconsistent lenght
        for key, value in assignment.items():
            if len(value) != key.length:
                return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domain = self.domains[var]
        var_neighbor = self.crossword.neighbors(var)
        #print(var_neighbor)
        result = [0 for w in domain]
        for index, word in enumerate(domain):
            for n_var in var_neighbor:
                for n_word in self.domains[n_var]:
                    overlap = self.crossword.overlaps[(n_var, var)]
                    if n_word[overlap[0]] != word[overlap[1]]:
                            result[index] += 1
        temp = [(w, result[i]) for i, w in enumerate(domain)]
        result = sorted(temp, key=lambda var: var[1])
        true_result = {i[0] for i in result}
        return true_result

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        variables = self.crossword.variables
        best_option = None
        n_neighbors = 0
        min_values = 10*100 # set minimum number of remaining values in its domain to high value
        for var in variables:
            if var not in assignment:
                if len(self.domains[var]) < min_values:
                    best_option = var
                elif len(self.domains[var]) == min_values:
                    if self.crossword.neighbors(var) > n_neighbors:
                        n_neighbors = self.crossword.neighbors(var)
                        best_option = var
        return best_option
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            else:
                del assignment[var]
        return None
                


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
