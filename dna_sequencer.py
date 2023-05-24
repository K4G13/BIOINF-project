import sys
import re
import numpy as np

def get_data(file_dir=""):

    if(file_dir==""):
        print(f"(!) no file input")
        print(f"(!) using test/test.10-2+2.txt file")
        file_dir = "test/test.10-2+2.txt"

    if file_dir[-4:] != ".txt":
        file_dir += ".txt"

    try:
        file = open(file_dir, "r")
        data = file.read().split()
        file.close()
    except:
        print(f"(!) couldn't find file: {file_dir}")
        print("Exiting...")
        exit()

    temp = file_dir.split(".")[1]
    negatives = re.findall("\-[0-9]*",temp)
    positives = re.findall("\+[0-9]*",temp)

    if negatives == []: negatives = 0
    else: negatives = int(negatives[0][1:])

    if positives == []: positives = 0
    else: positives = int(positives[0][1:])

    seq_length = int(re.findall(".[0-9]*",temp)[0])

    return data,negatives,positives,seq_length

def coverage(str_a,str_b):
    if str_a == str_b:
        return -1
    
    for i in range(len(str_a)):
        if str_a[i:] == str_b[:-i]:
            return int(len(str_a) - i)
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

def summary(resault,og_set,display=2):
    print("------------------ Summary: ------------------")
    print(f"Sequence length: \t{resault['seq len']}\t|shoud be: {og_seq_len}")
    print(f"Positive errors: \t{len(resault['positives'])}\t|shoud be: {og_positives}")
    print(f"Negative errors: \t{resault['negatives']}\t|shoud be: {og_negatives}")
    print(f"Elements in sequence: \t{resault['seq no el']}")

    seq = []
    for i in resault["seq"]: seq.append(og_set[i])

    #display one below another
    if display==1:
        prev = seq[0]
        spaces = 0
        print(seq[0])
        for el in seq[1:]:
            spaces += L - coverage(prev,el)
            for _ in range(spaces): print(" ",end="")
            print(el)
            prev = el

    #display one string
    if display==2:
        str = "".join(seq[0])
        prev = seq[0]
        for el in seq[1:]:
            str += el[coverage(prev,el):]
            prev = el
        print(str)

    #display sequence elements in list
    if display==3:
        print(seq)
    

data_dir = ""
if len(sys.argv) >= 2: data_dir = sys.argv[1]
    
og_set,og_negatives,og_positives,og_seq_len = get_data(data_dir)
L = len(og_set[0]) # length of oligonucleotide 

coverage_matrix = create_coverage_matrix(og_set)

best_resault = {
    "seq" : [], #sequence (indexes)
    "seq len" : 0, #length of sequence
    "seq no el": 0, #number of elements in sequence
    "negatives" : 0, #number of negative errors
    "positives" : 0 #number of positive errors 
}

all_elements_in_og_set = len(og_set)
index_of_iteration = 0

for starting_el_id in range(len(og_set)):
    print(f"Starting seq: {og_set[starting_el_id]} {round(index_of_iteration/all_elements_in_og_set*100,2)}%     ", end='\r', flush=True)
    index_of_iteration+=1

    availables = list(range(0,len(og_set),1))
    availables.pop(starting_el_id)

    resault = [starting_el_id]
    resault_length = L

    negative_errors = 0

    while(resault_length < og_seq_len or availables==[]):

        max_score = og_seq_len - resault_length
        succesor = best_successor(availables,resault[-1],max_score,coverage_matrix)

        if succesor == -1: break

        length_added = L - coverage_matrix[resault[-1]][succesor] 
        resault_length += length_added
        if length_added != 1: 
            negative_errors += length_added - 1

        resault.append(succesor)
        availables.pop(availables.index(succesor)) #HERE

    if resault_length >= best_resault["seq len"] and len(resault) > best_resault["seq no el"]:
        best_resault["seq"] = resault
        best_resault["seq no el"] = len(resault)
        best_resault["seq len"] = int(resault_length)
        best_resault["negatives"] = int(negative_errors)
        best_resault["positives"] = list(set(list(range(0,len(og_set),1))) - set(resault))
    
    if resault_length == og_seq_len:
        break #HERE
        if best_resault["positives"] == og_positives and best_resault["negatives"] == og_negatives:
            break

print()
summary(best_resault,og_set,2)