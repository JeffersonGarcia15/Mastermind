/* eslint-disable react/prop-types */
import { Link } from "react-router";

export function GameHistory({ games }) {
    // Filter out games that are ongoing or have a null score
    const completedGames = games.filter(
        (g) => g.status !== "ongoing" && g.score !== null
    );

    return (
        <ul>
            {completedGames.length === 0 ? (
                <p>No completed games to display.</p>
            ) : (
                completedGames.map((g) => (
                    <li key={g.game_id} style={{ marginBottom: "10px" }}>
                        <Link to={`/game/${g.game_id}`}>
                            <strong>Game ID:</strong> {g.game_id} - <strong>Status:</strong> {g.status} - <strong>Score:</strong> {g.score}
                        </Link>
                        <br />
                        <strong>Difficulty:</strong> {g.difficulty}, <strong>Started:</strong> {new Date(g.created_at).toLocaleString()}
                    </li>
                ))
            )}
        </ul>
    );
}