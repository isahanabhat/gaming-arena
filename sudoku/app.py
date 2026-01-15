from flask import Flask, request, render_template

import sudoku

app = Flask(__name__)

@app.route('/', methods=['GET'])
def test_app():
    sudoku_obj = sudoku.SudokuGenerator()
    grid = sudoku_obj.get_sudoku_grid()
    print(grid)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
