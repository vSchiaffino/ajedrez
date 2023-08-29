import Movement from './movement.js'

export default class SingleMovement extends Movement {
  getPossibleNextSquares(board, actualSquare, pieceColor) {
    const possibleNextSquare = board.getSquareApplyingMovement(
      actualSquare,
      this.dx,
      this.dy,
    )
    return this.canPerformMovement(possibleNextSquare, pieceColor)
      ? [possibleNextSquare]
      : []
  }
}
