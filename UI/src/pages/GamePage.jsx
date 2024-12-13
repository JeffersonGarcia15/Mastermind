import { useState } from "react";
import { createGame, makeGuess } from "../utils/api";
import { GameBoard } from "../components/Game/GameBoard";
import { HintCircles } from "../components/Game/HintCircles"; // Ensure correct import path

export function GamePage() {
    const [difficulty, setDifficulty] = useState("medium");
    const [game, setGame] = useState(null);
    const [attempts, setAttempts] = useState([]);

    async function startGame() {
        try {
            const { data, error } = await createGame(difficulty);
            if (data) {
                setGame({
                    game_id: data.game_id,
                    length: data.length,
                    is_sequence_locally_generated: data.is_sequence_locally_generated,
                    attempts_left: 10
                });
                setAttempts([]);
                console.log("Game started:", data);
            } else if (error) {
                console.error("Error starting game:", error);
                alert(`Error starting game: ${error}`);
            }
        } catch (err) {
            console.error("Unexpected error:", err);
            alert(`Unexpected error: ${err.message}`);
        }
    }

    async function handleGuess(guessString) {
        if (!game) {
            console.warn("No active game found.");
            return;
        }

        try {
            const { data, error } = await makeGuess(game.game_id, guessString);
            if (data) {
                const guessResult = data;
                const newAttempt = {
                    guess: guessString,
                    correct_positions: guessResult.correct_positions,
                    correct_numbers_only: guessResult.correct_numbers_only,
                    status: guessResult.status,
                    score: guessResult.score || 0
                };

                setAttempts(prevAttempts => [...prevAttempts, newAttempt]);

                setGame(prevGame => ({
                    ...prevGame,
                    attempts_left: guessResult.attempts_left
                }));

                console.log("Guess made:", guessResult);

                if (guessResult.status !== "ongoing") {
                    alert(`Game ended: ${guessResult.status}${guessResult.score ? `, Score: ${guessResult.score}` : ""}`);
                }
            } else if (error) {
                console.error("Error making guess:", error);
                alert(`Error making guess: ${error}`);
            }
        } catch (err) {
            console.error("Unexpected error:", err);
            alert(`Unexpected error: ${err.message}`);
        }
    }

    return (
        <div>
            {!game && (
                <div>
                    <h2>Start a New Game</h2>
                    <label>
                        Difficulty:
                        <select value={difficulty} onChange={e => setDifficulty(e.target.value)}>
                            <option value="medium">Medium (4 digits)</option>
                            <option value="hard">Hard (6 digits)</option>
                        </select>
                    </label>
                    <button onClick={startGame}>Start Game</button>
                </div>
            )}
            {game && (
                <div>
                    <h2>Game ID: {game.game_id}</h2>
                    <p>Attempts Left: {game.attempts_left}</p>
                    <GameBoard length={game.length} onSubmitGuess={handleGuess} />
                    <h3>Previous Attempts:</h3>
                    {attempts.length === 0 ? (
                        <p>No attempts yet.</p>
                    ) : (
                        <ul style={{ listStyleType: "none", padding: 0 }}>
                            {attempts.map((att, index) => (
                                <li key={index} style={{ marginBottom: "15px", border: "1px solid #ccc", padding: "10px", borderRadius: "5px" }}>
                                    <div>
                                        <strong>Guess {index + 1}: {att.guess}</strong>
                                    </div>
                                    <HintCircles
                                        correct_positions={att.correct_positions}
                                        correct_numbers_only={att.correct_numbers_only}
                                        total={game.length}
                                    />
                                    <div>Status: {att.status}{att.score ? `, Score: ${att.score}` : ""}</div>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            )}
        </div>
    );
}
