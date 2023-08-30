import Movement from './movement.js'

export class DirectionalMovement extends Movement {
  getPossibleNextSquares(board, actualSquare, pieceColor) {
    const possibleNextSquares = []
    let movingSquare = actualSquare
    let stopMovement = false
    while (!stopMovement) {
      const nextSquare = board.getSquareApplyingMovement(
        movingSquare,
        this.dx,
        this.dy,
      )
      // Necesito parar el movimiento si me fui de los limites o si hay una pieza en el medio
      stopMovement = nextSquare === undefined || nextSquare.isOccupied()

      // Hay q omitir este if, se puede hacer al final con filter a possibleNextSquares
      if (this.canPerformMovement(nextSquare, pieceColor))
        possibleNextSquares.push(nextSquare)

      movingSquare = nextSquare
    }

    return possibleNextSquares
  }
}
