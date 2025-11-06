// Flag to prevent auto-save when user intentionally exits
let isIntentionalExit = false;

function saveGameState() {
    const gameState = {
        difficulty: difficultyChosen.innerText.toUpperCase(),
        currentTime: current_time,
        mistakes: parseInt(document.getElementById("mistakes").getElementsByClassName("coloured-text")[0].innerText),
        hintsUsed: usedHints,
        cellStates: []
    };

    // Save state of only user-modifiable cells (not given/locked cells)
    const cells = document.querySelectorAll('.grid-item');
    cells.forEach((cell, index) => {
        const isFilled = cell.classList.contains('filled');
        const isUnfilled = cell.classList.contains('unfilled');
        
        // Only save cells that are user-modifiable (have filled or unfilled class)
        // Given cells don't have these classes, so they're skipped
        if (isFilled || isUnfilled) {
            const value = isFilled ? cell.innerText : '';
            const color = cell.style.color;
            
            gameState.cellStates.push({
                index: index,
                value: value,
                isFilled: isFilled,
                isUnfilled: isUnfilled,
                color: color
            });
        }
    });

    // Save to sessionStorage
    sessionStorage.setItem('sudokuGameState', JSON.stringify(gameState));
}

function restoreGameState() {
    const savedState = sessionStorage.getItem('sudokuGameState');
    
    if (!savedState) {
        return false;
    }

    try {
        const gameState = JSON.parse(savedState);
        
        // Check if the saved difficulty matches current difficulty
        if (gameState.difficulty !== difficultyChosen.innerText.toUpperCase()) {
            // Different difficulty, clear saved state
            sessionStorage.removeItem('sudokuGameState');
            return false;
        }

        // Restore timer
        current_time = gameState.currentTime;
        updateTime(current_time - 1); // Update display

        // Restore mistakes
        const mistakesDisplay = document.getElementById("mistakes").getElementsByClassName("coloured-text")[0];
        mistakesDisplay.innerText = gameState.mistakes;

        // Restore hints used
        usedHints = gameState.hintsUsed;
        const hintsUsedIdentifier = document.getElementById("h-u-span");
        hintsUsedIdentifier.innerText = `${usedHints}`;

        // Restore cell states (only user-modified cells)
        const cells = document.querySelectorAll('.grid-item');
        gameState.cellStates.forEach((cellState) => {
            const cell = cells[cellState.index];
            
            // Only restore if the cell is user-modifiable (has filled or unfilled class)
            if (cell.classList.contains('filled') || cell.classList.contains('unfilled')) {
                if (cellState.isFilled) {
                    cell.classList.remove('unfilled');
                    cell.classList.add('filled');
                    cell.innerText = cellState.value;
                    cell.style.color = cellState.color;
                } else if (cellState.isUnfilled) {
                    cell.classList.remove('filled');
                    cell.classList.add('unfilled');
                    // Clear any user-entered value
                    if (cell.innerText !== cell.getAttribute('data-solution')) {
                        // Reset to solution (hidden)
                    }
                }
            }
        });

        // Update number buttons availability
        for (let i = 1; i < 10; i++) {
            checkNumCompletion(i.toString());
        }

        return true;
    } catch (error) {
        console.error('Error restoring game state:', error);
        sessionStorage.removeItem('sudokuGameState');
        return false;
    }
}

// Auto-save game state periodically (every 5 seconds)
let autoSaveInterval;

function startAutoSave() {
    autoSaveInterval = setInterval(() => {
        if (!paused) {
            saveGameState();
        }
    }, 5000);
}

function stopAutoSave() {
    if (autoSaveInterval) {
        clearInterval(autoSaveInterval);
    }
}

// Save on significant actions
function saveOnAction() {
    saveGameState();
}

// Clear game state from storage
function clearGameState() {
    isIntentionalExit = true;
    sessionStorage.removeItem('sudokuGameState');
    console.log('Game state cleared');
}

// Initialize state management when page loads
window.addEventListener('DOMContentLoaded', function() {
    // Try to restore previous state
    const restored = restoreGameState();
    
    if (restored) {
        console.log('Game state restored from previous session');
    }
    
    // Start auto-save
    startAutoSave();
});

// Save state before page unload (only if not intentionally exiting)
window.addEventListener('beforeunload', function() {
    if (!isIntentionalExit) {
        saveGameState();
    }
});
