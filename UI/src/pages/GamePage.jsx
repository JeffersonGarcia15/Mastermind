/* eslint-disable react/prop-types */
import { useState, useEffect } from "react";
import { createGame, makeGuess, markGameAsLost } from "../utils/api";
import { GameBoard, HintCircles } from "../components/Game"; // Now it is letting me import from Game/index.jsx...

export function GamePage({ user }) {
    const [difficulty, setDifficulty] = useState("medium");
    const [game, setGame] = useState(null);
    const [attempts, setAttempts] = useState([]);
    const [ongoingGameId, setOngoingGameId] = useState(() => {
        const storedUserId = localStorage.getItem("ongoing_game_user_id");
        // Only restore if current user matches stored user ID. This is to avoid the bug of users playing other user's game when restoring a game
        if (user && storedUserId && storedUserId === String(user.id)) {
            return localStorage.getItem("ongoing_game_id");
        }
        return null;
    });
    const [createdByUser, setCreatedByUser] = useState(() => {
        const storedUserId = localStorage.getItem("ongoing_game_user_id");
        if (user && storedUserId && storedUserId === String(user.id)) {
            return localStorage.getItem("ongoing_game_created_by_user") === "true";
        }
        return false;
    });
    const [ongoingGameUserId, setOngoingGameUserId] = useState(() => {
        const storedUserId = localStorage.getItem("ongoing_game_user_id");
        if (user && storedUserId && storedUserId === String(user.id)) {
            return storedUserId;
        }
        return null;
    });

    useEffect(() => {
        if (user && ongoingGameId && !game && ongoingGameUserId && ongoingGameUserId === String(user.id)) {
            const shouldResume = window.confirm("You have an ongoing game. Resume?");
            if (shouldResume) {
                if (createdByUser && !user) {
                    alert("Cannot resume a user-associated game while logged out.");
                    markGameAsLost(ongoingGameId);
                    localStorage.removeItem("ongoing_game_id");
                    localStorage.removeItem("ongoing_game_difficulty");
                    localStorage.removeItem("ongoing_game_attempts");
                    localStorage.removeItem("ongoing_game_attempts_left");
                    localStorage.removeItem("ongoing_game_created_by_user");
                    localStorage.removeItem("ongoing_game_user_id");
                    setOngoingGameId(null);
                    setCreatedByUser(false);
                    setOngoingGameUserId(null);
                } else {
                    const savedDifficulty = localStorage.getItem("ongoing_game_difficulty") || "medium";
                    const savedAttempts = JSON.parse(localStorage.getItem("ongoing_game_attempts") || "[]");
                    const savedAttemptsLeft = parseInt(localStorage.getItem("ongoing_game_attempts_left") || "10", 10);
                    const savedLength = (savedDifficulty === "medium") ? 4 : 6;
                    setDifficulty(savedDifficulty);
                    setGame({
                        game_id: ongoingGameId,
                        length: savedLength,
                        is_sequence_locally_generated: true,
                        attempts_left: savedAttemptsLeft,
                        status: "ongoing"
                    });
                    setAttempts(savedAttempts);
                }
            } else {
                if (createdByUser) {
                    markGameAsLost(ongoingGameId);
                }
                localStorage.removeItem("ongoing_game_id");
                localStorage.removeItem("ongoing_game_difficulty");
                localStorage.removeItem("ongoing_game_attempts");
                localStorage.removeItem("ongoing_game_attempts_left");
                localStorage.removeItem("ongoing_game_created_by_user");
                localStorage.removeItem("ongoing_game_user_id");
                setOngoingGameId(null);
                setCreatedByUser(false);
                setOngoingGameUserId(null);
            }
        }
    }, [ongoingGameId, game, user, createdByUser, ongoingGameUserId]);

    async function startGame() {
        try {
            const { data, error } = await createGame(difficulty);
            if (data) {
                setGame({
                    game_id: data.game_id,
                    length: data.length,
                    is_sequence_locally_generated: data.is_sequence_locally_generated,
                    attempts_left: 10,
                    status: "ongoing"
                });
                setAttempts([]);
                if (user) {
                    localStorage.setItem("ongoing_game_id", data.game_id);
                    localStorage.setItem("ongoing_game_difficulty", difficulty);
                    localStorage.setItem("ongoing_game_attempts", JSON.stringify([]));
                    localStorage.setItem("ongoing_game_attempts_left", "10");
                    localStorage.setItem("ongoing_game_created_by_user", "true");
                    localStorage.setItem("ongoing_game_user_id", String(user.id));
                    setOngoingGameId(data.game_id);
                    setCreatedByUser(true);
                    setOngoingGameUserId(String(user.id));
                } else {
                    // Do not store any game if not logged in
                    setOngoingGameId(null);
                    setCreatedByUser(false);
                    setOngoingGameUserId(null);
                }
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

        if (guessString.length !== game.length) {
            alert(`You must enter exactly ${game.length} digits before guessing.`);
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

                const updatedAttempts = [...attempts, newAttempt];
                setAttempts(updatedAttempts);

                const updatedGame = {
                    ...game,
                    attempts_left: guessResult.attempts_left,
                    status: guessResult.status,
                    score: guessResult.score || game.score
                };
                setGame(updatedGame);

                if (user) {
                    localStorage.setItem("ongoing_game_attempts", JSON.stringify(updatedAttempts));
                    localStorage.setItem("ongoing_game_attempts_left", guessResult.attempts_left.toString());
                }

                console.log("Guess made:", guessResult);

                if (guessResult.status !== "ongoing") {
                    alert(`Game ended: ${guessResult.status}${guessResult.score ? `, Score: ${guessResult.score}` : ""}`);
                    localStorage.removeItem("ongoing_game_id");
                    localStorage.removeItem("ongoing_game_difficulty");
                    localStorage.removeItem("ongoing_game_attempts");
                    localStorage.removeItem("ongoing_game_attempts_left");
                    localStorage.removeItem("ongoing_game_created_by_user");
                    localStorage.removeItem("ongoing_game_user_id");
                    setOngoingGameId(null);
                    setCreatedByUser(false);
                    setOngoingGameUserId(null);
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

    async function startNewGameAfterEnd() {
        setGame(null);
        setAttempts([]);
    }

    return (
        <div>
            {!game && (
                <div>
                    <h2>Start a New Game</h2>
                    {!user && <p>You are not logged in. You can still play but your results won&apos;t be saved under an account.</p>}
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
                    {game.status !== "ongoing" && (
                        <div>
                            <button onClick={startNewGameAfterEnd}>Start Another Game</button>
                        </div>
                    )}
                    {game.status === "ongoing" && (
                        <GameBoard length={game.length} onSubmitGuess={handleGuess} />
                    )}
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
