import { useState, useEffect } from "react";
import { getLeaderboardByScore, getLeaderboardByGames } from "../utils/api";
import { Leaderboard } from "../components/Leaderboard";

export function LeaderboardPage() {
    const [mode, setMode] = useState("score"); // "score" or "games"
    const [data, setData] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                let response;
                if (mode === "score") {
                    response = await getLeaderboardByScore();
                } else {
                    response = await getLeaderboardByGames();
                }

                const { data, error } = response;

                if (error) {
                    setError(error);
                    setData([]);
                } else {
                    setData(data);
                    setError(null);
                }
            } catch (err) {
                setError("An unexpected error occurred.");
                setData([]);
                console.error(err);
            }
        }
        fetchData();
    }, [mode]);

    return (
        <div>
            <h1>Leaderboard</h1>
            <div style={{ marginBottom: "20px" }}>
                <button onClick={() => setMode("score")} disabled={mode === "score"}>
                    By Score
                </button>
                <button onClick={() => setMode("games")} disabled={mode === "games"}>
                    By Games
                </button>
            </div>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <Leaderboard data={data} mode={mode} />
        </div>
    );
}