import Movement from '../src/movement/movement.js'
import Square from '../src/square.js'

describe('Movement', () => {
  describe('.canPerformMovement', () => {
    const movement = new Movement(1, 1)
    const square = new Square()
    it('should return false if squareToMove is undefined', () => {
      expect(movement.canPerformMovement(undefined, 'white')).toBe(false)
      expect(movement.canPerformMovement(undefined, 'black')).toBe(false)
    })

    it('should return false if squareToMove contains an ally piece', () => {
      square.setPiece({ getColor: () => 'white' })
      expect(movement.canPerformMovement(square, 'white')).toBe(false)

      square.setPiece({ getColor: () => 'black' })
      expect(movement.canPerformMovement(square, 'black')).toBe(false)
    })

    it('should return true if squareToMove contains an enemy piece', () => {
      square.setPiece({ getColor: () => 'white' })
      expect(movement.canPerformMovement(square, 'black')).toBe(true)

      square.setPiece({ getColor: () => 'black' })
      expect(movement.canPerformMovement(square, 'white')).toBe(true)
    })

    it('should return true if squareToMove does not contains a piece', () => {
      square.setPiece(null)
      expect(movement.canPerformMovement(square, 'black')).toBe(true)
      expect(movement.canPerformMovement(square, 'white')).toBe(true)
    })
  })
})
