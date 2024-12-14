import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router";
import { getGameDetails, makeGuess } from "../utils/api";
import { GameBoard } from "../components/Game/GameBoard";
import { HintCircles } from "../components/Game/HintCircles";

export function GameDetailsPage() {
    const { gameId } = useParams();
    const navigate = useNavigate();
    const [game, setGame] = useState(null);
    const [attempts, setAttempts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchData() {
            const { data, error } = await getGameDetails(gameId);
            if (data) {
                // Check if the game is completed
                if (data.status === "ongoing") {
                    alert("This game is still ongoing and cannot be viewed here.");
                    navigate("/");
                    return;
                }

                setGame({
                    game_id: data.game_id,
                    length: data.solution ? data.solution.length : 0,
                    is_sequence_locally_generated: data.is_sequence_locally_generated || false,
                    attempts_left: data.attempts_left || 0,
                    status: data.status,
                    score: data.score || 0,
                    solution: data.solution || null,
                });
                setAttempts(data.attempts || []);
                console.log("Game details fetched:", data);
            } else if (error) {
                console.error("Error fetching game details:", error);
                alert(`Error fetching game details: ${error}`);
            }
            setLoading(false);
        }
        fetchData();
    }, [gameId, navigate]);

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
                    score: guessResult.score || 0,
                };

                setAttempts((prevAttempts) => [...prevAttempts, newAttempt]);

                setGame((prevGame) => ({
                    ...prevGame,
                    attempts_left: guessResult.attempts_left,
                    status: guessResult.status,
                    score: guessResult.score || prevGame.score,
                    solution: guessResult.solution || prevGame.solution,
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

    if (loading) {
        return <div>Loading game details...</div>;
    }

    if (!game) {
        return <div>Game not found or an error occurred.</div>;
    }

    return (
        <div>
            <h2>Game ID: {game.game_id}</h2>
            <p>Status: {game.status}</p>
            <p>Attempts Left: {game.attempts_left}</p>
            {game.status === "ongoing" && (
                <GameBoard length={game.length} onSubmitGuess={handleGuess} />
            )}
            {game.status !== "ongoing" && (
                <div>
                    <h3>Game Over</h3>
                    {game.status === "win" && <p>Congratulations! You&apos;ve won!</p>}
                    {game.status === "lose" && <p>Sorry, you&apos;ve lost.</p>}
                    <p>Solution: {game.solution}</p>
                    <p>Your Score: {game.score}</p>
                </div>
            )}
            <h3>Previous Attempts:</h3>
            {attempts.length === 0 ? (
                <p>No attempts yet.</p>
            ) : (
                <ul style={{ listStyleType: "none", padding: 0 }}>
                    {attempts.map((att, index) => (
                        <li
                            key={index}
                            style={{
                                marginBottom: "15px",
                                border: "1px solid #ccc",
                                padding: "10px",
                                borderRadius: "5px",
                            }}
                        >
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
    );
}