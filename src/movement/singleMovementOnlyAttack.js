import SingleMovement from './singleMovement.js'

export default class SingleMovementOnlyAttack extends SingleMovement {
  /**
   * Puede realizar el movimiento, si el casillero al que quiere ir no esta fuera de los limites
   * y además contiene una pieza enemiga
   */
  canPerformMovement(square, pieceColor) {
    return square != undefined && square.containsEnemyPiece(pieceColor)
  }
}
