# Routine app pseudocode

# Method1: BruteForce
    * Find all the valid classes for a teacher
    * iterate over all possible routines
    * check if the routine is valid :: no two classes of same teacher at the same time unless merged
    * return all the valid routines

# Method2: Genetic Algorithm
    * Find all valid classes for a teacher
    * Initialize with a random routine
    * Calculate fitness
    * Mutate
    * Crossover
    * Repeat until fitness is 100%

## Parameters:
   full time teachers: available all the time
   part time teachers: available at certain times
   One subject can have multiple teachers: Normal class, merged class

   class can be merged with other classes
   teachers can be merged
   
   Normal class:
      * one teacher per class unless
   Merged class:
      * Teacher Merged: n teachers per class at the same time
      * Class Merged: n classes per teacher  at the same time

