import Piece from '../piece.js'

export default class Knight extends Piece {
  toString() {
    return this.color === 'white' ? '♘' : '♞'
  }
}
