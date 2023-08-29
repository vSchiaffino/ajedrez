import Piece from '../piece.js'

export default class Queen extends Piece {
  toString() {
    return this.color === 'white' ? '♕' : '♛'
  }
}
