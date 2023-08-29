export default class Piece {
  constructor(color, movements) {
    this.color = color
    this.movements = movements
  }

  getPossibleNextSquares(board, actualSquare) {
    const squares = []
    for (const movement of this.movements) {
      squares.push(
        ...movement.getPossibleNextSquares(board, actualSquare, this.color),
      )
    }
    return squares
  }

  getColor() {
    return this.color
  }
}
