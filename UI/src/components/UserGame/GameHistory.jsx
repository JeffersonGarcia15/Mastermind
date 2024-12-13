/* eslint-disable react/prop-types */
import { Link } from "react-router-dom";

export function GameHistory({ games }) {
    return (
        <ul>
            {games.map(g => (
                <li key={g.id}>
                    <Link to={`/game/${g.id}`}>Game {g.id} - Score: {g.score}</Link>
                </li>
            ))}
        </ul>
    );
}
