from flask import Flask, request, render_template

import sudoku

app = Flask(__name__)

@app.route('/', methods=['GET'])
def test_app():
    sudoku_obj = sudoku.SudokuGenerator()
    solved_grid = sudoku_obj.get_sudoku_grid()
    print(solved_grid)
    grid = sudoku_obj.remove_values("easy")
    print()
    print(grid)
    """
    input_data = []
    for i in range(9):
        for j in range(9):
            id_name = "v" + str(i) + str(j)
            element_value = grid[i][j]
            element_attributes = {
                'id' : id_name,
                'value' : element_value,
                'readonly': True
            }
            input_data.append(element_attributes)
    """

    return render_template('index.html', grid=grid)

if __name__ == "__main__":
    app.run(debug=True)
