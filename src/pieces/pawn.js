import SingleMovementNoAttack from '../movement/singleMovementNoAttack.js'
import SingleMovementOnlyAttack from '../movement/singleMovementOnlyAttack.js'
import Piece from '../piece.js'

export default class Pawn extends Piece {
  constructor(color) {
    const dy = color === 'white' ? 1 : -1
    super(color, [
      new SingleMovementOnlyAttack(1, dy),
      new SingleMovementOnlyAttack(-1, dy),
      new SingleMovementNoAttack(0, dy),
      new SingleMovementNoAttack(0, 2 * dy), // movimiento doble, esta en la posicion i=3
    ])
  }

  move(from, to) {
    super.move(from, to)
    // Elimino el movimiento doble que esta en la posicion 3, porque si ya se movio no es valido
    this.movements = this.movements.filter((_, i) => i !== 3)
  }

  toString() {
    return this.color === 'white' ? '♙' : '♟'
  }
}
