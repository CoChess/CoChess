const pieces = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
};

// Tabuleiro inicial (FEN simplificado)
const initialBoard = [
    'r','n','b','q','k','b','n','r',
    'p','p','p','p','p','p','p','p',
    '','','','','','','','',
    '','','','','','','','',
    '','','','','','','','',
    '','','','','','','','',
    'P','P','P','P','P','P','P','P',
    'R','N','B','Q','K','B','N','R'
];

const board = document.getElementById('chessboard');

function createBoard() {
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.classList.add('square');
            square.classList.add((row + col) % 2 === 0 ? 'white' : 'black');
            square.dataset.row = row;
            square.dataset.col = col;

            const piece = initialBoard[row * 8 + col];
            if (piece) square.textContent = pieces[piece];

            square.addEventListener('click', () => handleClick(square));
            board.appendChild(square);
        }
    }
}

let selectedSquare = null;

function handleClick(square) {
    if (selectedSquare) {
        selectedSquare.classList.remove('selected');
        const fromRow = parseInt(selectedSquare.dataset.row);
        const fromCol = parseInt(selectedSquare.dataset.col);
        const toRow = parseInt(square.dataset.row);
        const toCol = parseInt(square.dataset.col);
        const piece = selectedSquare.textContent;

        square.textContent = piece;
        selectedSquare.textContent = '';
        selectedSquare = null;

        fetch("/move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                game_id: gameId,
                from: [fromRow, fromCol],
                to: [toRow, toCol],
                piece: piece.toLowerCase()
            })
        }).then(res => {
            if (!res.ok) alert("Movimento inválido!");
        });

    } else if (square.textContent !== '') {
        selectedSquare = square;
        square.classList.add('selected');
    }
}

createBoard();
