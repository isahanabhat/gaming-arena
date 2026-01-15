import random
import pandas as pd

class SudokuGenerator:
    def __init__(self):
        self.grid = [[0] * 9 for _ in range(9)]
        self.final_placements = []
        self.file = r"../input/sudoku_combinations.csv"

    def is_safe(self, mat, row, col):

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
    def place_queen(self, row, mat, result):
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
            if self.is_safe(mat, row, i):
                mat[row][i] = 1
                self.place_queen(row + 1, mat, result)

                # backtrack
                mat[row][i] = 0

    def n_queen(self, n):
        # Initialize the board
        mat = [[0] * n for _ in range(n)]
        result = []

        # Place queens
        self.place_queen(0, mat, result)

        return result

    def get_combinations(self):
        n = 9
        result = self.n_queen(n)
        comb = pd.DataFrame(result, columns=["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"])
        comb.to_csv(self.file, index=False)


    def get_sudoku_grid(self, verbose=0):
        while True:
            try:
                cols = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"]
                comb = pd.read_csv(self.file)
                sudoku_groups = comb.groupby("C0")
                group_names = list(sudoku_groups.groups.keys())

                # groups dict
                group_dict = {}
                for name, group in sudoku_groups:
                    group_dict[name] = group.reset_index()

                self.final_placements = []

                for i in range(1, 10):
                    # print("===== ITERATION ", i, "=====")
                    """
                    group_indices = (
                        {'group': name, 'start_index': indices[0], 'end_index': indices[-1]}
                        for name, indices in comb.index.groupby(comb['C0']).items()
                    )
                    index = pd.DataFrame(list(group_indices))
                    """

                    c = random.choice(group_names)  # choose C0 randomly
                    g = group_dict[c]

                    start = 0
                    end = g.shape[0]

                    random_row_number = random.randint(start, end - 1)
                    number_placement = list(g.loc[random_row_number])

                    group_names.remove(c)
                    for group_number in group_names:  # group to remove rows from

                        for col_num in range(1, 9):  # value to check
                            val = number_placement[col_num + 1]
                            temp = group_dict[group_number]
                            temp = temp[~(temp[cols[col_num]] == val)].reset_index(drop=True)
                            group_dict[group_number] = temp
                    self.final_placements.append(number_placement[1:])

                print("SUCCESS!")
                break

            except Exception as e:
                print("ERROR ENCOUNTERED. RUNNING ALGORITHM AGAIN.", e)
                print("\n-----------------------------------------------------------------------------\n")

        number = 1
        for placement in self.final_placements:
            for i in range(0, 9):
                self.grid[placement[i] - 1][i] = number
            number += 1

        if verbose == 1:
            print("FINAL SOLVED GRID:\n")
            for i in self.grid:
                print(i)

        return self.grid


if __name__ == "__main__":
    print()

    s = SudokuGenerator()
    s.get_sudoku_grid(verbose=1)
