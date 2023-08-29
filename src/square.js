export default class Square {
  constructor() {
    this.piece = null
  }

  setPiece(piece) {
    this.piece = piece
  }

  toString() {
    return this.piece ? this.piece.toString() : ' '
  }
}
