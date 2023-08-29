import Square from './square.js'
import { Bishop, King, Knight, Pawn, Queen, Rook } from './pieces/index.js'

export default class Board extends Object {
  constructor() {
    super()
    this.grid = this.createEmptyGrid()
    this.spawnPieces()
  }

  /**
   * Crea un array de 8x8 con un objeto casilla en cada posición
   */
  createEmptyGrid() {
    return Array.from({ length: 8 }, (_, y) =>
      Array.from({ length: 8 }, (_, x) => new Square(x, y)),
    )
  }

  /**
   * Crea todas las piezas y las asigna a su posición inicial
   */
  spawnPieces() {
    // Peones
    const whitePawnsRow = this.grid[1]
    const blackPawnsRow = this.grid[6]
    whitePawnsRow.forEach((square) => square.setPiece(new Pawn('white')))
    blackPawnsRow.forEach((square) => square.setPiece(new Pawn('black')))
    // Torres
    const columnsWithRooks = [0, 7]
    columnsWithRooks.forEach((colIndex) => {
      this.grid[0][colIndex].setPiece(new Rook('white'))
      this.grid[7][colIndex].setPiece(new Rook('black'))
    })
    // Caballos
    const columnsWithKnights = [1, 6]
    columnsWithKnights.forEach((colIndex) => {
      this.grid[0][colIndex].setPiece(new Knight('white'))
      this.grid[7][colIndex].setPiece(new Knight('black'))
    })
    // Alfiles
    const columnsWithBishops = [2, 5]
    columnsWithBishops.forEach((colIndex) => {
      this.grid[0][colIndex].setPiece(new Bishop('white'))
      this.grid[7][colIndex].setPiece(new Bishop('black'))
    })
    // Reinas
    this.grid[0][3].setPiece(new Queen('white'))
    this.grid[7][3].setPiece(new Queen('black'))
    // Reyes
    this.grid[0][4].setPiece(new King('white'))
    this.grid[7][4].setPiece(new King('black'))
  }

  toString() {
    const columnLabels = 'ABCDEFGH'

    return [...this.grid]
      .reverse()
      .map(
        (row, rowIndex) =>
          `${8 - rowIndex} ${row.map((square) => square.toString()).join(' ')}`,
      )
      .join('\n')
      .concat(`\n  ${columnLabels.split('').join(' ')}`)
  }

  /**
   * Devuelve un square, moviendolo dx lugares en x y dy lugares en y
   * en caso de que se vaya de los limites del tablero, devuelve undefined
   */
  getSquareApplyingMovement(initialSquare, dx, dy) {
    const [x, y] = [initialSquare.getX(), initialSquare.getY()]

    const row = this.grid[y + dy]

    return row === undefined ? undefined : row[x + dx]
  }

  getPieceIn(squareNotation) {
    const mapColumnNotation = {
      A: 0,
      B: 1,
      C: 2,
      D: 3,
      E: 4,
      F: 5,
      G: 6,
      H: 7,
    }
    const row = Number(squareNotation[1]) - 1
    const column = mapColumnNotation[squareNotation[0]]
    return this.grid[row][column].piece
  }
}

const board = new Board()

board.grid[2][0].setPiece(new Pawn('black'))
board.grid[2][2].setPiece(new Pawn('black'))
console.log(board.toString())
const knight = board.getPieceIn('B1')

const possibleSquares = knight.getPossibleNextSquares(board, board.grid[0][1])
console.log(possibleSquares.map((square) => square.getNotation()))
