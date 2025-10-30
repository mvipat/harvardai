import unittest
from generate import CrosswordCreator
from crossword import Crossword

class TestCrosswordCreator(unittest.TestCase):
    def test_add_one(self):
        crosswordInstance = Crossword("data/structure2.txt","data/words2.txt")
        instance = CrosswordCreator(crosswordInstance)
        instance.enforce_node_consistency()
        for variable1,words in instance.domains.items():
          for variable2,words in instance.domains.items():
            if variable1 != variable2:
               instance.revise(variable1,variable2)
 
        print(f" domain: {instance.domains}")

if __name__ == '__main__':
    unittest.main()