import { DirectionalMovement } from '../movement/directionalMovement.js'
import Piece from '../piece.js'

export const rookMovements = [
  new DirectionalMovement(1, 0),
  new DirectionalMovement(-1, 0),
  new DirectionalMovement(0, 1),
  new DirectionalMovement(0, -1),
]

export default class Rook extends Piece {
  constructor(color) {
    super(color, rookMovements)
  }

  toString() {
    return this.color === 'white' ? '♖' : '♜'
  }
}
