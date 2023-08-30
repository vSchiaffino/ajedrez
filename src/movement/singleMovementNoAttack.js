import SingleMovement from './singleMovement.js'

export default class SingleMovementNoAttack extends SingleMovement {
  canPerformMovement(square, pieceColor) {
    return square != undefined && !square.isOccupied()
  }
}
