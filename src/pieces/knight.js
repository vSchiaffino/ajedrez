import Piece from '../piece.js'
import SingleMovement from '../movement/singleMovement.js'

export default class Knight extends Piece {
  constructor(color) {
    super(color, [
      new SingleMovement(2, 1),
      new SingleMovement(-2, 1),
      new SingleMovement(2, -1),
      new SingleMovement(-2, -1),
      new SingleMovement(1, 2),
      new SingleMovement(-1, 2),
      new SingleMovement(1, -2),
      new SingleMovement(-1, -2),
    ])
  }

  toString() {
    return this.color === 'black' ? '♘' : '♞'
  }
}
