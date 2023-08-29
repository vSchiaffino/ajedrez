import Piece from '../piece.js'

export default class Bishop extends Piece {
    toString(){
        return this.color === 'white' ? '♗' : '♝'
    }
}
