import Board from './board.js'
import GameState from './gameState.js'

export default class Game {
  constructor() {
    this.board = new Board()
    this.state = new GameState()
  }

  move(fromNotation, toNotation) {
    if (this.isOver()) throw new Error('El juego ya termino')

    const fromSquare = this.board.getSquareByNotation(fromNotation)
    const toSquare = this.board.getSquareByNotation(toNotation)

    const piece = fromSquare.piece

    if (!piece) throw new Error('No hay pieza en la casilla de origen')
    const possibleToSquares = piece.getPossibleNextSquares(
      this.board,
      fromSquare,
      piece.color,
    )

    if (!possibleToSquares.includes(toSquare))
      throw new Error('Movimiento no valido')

    piece.move(fromSquare, toSquare)
    this.state.changeTurn()
  }

  isOver() {
    return this.state.isOver()
  }
}
