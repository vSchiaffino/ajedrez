import SingleMovement from '../movement/singleMovement.js'
import Piece from '../piece.js'

export default class King extends Piece {
  constructor(color) {
    super(color, [
      new SingleMovement(1, 0),
      new SingleMovement(-1, 0),
      new SingleMovement(0, 1),
      new SingleMovement(0, -1),
      new SingleMovement(1, 1),
      new SingleMovement(-1, 1),
      new SingleMovement(1, -1),
      new SingleMovement(-1, -1),
    ])
  }

  toString() {
    return this.color === 'white' ? '♔' : '♚'
  }
}
