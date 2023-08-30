import Game from '../game.js'

const table = document.getElementById('table')
const game = new Game()
const gameStateElement = document.getElementById('game-state')

let possibleMoves = []
let fromSelected = null

function renderBoard() {
  gameStateElement.innerHTML = game.state.state
  table.innerHTML = ''
  let i = 0
  for (const row of [...game.board.grid].reverse()) {
    const tr = document.createElement('tr')
    const td = document.createElement('td')
    td.innerHTML = 8 - (i % 8)
    tr.appendChild(td)
    for (const square of row) {
      const td = document.createElement('td')
      const colorClass = i % 2 === 0 ? 'white' : 'black'
      const nextMoveClass = possibleMoves.includes(square) ? 'next-move' : ''
      td.className = `${colorClass} ${nextMoveClass}`
      td.innerHTML = square.toString()
      td.onclick = () => onClickSquare(square)--
      tr.appendChild(td)
      i += 1
    }
    i += 1
    table.appendChild(tr)
  }
  const tr = document.createElement('tr')
  tr.appendChild(document.createElement('td'))
  for (const letter of ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']) {
    const td = document.createElement('td')
    td.innerHTML = letter
    tr.appendChild(td)
  }
  table.appendChild(tr)
}

function onClickSquare(square) {
  if (fromSelected === null) onClickFromSquare(square)
  else onClickToSquare(square)

  renderBoard()
}

function onClickFromSquare(square) {
  console.log(square.piece.getColor())
  if (square.piece === null || !game.state.isTurnOf(square.piece.getColor())) {
    fromSelected = null
    possibleMoves = []
    return
  } else {
    possibleMoves = square.piece.getPossibleNextSquares(game.board, square)
    if (possibleMoves.length === 0) return
    fromSelected = square
  }
}

function onClickToSquare(square) {
  if (possibleMoves.includes(square)) {
    game.move(fromSelected.getNotation(), square.getNotation())
    fromSelected = null
    possibleMoves = []
  } else {
    onClickFromSquare(square)
  }
}

renderBoard()
