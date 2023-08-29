export default class Movement {
  constructor(dx, dy) {
    this.dx = dx
    this.dy = dy
  }

  getPossibleNextSquares(board, actualSquare, pieceColor) {
    return []
  }

  /**
   * Puede realizar el movimiento, si el casillero al que quiere ir no esta fuera de los limites
   * y no hay una pieza aliada
   */
  canPerformMovement(squareToMove, pieceColor) {
    return squareToMove !== undefined &&  !squareToMove.containsAllyPiece(pieceColor)
  }
}
