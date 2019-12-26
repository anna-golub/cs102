package main

import (
	"fmt"
	"main/sudoku"
)

func main() {
	grid := sudoku.GenerateSudoku(50)
  sudoku.Display(grid)
  fmt.Println()

	solution, flag := sudoku.Solve(grid)
	if flag == true {
		sudoku.Display(solution)
		fmt.Println(sudoku.CheckSolution(solution))
	} else {
		print("no solution found")
	}

  sudoku.Main()
}
