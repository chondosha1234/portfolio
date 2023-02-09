
const statusDisplay = document.querySelector('.game-status');
const playerData = document.querySelector('.player-names');

let gameActive = true;
let gameState = ["", "", "", "", "", "", "", "", ""];

const winningConditions = [
  [0,1,2],
  [3,4,5],
  [6,7,8],
  [0,3,6],
  [1,4,7],
  [2,5,8],
  [0,4,8],
  [2,4,6]
];

let playerx = {
  "name": playerData.getAttribute('data-playerx'),
  "team": "X"
};
let playero = {
  "name": playerData.getAttribute('data-playero'),
  "team": "O"
};

let currentPlayer = playerx;



function winningMessage() {
  return `Player ${currentPlayer.name} has won!`;
}

function drawMessage() {
  return `Game ended in a draw!`;
}

function currentPlayerTurn() {
  return `It is ${currentPlayer.name}'s turn!`;
}

statusDisplay.innerHTML = currentPlayerTurn();


function playCell(clickedCell, clickedCellIndex) {
  gameState[clickedCellIndex] = currentPlayer.team;
  clickedCell.innerHTML = currentPlayer.team;
}


function changePlayer() {
  if (currentPlayer.team === "X"){
    currentPlayer = playero;
  }else{
    currentPlayer = playerx;
  }
  statusDisplay.innerHTML = currentPlayerTurn();
}


function validateResult(){
  let gameOver = false;
  for (let i = 0; i <= 7; i++){
    const condition = winningConditions[i];
    let a = gameState[condition[0]];
    let b = gameState[condition[1]];
    let c = gameState[condition[2]];

    if (a === "" || b === "" || c === ""){
      continue;
    }
    if (a === b && b === c){
      gameOver = true;
      break;
    }
  }

  if (gameOver){
    statusDisplay.innerHTML = winningMessage();
    gameActive = false;
    return;
  }

  const draw = !gameState.includes("");
  if (draw){
    statusDisplay.innerHTML = drawMessage();
    gameActive = false;
    return
  }
  changePlayer();
}


function clickCell(cellEvent) {
  const clickedCell = cellEvent.target;
  const cellIndex = parseInt(clickedCell.getAttribute('data-cell-index'));

  if (gameState[cellIndex] !== "" || !gameActive) return;

  playCell(clickedCell, cellIndex);
  validateResult();
}

function restartGame() {
  gameActive = true;
  currentPlayer = playerx;
  gameState = ["", "", "", "", "", "", "", "", ""];
  statusDisplay.innerHTML = currentPlayerTurn();
  document.querySelectorAll('.cell').forEach(cell => cell.innerHTML = "");
}

document.querySelectorAll('.cell').forEach(cell => cell.addEventListener('click', clickCell));
document.querySelector('.restart-btn').addEventListener('click', restartGame);
