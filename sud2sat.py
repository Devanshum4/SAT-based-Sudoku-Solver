import sys

# x = column 
# y = row
# z = number

def convert_to_base_9(x,y,z):
    return (81*(y-1)+9*(x-1)+(z-1)+1)

def make_cnf(output_file, DIMACS_encoding):
    clause_file = open(output_file, "w+") #opening output file 
    clause_file.write('c A CNF File - Minimal Encoding\n')
    clause_file.write('p cnf 729 8829\n') #writing number of variables and clauses
     
	 #Clause 1 : There is at least one number in each entry 
    for y in range(1,10):
        for x in range(1,10):
            for z in range(1,10):
                clause_file.write(str(convert_to_base_9(x,y,z))+ " ")
            clause_file.write(" 0\n")
    
	#Clause 2: Each number appears at most once in each row
    for y in range(1,10):
        for z in range(1,10):
            for x in range(1,10):
                for i in range((x+1),10):
                    clause_file.write("-" + str(convert_to_base_9(x,y,z)) + " -" + str(convert_to_base_9(i,y,z)) + " 0\n") 
    
	#Clause 3: Each number appears at most once in each column
    for x in range(1,10):
        for z in range(1,10):
            for y in range(1,10):
                for i in range((y+1), 10):in
                    clause_file.write("-" + str(convert_to_base_9(x,y,z)) + " -" + str(convert_to_base_9(x,i,z)) + " 0\n") 
    
	#CLause 4: Each number appears at most once in each 3*3 sub-grid (Row):
    for z in range(1,10):
        for i in range(0,3):
            for j in range(0,3):
                for x in range(1,4):
                    for y in range(1,4):
                        for k in range((y+1),4):
                            clause_file.write("-" + str(convert_to_base_9((3*i+x), (3*j+y), z)) + " -" + str(convert_to_base_9((3*i+x),(3*j+k), z)) + " 0\n")

	#Clause 5: Each number appears at most once in each 3*3 sub-grid:
    for z in range(1, 10):
        for i in range(0, 3):
            for j in range(0, 3):
                for x in range(1, 4):
                    for y in range(1, 4):
                        for k in range((x+1), 4):
                            for l in range(1, 4):
                                clause_file.write("-" + str(convert_to_base_9((3*i+x), (3*j+y), z)) + " -" + str(convert_to_base_9((3*i+k),(3*j+l), z)) + " 0\n") 
    
    clause_file.close()

    reading_clause_file = open(output_file, "r+") #reading written clause_file 
    CNF_file = open("CNF.txt", "w+") #creating CNF.txt

    #Reading the header line from reading_clause_file
    header_line_1 = reading_clause_file.readline()
    CNF_file.write(header_line_1)
    header_line_2 = reading_clause_file.readline().split()
    clauses = int(header_line_2[3]) + len(DIMACS_encoding)
    header_line_2[3] = str(clauses)
    CNF_file.write(" ".join(header_line_2) + "\n")

    # Copy existing clauses
    for line in reading_clause_file:
        CNF_file.write(line)

    # Write DIMACS encoding clauses
    for number in DIMACS_encoding:
        CNF_file.write(str(number) + " 0\n")

    # Close files
    reading_clause_file.close()
    CNF_file.close()

def main():
    DIMACS_encoding = []
    
    if len(sys.argv) < 3:
         print("Error: Missing puzzle file or the output file")
         return
    
    try:
        puzzle_txt = open(sys.argv[1], "r").read().replace('\n', '')
    except IndexError:
        puzzle_txt = sys.stdin
    except FileNotFoundError:
        print("File specified does not exist!")
    except IOError as e:
        print(f"An error occurred: {e}")
    
    
    if len(puzzle_txt) < 81:
         print("Error: Wrong format of the puzzle. Hint: It is a 3*3 grid puzzle")
    else:
        y, x = 1, 1
        for i in range(0, 81):
            if puzzle_txt[i].isdigit() and int(puzzle_txt[i]) > 0:
                DIMACS_encoding.append(convert_to_base_9(x, y, int(puzzle_txt[i])))
            x += 1
            if x == 10:
                x, y = 1, y + 1
    print(DIMACS_encoding)
                
    make_cnf(sys.argv[2], DIMACS_encoding)

if __name__ == "__main__":
    main()
