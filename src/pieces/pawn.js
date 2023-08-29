import Piece from '../piece.js'

export default class Pawn extends Piece {
  toString() {
    return this.color === 'white' ? '♙' : '♟'
  }
}
