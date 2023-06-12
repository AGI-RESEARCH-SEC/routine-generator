# Routine app pseudocode

# Method1: BruteForce 
     * ***note: (Simple Bruteforce is Not feasible: assuming 1000 searches per second would take around 10^34 years to complete)***
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

# Note:
    - subject has: student, teacher, course_name
    - before finalizing: replace time with datetime in seconds so that whole syllabus can be covered
    - some subjects like elective-I has special subject time (6:00 - 10:00)
# Todo:
    * give unique id to each teacher instead of using name as unique identifier
    * give seperate folder to each class
    * gene1:classroom.time generated (random, mutation, crossover, ...) from sample space of teacher.feasible_time
    * 
    * check colliding routine for same teacher for multiple classes
    * fixed number of classes for students and teachers for 
# Errors
    * teachers[0].feasible_time is changing after running generating code. why?