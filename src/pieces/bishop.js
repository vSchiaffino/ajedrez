import { DirectionalMovement } from '../movement/directionalMovement.js'
import Piece from '../piece.js'

export const bishopMovements = [
  new DirectionalMovement(1, 1),
  new DirectionalMovement(-1, 1),
  new DirectionalMovement(1, -1),
  new DirectionalMovement(-1, -1),
]

export default class Bishop extends Piece {
  constructor(color) {
    super(color, bishopMovements)
  }

  toString() {
    return this.color === 'black' ? '♗' : '♝'
  }
}
