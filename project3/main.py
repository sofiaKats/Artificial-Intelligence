# AI Assignment 3 | 2021-2022 | Sofia Meropi Katsaouni sdi1800070
import csp
import sys
import pandas as pd
import time

from search import Problem


class Timetable(csp.CSP):
    def __init__(self, semester, courses, professor, difficulty, lab):
        self.semester = semester
        self.professor = professor
        self.difficulty =  difficulty
        self.lab = lab

        self.constraint_counter  = 0

        # variable is list of all the courses
        self.variables = courses.copy()

        #domain is a dictionary with all the possible hours and days of examination for each subject
        # {subject:[(day1,slot1),(day1,slot2)...etc]}
        self.domain = {}
        hour_slots = []
        slots = ["9:00-12:00", "12:00-3:00", "3:00-6:00"]
        for day in range(1,22):
            for slot in slots:
                hour_slots.append((day,slot))
        
        for sub in courses:
            self.domain[sub] = hour_slots

        # neighbors of a subject (sub) is every other subject except sub
        self.neighbors = {}
        for sub in courses:
            subjects = courses.copy()
            subjects.remove(sub)
            # neighbors --> dictionary with {subject:[neighbor_subject1, nghb_sub2...]etc}
            self.neighbors[sub] = subjects

        # since every subject participates in a constraint with every other subject
        # due to the limitation of one room which means that no more than one course
        # can be examined at the same time
        # i have a list of tuples type (variable, neighbor) used at dom/wdeg
        constraint_tuples = list()
        for subject in self.variables:
            for neighbor in self.neighbors[subject]:
                constraint_tuples.append((subject,neighbor))
       
        csp.CSP.__init__(self , self.variables , self.domain, self.neighbors, self.var_constraints, constraint_tuples)



    def var_constraints(self,A,a,B,b):
        self.constraint_counter += 1 # var_constraint was called --> counter incremented
        #if it's the same subject or the same day and hour 
        if(A == B or a == b ):
            return False

        indexA = self.variables.index(A)
        indexB = self.variables.index(B)
        #print("sub1: ",self.variables[indexA]," sub2: ",self.variables[indexB])

        # if it's the same day
        if(a[0] == b[0]):
            #if it's on the same semester
            if(self.semester[indexA] == self.semester[indexB]):
                return False
            #if it's the same professor that teaches subject A and B
            if(self.professor[indexA] == self.professor[indexB]):
                return False

            #if the two subjects both have labs there are only 3 slots
            #so the examination of two subjects and the labs can't happen on the same day
            if(self.lab[indexA] and self.lab[indexB]):
                return False

            # if only one of the subjects has a lab
            elif(self.lab[indexA]):
                # if theory is examined in the last slot, no slot left for lab
                if(a[1] == "3:00-6:00"):
                    return False
                # if the lab can not be examined right after the theory examination
                if( (a[1]=="9:00-12:00" and b[1]=="12:00-3:00") or (a[1]=="12:00-3:00" and b[1]=="3:00-6:00") ):
                    return False
                if( (a[1]=="12:00-3:00" and b[1]=="9:00-12:00") or (a[1]=="3:00-6:00" and b[1]=="12:00-3:00") ):
                    return False

            elif(self.lab[indexB]):
                # if theory is examined in the last slot, no slot left for lab
                if(b[1] == "3:00-6:00"):
                    return False
                if( (a[1]=="9:00-12:00" and b[1]=="12:00-3:00") or (a[1]=="12:00-3:00" and b[1]=="3:00-6:00") ):
                    return False
                if( (a[1]=="12:00-3:00" and b[1]=="9:00-12:00") or (a[1]=="3:00-6:00" and b[1]=="12:00-3:00") ):
                    return False
        
        # if the subjects are hard and the examination of the two happens 
        # within less than a 2 day gap
        if(abs(a[0]-b[0]) <= 2):
            if(self.difficulty[indexA] and self.difficulty[indexB]):
                return False

        return True

    def printStatistics(self, time_elapsed, nodes_expanded, algorithm):
        print("\n\n\n\n\n")
        print("Running ",algorithm," ...")
        s = "{:<10} {:^15} {:^20}".format("time elapsed","nodes expanded","constraint checks")
        print("\t\t\t",s)
        s = "{:<10.2f} {:^15.2f} {:^20}".format(time_elapsed,nodes_expanded,self.constraint_counter)
        print("\t\t\t",s)

def main():
    data = pd.read_csv('Στοιχεία Μαθημάτων.csv') # open excel file
    semester = list(data["Εξάμηνο"])
    courses = list(data["Μάθημα"])
    professor = list(data["Καθηγητής"])
    difficulty = list(data["Δύσκολο (TRUE/FALSE)"])
    lab = list(data["Εργαστήριο (TRUE/FALSE)"])

    problem = Timetable(semester,courses,professor,difficulty,lab)

    if(sys.argv[1] == "mac+mrv"):
        start = time.time()
        csp.backtracking_search(problem, csp.mrv, csp.lcv, csp.mac)
        end = time.time()
    elif(sys.argv[1] == "fc+mrv"):
        start = time.time()
        csp.backtracking_search(problem, csp.mrv, csp.lcv, csp.forward_checking)
        end = time.time()
    elif(sys.argv[1] == "mincon"):
        start = time.time()
        out = csp.min_conflicts(problem)
        end = time.time()
        print(out)
    elif(sys.argv[1] == "bt"):
        start = time.time()
        csp.backtracking_search(problem)
        end = time.time()
    elif(sys.argv[1] == "bt+mrv"):
        start = time.time()
        csp.backtracking_search(problem, csp.mrv)
        end = time.time()
    elif(sys.argv[1] == "fc+dom"):
        start = time.time()
        csp.backtracking_search(problem, csp.dom_wdeg, csp.lcv, csp.forward_checking)
        end = time.time()
    elif(sys.argv[1] == "mac+dom"):
        start = time.time()
        csp.backtracking_search(problem, csp.dom_wdeg, csp.lcv, csp.mac)
        end = time.time()
    elif(sys.argv[1] == "bt+dom"):
        start = time.time()
        csp.backtracking_search(problem, csp.dom_wdeg, csp.lcv)
        end = time.time()

    if(len(sys.argv) > 2):
        if(sys.argv[2] == "display"):
            problem.display(problem.infer_assignment())
        elif(sys.argv[2] == "mydisplay"):
            problem.my_display2()

    time_elpased = end - start
    # function for ii) of exercise 1
    #problem.printStatistics(time_elpased, problem.nassigns, sys.argv[1])

if __name__ == '__main__':
	main()