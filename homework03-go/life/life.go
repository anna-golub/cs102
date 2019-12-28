package life

import (
	"fmt"
  "os"
  "strconv"
  "strings"
  "bufio"
	"math/rand"
)

type GameOfLife struct {
	rows, cols, generations, max_generations int
	prev_generation, curr_generation         [][]int
}

type Cell struct {
	row, col int
}

func newGame(rows int, cols int, randomize bool, max_generations int) GameOfLife {
	prev_generation := CreateGrid(rows, cols, false)
	curr_generation := CreateGrid(rows, cols, randomize)
	return GameOfLife{
		rows:            rows,
		cols:            cols,
		prev_generation: prev_generation,
		curr_generation: curr_generation,
		max_generations: max_generations,
		generations:     1,
	}
}

func CreateGrid(rows int, cols int, randomize bool) [][]int {
	grid := make([][]int, rows)

	for i := 0; i < rows; i++ {
		grid[i] = make([]int, cols)
		if randomize == true {
			for j := 0; j < cols; j++ {
				grid[i][j] = rand.Intn(2)
			}
		}
	}
	return grid
}

func (game GameOfLife) GetNeighbours(cell Cell) []int {
	row, col := cell.row, cell.col
	res := make([]int, 0)

	if row > 0 {
		res = append(res, game.curr_generation[row-1][col])
		if col > 0 {
			res = append(res, game.curr_generation[row-1][col-1])
		}
		if col < game.cols-1 {
			res = append(res, game.curr_generation[row-1][col+1])
		}
	}
	if row < game.rows-1 {
		res = append(res, game.curr_generation[row+1][col])
		if col > 0 {
			res = append(res, game.curr_generation[row+1][col-1])
		}
		if col < game.cols-1 {
			res = append(res, game.curr_generation[row+1][col+1])
		}
	}
	if col > 0 {
		res = append(res, game.curr_generation[row][col-1])
	}
	if col < game.cols-1 {
		res = append(res, game.curr_generation[row][col+1])
	}
	return res
}

func (game *GameOfLife) GetNextGeneration() [][]int {
	for i := 0; i < game.rows; i++ {
		for j := 0; j < game.cols; j++ {
			game.prev_generation[i][j] = game.curr_generation[i][j]
		}
	}

	alive := make([]Cell, 0)
	dead := make([]Cell, 0)
	for i := 0; i < game.rows; i++ {
		for j := 0; j < game.cols; j++ {
			neighbours := game.GetNeighbours(Cell{i, j})
			sum := 0
			for _, n := range neighbours {
				sum += n
			}

			if sum < 2 || sum > 3 {
				dead = append(dead, Cell{i, j})
			} else if sum == 3 && game.curr_generation[i][j] == 0 {
				alive = append(alive, Cell{i, j})
			}
		}
	}

	for _, a := range alive {
		game.curr_generation[a.row][a.col] = 1
	}
	for _, d := range dead {
		game.curr_generation[d.row][d.col] = 0
	}
	return game.curr_generation
}

func (game *GameOfLife) Step() {
	game.GetNextGeneration()
	game.generations++
}

func (game *GameOfLife) Is_Max_Generations_Exceeded() bool {
	return game.generations >= game.max_generations
}

func (game *GameOfLife) Is_Changing() bool {
	for i := 0; i < game.rows; i++ {
		for j := 0; j < game.cols; j++ {
			if game.curr_generation[i][j] != game.prev_generation[i][j] {
				return true
			}
		}
	}
	return false
}

func FromFile(filename string) GameOfLife {
  file, err := os.Open(filename) 
    if err != nil { 
      fmt.Println(err) 
      os.Exit(1)
    } 
  defer file.Close() 
  
  reader := bufio.NewReader(file)
  var grid [][]int

  for { 
    line, err := reader.ReadString('\n') 
    if err != nil {
      break
    }
    str_arr := strings.Split(strings.Trim(line, "\n"), "")
    var int_arr []int
    for _, str := range str_arr {
      temp, _ := strconv.ParseInt(str, 10, 64)
      int_arr = append(int_arr, int(temp))
    }
    grid = append(grid, int_arr)
  }

  game := newGame(len(grid), len(grid[0]), false, 1000)
  game.curr_generation = grid
  return game
}

func (game *GameOfLife) Save (filename string) {
  file, err := os.Create(filename) 
  writer := bufio.NewWriter(file) 
  if err != nil { 
    fmt.Println(err) 
    os.Exit(1) 
  } 
  defer file.Close() 
  
  for _, row := range game.curr_generation {
    var str_res string
    for _, v := range row {
      str_res += strconv.Itoa(v)
    }
    writer.WriteString(str_res + "\n")
  } 
  writer.Flush() 
}

func Main() {
	//game := FromFile("life/grid.txt")
	game := newGame(5, 5, true, 5)

	for i := 0; i < 4; i++ {
	  game.Step()
	  fmt.Println("generations =", game.generations)
	  fmt.Println("max_generations =", game.max_generations)
	  fmt.Println("exceeded =", game.Is_Max_Generations_Exceeded())
	  fmt.Println("changing =", game.Is_Changing())
	  fmt.Println(game.prev_generation)
	  fmt.Println()
	}
  game.Save("life/curr_gen.txt")
}
