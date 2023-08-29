import Piece from '../src/piece.js'
import Square from '../src/square.js'

describe('Square', () => {
  describe('.containsAllyPiece', () => {
    const square = new Square(0, 0)
    const whitePiece = new Piece('white', [])
    const blackPiece = new Piece('black', [])
    it('should return true if the square contains a piece of the same color', () => {
      square.setPiece(whitePiece)
      expect(square.containsAllyPiece('white')).toBe(true)

      square.setPiece(blackPiece)
      expect(square.containsAllyPiece('black')).toBe(true)
    })
    it('should return false in any other scenario', () => {
      square.setPiece(whitePiece)
      expect(square.containsAllyPiece('black')).toBe(false)

      square.setPiece(blackPiece)
      expect(square.containsAllyPiece('white')).toBe(false)

      square.setPiece(null)
      expect(square.containsAllyPiece('white')).toBe(false)
      expect(square.containsAllyPiece('black')).toBe(false)
    })
  })
})
