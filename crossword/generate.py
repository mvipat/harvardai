import sys
import collections
import copy

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
        for variable,words in self.domains.items():
            #print(f"var {variable}")
            #print(f"word {words}")
            for word in words.copy():
                if variable.length != len(word):
                    #print(f"removing {word}")
                    words.remove(word)

        #print(f" domain: {self.domains}")

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        #print(f"revising: {x} {self.domains[x]} {y} {self.domains[y]}")
        overlap = self.crossword.overlaps[x,y]
        #print(f" overlap {overlap}")
        if overlap is None:
            return False
        
        revison_made = False
        for word_x in self.domains[x].copy():
            #print(f"words_x {word_x}")
            match = False
            for word_y in self.domains[y]:
                #print(f"word_x {word_x} word_y {word_y} word_x[overlap[0]] {word_x[overlap[0]]} word_y[overlap[1]] {word_y[overlap[1]]}")
                if word_x[overlap[0]] == word_y[overlap[1]]:
                    #print(f"matched {word_x} word_y {word_y} overlap[0] {overlap[0]} overlap[1] {overlap[1]} word_x[overlap[0]] {word_x[overlap[0]]} word_y[overlap[1]] {word_y[overlap[1]]}")
                    match = True
                    break

            if match is False:
                print(f"removing word {word_x} for variable {x} with words")
                self.domains[x].remove(word_x)
                revison_made = True

        #print(f"revised domain: {self.domains}")

        return revison_made

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        csp = None
        if arcs is None:
            csp = self.initial_arc()
        else:
            csp = collections.deque(arcs)

        print(f"csp {csp}")
        while csp:
            variable1,variable2 = csp.popleft()
            if self.revise(variable1,variable2):
                if len(self.domains[variable1]) == 0:
                    return False
                list_of_variables = self.crossword.neighbors(variable1)
                for near_neighbor in list_of_variables:
                    if near_neighbor != variable2:
                        print(f"adding neighbor {near_neighbor} for variable {variable1}")
                        csp.append((variable1,near_neighbor))
                        csp.append((near_neighbor,variable1))

        return True

    def initial_arc(self):
        """
        Returns all the possible arcs possible as a collections.dequue object using overlap functionality
        """
        csp = collections.deque()
        for variable1,words in self.domains.items():
          for variable2,words in self.domains.items():
            if variable1 != variable2:
               overlap = self.crossword.overlaps[variable1,variable2]
               if overlap is not None:
                   csp.append((variable1,variable2))
                   csp.append((variable2,variable1))
        
        return csp

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        #print(f"each variable has one word assignment {assignment}")
        completed = True
        for variable,words in self.domains.items():
            if variable in assignment:
                continue
            else:
                completed = False
                break

        return completed

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        print(f"entering consistent with assignment {assignment}")
        completed = True
        for variable,word in assignment.items():
            if completed:
                completed = self.check_duplicate(assignment, variable, word)
            else:
                break
            
            if completed:
                if variable.length != len(word):
                    completed = False
                    break
            else:
                break

            
            if completed:
                for variable_x,word_x in assignment.items():
                    for variable_y,word_y in assignment.items():
                        if variable_x == variable_y:
                            continue

                        overlap = self.crossword.overlaps[variable_x,variable_y]
                        #print(f" overlap {overlap}")
                        if overlap is None:
                            continue
                        
                        if word_x[overlap[0]] != word_y[overlap[1]]:
                            #print(f"matched {word_x} word_y {word_y} overlap[0] {overlap[0]} overlap[1] {overlap[1]} word_x[overlap[0]] {word_x[overlap[0]]} word_y[overlap[1]] {word_y[overlap[1]]}")
                            return False

        return completed
    
    def check_duplicate(self, assignment, variable, word):
        """
        Check whether assignment contains variables with same word as answer
        """

        for variable2,word2 in assignment.items():
            if variable != variable2:
                if word == word2:
                    print(f"word {word} already used in variable {variable} cannot use it in {variable2}")
                    return False
        
        return True
    
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        variable_x = var
        words_x = self.domains[var]
        ret_dict = dict()
        if words_x is not None:
            for word_x in words_x:
                ret_dict[word_x] = 0
                for variable_y in self.crossword.variables - set(assignment):
                    if variable_x == variable_y:
                        continue

                    overlap = self.crossword.overlaps[variable_x,variable_y]
                    #print(f" overlap {overlap}")
                    if overlap is None:
                        continue
                    
                    for word_y in self.domains[variable_y]:
                        #print(f"word_x {word_x} word_y {word_y} word_x[overlap[0]] {word_x[overlap[0]]} word_y[overlap[1]] {word_y[overlap[1]]}")
                        if word_x[overlap[0]] != word_y[overlap[1]]:
                            ret_dict[word_x] += 1

        sorted_keys_by_value = [key for key, value in sorted(ret_dict.items(), key=lambda item: item[1])]
        return sorted_keys_by_value

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        least_assigned_words = None
        for variable,words in self.domains.items():
            if variable in assignment:
                continue

            if least_assigned_words is None:
                least_assigned_words = variable
                continue

            if len(self.domains[least_assigned_words]) > len(words):
                least_assigned_words = variable

        print(f"least_assigned_words {least_assigned_words}")
        return least_assigned_words

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        print(f"entering backtrack with assignment {assignment}")
        if self.assignment_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)
        print(f"unassigned variable {variable} words {self.domains[variable]}")
        for word in self.order_domain_values(variable,assignment):
            print(f"checking {word}")
            assignment[variable] = word
            if self.consistent(assignment):
                print(f"assignment is consistent {word}")
                result = self.backtrack(assignment)
                if result:
                    return result
                
            print(f"assignment is not consistent removing {word}")
            del assignment[variable]

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
