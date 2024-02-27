This program calculates likelihoods for a person having a hearing impairment.
The genes of parents affect the child, depending on how many copies of the gene the parents have.
Person can have either 0, 1 or 2 copies of the gene.

If parent has 2 genes, the gene is passed on the child with probability 1. With 1 copy of the gene, the probability is 0.5, and with 0 copies the gene is passed with probability 0. 
In case of probability of 1 or 0, there is a small probability to undergo additional mutation.

The program models the relationships with a Bayesian Network. 

For example:

            MotherGene            FatherGene
           |    |    |          |     |     |
           |  0,1,2  |          |    0,1,2  |
           |         |          |           |
       MotherTrait   |          |        FatherTrait       
         Yes,No      |          |          Yes,No
                     |          |
                       ChildGene
                          0,1,2
                           |
                           |
                       ChildTrait
                          Yes,No



