from heredity import joint_probability
from heredity import get_probability
people = {
  'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
  'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
  'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}

one_gene = {'Harry','Lily','James'}
two_genes = {}
have_trait = {'Harry','Lily','James'}
p = joint_probability(people, one_gene, two_genes, have_trait)
print(p)
# Result should be = 7.9027E-5
print(f" Mother Father Probability 0: {get_probability(0)}")
print(f" Mother Father Probability 1: {get_probability(1)}")
print(f" Mother Father Probability 2: {get_probability(2)}")