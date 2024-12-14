/* eslint-disable react/prop-types */
import { HintCircles } from "../Game";

export function GameDetails({ game }) {
    return (
        <div>
            <h2>Game {game.game_id}</h2>
            <p>Score: {game.score === null ? "N/A" : game.score}</p>
            <p>Status: {game.status}</p>
            <p>Solution: {game.solution === null ? "Unknown" : game.solution}</p>
            <p>Difficulty: {game.difficulty}</p>
            <p>Started at: {game.created_at}</p>
            <h3>Attempts:</h3>
            <ul>
                {game.attempts.map((att, i) => {
                    const guessArray = att.guess.split("");
                    return (
                        <li key={i}>
                            Guess: {guessArray.join(", ")}{" "}
                            <HintCircles
                                correct_positions={att.correct_positions}
                                correct_numbers_only={att.correct_numbers_only}
                            />
                            <br />
                            Hints text: {att.hints}
                        </li>
                    );
                })}
            </ul>
        </div>
    );
}