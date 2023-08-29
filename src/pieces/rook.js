import Piece from '../piece.js'

export default class Rook extends Piece {
  toString() {
    return this.color === 'white' ? '♖' : '♜'
  }
}
