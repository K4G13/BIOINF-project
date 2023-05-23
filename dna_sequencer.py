import sys
import numpy as np

def get_data(file_dir=""):

    # get file dir from program arguments
    if not file_dir and len(sys.argv) >= 2:
        file_dir = sys.argv[1]

    if(file_dir==""):
        print(f"(!) get_data: no filename entered")
        exit()

    # add .txt at the end if there is not one
    if file_dir[-4:] != ".txt":
        file_dir += ".txt"

    try:
        file = open(file_dir, "r")
        data = file.read().split()
        file.close()
        return data
    except:
        print(f"(!) get_data: couldn't find file: {file_dir}")
        exit()

def coverage(str_a,str_b):
    if str_a == str_b:
        return -1
    
    for i in range(len(str_a)):
        if str_a[i:] == str_b[:-i]:
            return len(str_a) - i
    return 0

def create_coverage_matrix(o_list):
    # input o_list: list of oligonucleotides
    n = len(o_list)
    matrix = np.empty([n,n])

    for y in range(n):
        for x in range(n):
            matrix[y][x] = coverage(o_list[y],o_list[x])

    return matrix

def best_successor(availables,last_el_id,max_score,coverage_matrix):
    best = None
    best_score = -1

    for first_el in availables:
        first_el_coverage = coverage_matrix[last_el_id][first_el]
        if L - first_el_coverage > max_score: continue
        for second_el in availables:            
            second_el_coverage = coverage_matrix[first_el][second_el]
            sum_coverage = first_el_coverage + second_el_coverage            
            if L - sum_coverage > max_score: continue
            if sum_coverage > best_score:
                best_score = sum_coverage
                best = first_el

    if best == None:
        return -1
    else:
        return best

original_set = get_data("test")
# length of oligonucleotide
L = len(original_set[0]) 
# length of sequence
N = len(original_set) + L - 1
coverage_matrix = create_coverage_matrix(original_set)

output = []
output_length = 0
for starting_el in original_set:

    # print(f"Starting element: {starting_el}")

    availables_id = list(range(0,len(original_set),1))
    availables_id.pop(original_set.index(starting_el))

    resault = [original_set.index(starting_el)]
    resault_length = L

    while(resault_length<N or availables_id==[]):

        max_score = N - resault_length
        succesor = best_successor(availables_id,resault[-1],max_score,coverage_matrix)
        if succesor == -1:
            break
        resault_length += L - coverage_matrix[resault[-1]][succesor] 
        resault.append(succesor)
        availables_id.pop(availables_id.index(succesor))

    if resault_length > output_length:
        output = resault
        output_length = resault_length
    
    if resault_length == N:
        break

for i in resault:
    print(original_set[i])
print(resault_length)