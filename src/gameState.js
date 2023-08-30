/**
 * state can be = ['whiteToPlay', 'blackToPlay', 'whiteWins', 'blackWins', 'draw']
 */

export default class GameState {
  constructor() {
    this.state = 'whiteToPlay'
  }

  isOver() {
    return ['whiteWins', 'blackWins', 'draw'].includes(this.state)
  }

  changeTurn() {
    // TODO check if checkmate or draw
    const mapStateChange = {
      whiteToPlay: 'blackToPlay',
      blackToPlay: 'whiteToPlay',
    }
    this.state = mapStateChange[this.state]
  }
}
