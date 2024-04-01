const { spawn } = require('child_process');

const electronProcess = spawn('npm', ['start']);

electronProcess.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

electronProcess.stderr.on('data', (data) => {
  console.error(`stderr: ${data}`);
});

electronProcess.on('close', (code) => {
  console.log(`child process exited with code ${code}`);
});

function startGame(gameType) {
    if (gameType === 'Game1') {
        window.location.href = 'game1.html';
    } else if (gameType === 'Game2') {
        window.location.href = 'game2.html';
    }
}

function Reselect() {
    window.location.href = 'gameselect.html'; 
}

function gotoMain() {
    window.location.href = 'main.html'; 
}