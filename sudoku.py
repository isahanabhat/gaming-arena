import random
import pandas as pd

def isSafe(mat, row, col):
    n = len(mat)

    for i in range(row):
        if mat[i][col]:
            return 0

    quadrants = {
        1 : [[0, 2], [0, 2]],
        2 : [[3, 5], [0, 2]],
        3 : [[6, 8], [0, 2]],
        4 : [[0, 2], [3, 5]],
        5 : [[3, 5], [3, 5]],
        6 : [[6, 8], [3, 5]],
        7 : [[0, 2], [6, 8]],
        8 : [[3, 5], [6, 8]],
        9 : [[6, 8], [6, 8]],
    }
    quadrants_vals = list(quadrants.values())
    quad = 0
    for q in range(1,10):
        if row in range(quadrants_vals[q - 1][0][0], quadrants_vals[q - 1][0][1] + 1):
            if col in range(quadrants_vals[q - 1][1][0], quadrants_vals[q - 1][1][1] + 1):
                quad = q
                break

    row_list = quadrants[quad][0]
    col_list = quadrants[quad][1]

    for i in range(row_list[0], row_list[1] + 1):
        for j in range(col_list[0], col_list[1] + 1):
            if mat[i][j]:
                return 0
    return 1


# Recursive function to place queens
def placeQueens(row, mat, result):
    n = len(mat)
    if row == n:
        ans = []
        for i in range(n):
            for j in range(n):
                if mat[i][j]:
                    ans.append(j + 1)
        result.append(ans)
        return

    for i in range(n):
        if isSafe(mat, row, i):
            mat[row][i] = 1
            placeQueens(row + 1, mat, result)

            # backtrack
            mat[row][i] = 0

def nQueen(n):
    # Initialize the board
    mat = [[0] * n for _ in range(n)]
    result = []

    # Place queens
    placeQueens(0, mat, result)

    return result

def get_combinations(file):
    n = 9
    result = nQueen(n)
    comb = pd.DataFrame(result, columns=["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"])
    comb.to_csv(file, index=False)

if __name__ == "__main__":
    file = r"input/sudoku_combinations.csv"
    # get_combinations(file)
    grid = [[0] * 9 for _ in range(9)]
    final_placements = []
    while True:
        try:
            cols = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"]
            comb = pd.read_csv(file)
            sudoku_groups = comb.groupby("C0")
            group_names = list(sudoku_groups.groups.keys())

            # groups dict
            group_dict = {}
            for name, group in sudoku_groups:
                group_dict[name] = group.reset_index()

            last = None
            final_placements = []


            for i in range(1, 10):
                # print("===== ITERATION ", i, "=====")
                """
                group_indices = (
                    {'group': name, 'start_index': indices[0], 'end_index': indices[-1]}
                    for name, indices in comb.index.groupby(comb['C0']).items()
                )
                index = pd.DataFrame(list(group_indices))
                """

                c = random.choice(group_names) # choose C0 randomly
                g = group_dict[c]

                start = 0
                end = g.shape[0]

                random_row_number = random.randint(start, end - 1)
                number_placement = list(g.loc[random_row_number])

                group_names.remove(c)
                for group_number in group_names: # group to remove rows from

                    for col_num in range(1, 9): # value to check
                        val = number_placement[col_num + 1]
                        temp = group_dict[group_number]
                        temp = temp[~(temp[cols[col_num]] == val)].reset_index(drop=True)
                        group_dict[group_number] = temp
                final_placements.append(number_placement[1:])

            print("SUCCESS!")
            break

        except Exception as e:
            print("ERROR ENCOUNTERED. RUNNING ALGORITHM AGAIN.")

    number = 1
    j = 0
    for placement in final_placements:
        for i in range(0,9):
            grid[placement[i] - 1][i] = number
        number += 1


    print("FINAL SOLVED GRID:\n")
    for i in grid:
        print(i)
