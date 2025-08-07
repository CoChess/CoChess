document.addEventListener("DOMContentLoaded", () => {
    const board = document.getElementById('chessboard');
    const gameId = document.body.dataset.gameId;

    // Oculta mensagens flash se existirem
    const flash = document.querySelector('.flash-messages');
    if (flash) {
        setTimeout(() => {
            flash.style.display = 'none';
        }, 4000);
    }

    if (board) {
        createBoard(board, gameId);
    }
});

const pieces = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
};

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

let selectedSquare = null;

function createBoard(board, gameId) {
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.classList.add('square');
            square.classList.add((row + col) % 2 === 0 ? 'white' : 'black');
            square.dataset.row = row;
            square.dataset.col = col;

            const piece = initialBoard[row * 8 + col];
            if (piece) square.textContent = pieces[piece];

            square.addEventListener('click', () => handleClick(square, board, gameId));
            board.appendChild(square);
        }
    }
}

function handleClick(square, board, gameId) {
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

        if (gameId) {
            fetch("/move", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    game_id: gameId,
                    from: [fromRow, fromCol],
                    to: [toRow, toCol],
                    piece: piece.toLowerCase()
                })
            });
        }

    } else if (square.textContent !== '') {
        selectedSquare = square;
        square.classList.add('selected');
    }
}
