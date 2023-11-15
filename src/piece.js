export class NullPiece {
  isNull() {
    return true
  }

  getColor() {
    return undefined
  }
}

export default class Piece {
  constructor(color, movements) {
    this.color = color
    this.movements = movements
  }

  isNull() {
    return false
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

  move(from, to) {
    console.log(`moving ${from.getNotation()} to ${to.getNotation()}`)
    // No se si va asi, lo puse por ahora
    from.setPiece(null)
    to.setPiece(this)
  }
}
