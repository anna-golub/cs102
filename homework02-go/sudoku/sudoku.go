package sudoku

import (
	"fmt"
	"io/ioutil"
	"math"
	"math/rand"
	"path/filepath"
)

func readSudoku(filename string) ([][]rune, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Println(err)
		return nil, err
	}
	grid := group(filter(data), 9)
	return grid, nil
}

func filter(values []byte) []rune {
	filtered_values := make([]rune, 0)
	for _, v := range values {
		if (rune(v) >= '1' && rune(v) <= '9') {
			filtered_values = append(filtered_values, rune(v - '0'))
		} else if rune(v) == '.' {
      filtered_values = append(filtered_values, rune(v))
    }
	}
	return filtered_values
}

func Display(grid [][]rune) {
	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid); j++ {
      if grid[i][j] == rune('.') {
        fmt.Print(".")
      } else {
			  fmt.Print(string(rune(grid[i][j] + '0')))
		  }
    }
		fmt.Println()
	}
}

func group(values []rune, n int) [][]rune {
	res := make([][]rune, len(values)/n)

	for i := 0; i < len(values); i += n {
		res[i/n] = make([]rune, n)
		temp := values[i : i+n]
		for j := 0; j < len(temp); j++ {
			res[i/n][j] = temp[j]
		}
	}
	return res
}

func getRow(grid [][]rune, row int) []rune {
	return grid[row]
}

func getCol(grid [][]rune, col int) []rune {
	res := make([]rune, len(grid))
	for i := 0; i < len(grid); i++ {
		res[i] = grid[i][col]
	}
	return res
}

func getBlock(grid [][]rune, row int, col int) []rune {
	row = (row / 3) * 3
	col = (col / 3) * 3
	res := make([]rune, 9)

	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			res[i*3+j] = grid[row+i][col+j]
		}
	}
	return res
}

func findEmptyPosition(grid [][]rune) (int, int) {
	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid); j++ {
			if grid[i][j] == rune('.') {
				return i, j
			}
		}
	}
	return -1, -1
}

func contains(values []rune, search rune) bool {
	for _, v := range values {
		if v == search {
			return true
		}
	}
	return false
}

func findPossibleValues(grid [][]rune, row int, col int) []rune {
	var check [10]bool
	temp := getRow(grid, row)
	for _, v := range temp {
		if v == rune('.') {
			continue
		}
		check[int(v)] = true
	}
	temp = getCol(grid, col)
	for _, v := range temp {
		if v == rune('.') {
			continue
		}
		check[int(v)] = true
	}
	temp = getBlock(grid, row, col)
	for _, v := range temp {
		if v == rune('.') {
			continue
		}
		check[int(v)] = true
	}

	var res []rune
	for n, v := range check {
		if n == 0 {
			continue
		}
		if v == false {
			res = append(res, rune(n))
		}
	}
	return res
}

func Solve(grid [][]rune) ([][]rune, bool) {
	row, col := findEmptyPosition(grid)
	if row == -1 {
		return grid, true
	}
	poss_values := findPossibleValues(grid, row, col)
	for _, v := range poss_values {
		grid[row][col] = v
		poss_solution, flag := Solve(grid)
		if flag {
			return poss_solution, true
		}
	}
	grid[row][col] = rune('.')
	return grid, false
}

func CheckSolution(grid [][]rune) bool {
	var row, col, block, temp []rune

	for i := 0; i < len(grid); i++ {
		row = getRow(grid, i)
		temp = make([]rune, 0)
		for _, n := range row {
			for _, t := range temp {
				if t == n {
					return false
				}
			}
			temp = append(temp, n)
		}
	}

	for i := 0; i < len(grid); i++ {
		col = getCol(grid, i)
		temp = make([]rune, 0)
		for _, n := range col {
			for _, t := range temp {
				if t == n {
					return false
				}
			}
			temp = append(temp, n)
		}
	}

	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			block = getBlock(grid, i*3, j*3)
			temp = make([]rune, 0)
			for _, n := range block {
				for _, t := range temp {
					if t == n {
						return false
					}
				}
				temp = append(temp, n)
			}
		}
	}
	return true
}

func GenerateSudoku(N int) [][]rune {
	N = 81 - int(math.Min(float64(N), 81))
	grid := make([][]rune, 9)

	for i := 0; i < 9; i++ {
		grid[i] = make([]rune, 9)
		for j := 0; j < 9; j++ {
			if 0 <= i && i < 3 {
				grid[i][j] = rune((i*3+j)%9 + 1)
			} else if 3 <= i && i < 6 {
				grid[i][j] = rune((3*(i%3)+1+j)%9 + 1)
			} else {
				grid[i][j] = rune((3*(i%3)+2+j)%9 + 1)
			}
		}
	}

	var temp rune
	for i := 0; i < 9; i++ {
		for j := i; j < 9; j++ {
			temp = grid[i][j]
			grid[i][j] = grid[j][i]
			grid[j][i] = temp
		}
	}

	row1, row2 := rand.Intn(2), rand.Intn(2)
	for j := 0; j < 9; j++ {
		temp = grid[row1][j]
		grid[row1][j] = grid[row2][j]
		grid[row2][j] = temp
	}
	col1, col2 := rand.Intn(2)+3, rand.Intn(2)+3
	for i := 0; i < 9; i++ {
		temp = grid[i][col1]
		grid[i][col1] = grid[i][col2]
		grid[i][col2] = temp
	}

	for N > 0 {
		row, col := rand.Intn(8), rand.Intn(8)
		if grid[row][col] != 0 {
			grid[row][col] = rune('.')
			N--
		}
	}
	return grid
}

func Main() {
	puzzles, err := filepath.Glob("main/puzzle1.txt")
	if err != nil {
		fmt.Printf("Could not find any puzzles")
		return
	}
	for _, fname := range puzzles {
		go func(fname string) {
			grid, _ := readSudoku(fname)
			Display(grid)
			solution, _ := Solve(grid)
			fmt.Println("Solution for", fname)
			Display(solution)
		}(fname)
	}
	var input string
	fmt.Scanln(&input)
}
