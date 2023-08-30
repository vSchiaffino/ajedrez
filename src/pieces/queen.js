import Piece from '../piece.js'
import { bishopMovements } from './bishop.js'
import { rookMovements } from './rook.js'

export default class Queen extends Piece {
  constructor(color) {
    super(color, [...bishopMovements, ...rookMovements])
  }

  toString() {
    return this.color === 'black' ? '♕' : '♛'
  }
}
