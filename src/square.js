export default class Square {
  constructor(x, y) {
    this.piece = NullPiece()
    this.x = x
    this.y = y
  }

  getX() {
    return this.x
  }

  getY() {
    return this.y
  }

  setPiece(piece) {
    this.piece = piece
  }

  toString() {
    return this.piece.toString()
  }

  getPieceColor() {
    return this.piece.getColor()
  }

  containsAllyPiece(pieceColor) {
    return this.getPieceColor() === pieceColor
  }

  containsEnemyPiece(pieceColor) {
    return this.isOccupied() && this.getPieceColor() !== pieceColor
  }

  isOccupied() {
    return !this.piece.isNull()
  }

  getNotation() {
    const mapColumnNotation = {
      0: 'A',
      1: 'B',
      2: 'C',
      3: 'D',
      4: 'E',
      5: 'F',
      6: 'G',
      7: 'H',
    }

    return `${mapColumnNotation[this.x]}${this.y + 1}`
  }
}
