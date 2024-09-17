import sys

def revert_base_9(n):
    return (n - 1) % 9 + 1

def read_sudoku(filename):
    try:
        with open(filename, "r") as file:
            output = file.read().strip()

            if output.lower()=="unsat":
                    return "unsatisfiable"
            else:
                 # Read the file, convert numbers to integers, and return as a list
                 return [int(revert_base_9(int(num))) for num in output.split() if num.isdigit() and int(num) > 0]
    except FileNotFoundError:
        print("Error: File not found")
    except Exception as e:
        print("An error occurred:", e)
    return None

def generate_file(location,grid):
    # Print the Sudoku grid
    with open(location,"w") as sudoku_file: 
        if grid == "unsatisfiable":
            sudoku_file.write("unsatisfiable")
        else:
            for i, num in enumerate(grid, start=1):
                sudoku_file.write(str(num) + " ")
                if i % 3 == 0 and i % 9 != 0:
                    sudoku_file.write("| ")
                if i % 9 == 0 and i % 27 != 0:
                    sudoku_file.write("\n")
                    if (i // 9) % 3 == 0:
                     sudoku_file.write("- " * 11+"\n")
                if i % 27 == 0 and i != 81:
                    sudoku_file.write("\n")
                    sudoku_file.write("- " * 11+ "\n")

def main():
    if len(sys.argv) != 3:
        print("Error: Please provide the input file name as a command line argument")
        return

    filename = sys.argv[1]
    sudoku_grid = read_sudoku(filename)
    generate_file(sys.argv[2],sudoku_grid)
if __name__ == "__main__":
    main()
