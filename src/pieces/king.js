import Piece from '../piece.js'

export default class King extends Piece {
  toString() {
    return this.color === 'white' ? '♔' : '♚'
  }
}
