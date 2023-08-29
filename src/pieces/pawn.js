import SingleMovement from '../movement/singleMovement.js'
import Piece from '../piece.js'

export default class Pawn extends Piece {
  constructor(color) {
    super(color, [new SingleMovement(0, 1), new SingleMovement(0, 2)])
  }

  toString() {
    return this.color === 'white' ? '♙' : '♟'
  }
}
