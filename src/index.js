import Game from './game.js'
import readline from 'readline-sync'

const game = new Game()

let respuesta = ''
let tablero = game.board.toString()

function getAction() {
  tablero = game.board.toString()
  console.clear()
  console.log(`El tablero es: (${game.state.state})`)
  console.log(tablero)
  console.log(respuesta)
  const action = readline.keyIn(
    'Que queres hacer? (1: Mover, 2: Ver movimientos, 3: Salir): ',
  )
  return action
}

function handleMove() {
  const from = readline.question(
    'Donde esta la pieza que queres mover (EJ: "E2"): ',
  )
  const square = game.board.getSquareByNotation(from)
  const piece = square.piece
  if (!piece) return
  const moves = piece.getPossibleNextSquares(game.board, square, piece.color)
  const movesStr = moves.map((square) => square.getNotation()).join(', ')

  const to = readline.question(
    `Adonde la queres mover? (posibles: ${movesStr}): `,
  )

  game.move(from, to)
}

function HandleSeeMoves() {
  const name = readline.question(
    'Donde esta la pieza que queres mover (EJ: "E2"): ',
  )
  const square = game.board.getSquareByNotation(name)
  const piece = square.piece
  if (!piece) return
  const moves = piece.getPossibleNextSquares(game.board, square, piece.color)
  const movesStr = moves.map((square) => square.getNotation()).join(', ')
  respuesta = `Los movimientos posibles desde ${name} son: ${movesStr}`
}

while (!game.isOver()) {
  const action = getAction()
  const mapActionWithHandler = {
    1: handleMove,
    2: HandleSeeMoves,
    3: process.exit,
  }
  mapActionWithHandler[action]()
}
