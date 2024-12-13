import { useState, useEffect } from "react";
import { getLeaderboardByScore, getLeaderboardByGames } from "../utils/api";
import { Leaderboard } from "../components/Leaderboard";

export function LeaderboardPage() {
    const [mode, setMode] = useState("score");
    const [data, setData] = useState([]);

    useEffect(() => {
        async function fetchData() {
            let res;
            if (mode === "score") {
                res = await getLeaderboardByScore();
            } else {
                res = await getLeaderboardByGames();
            }
            setData(res.data || []);
        }
        fetchData();
    }, [mode]);

    return (
        <div>
            <button onClick={() => setMode("score")}>By Score</button>
            <button onClick={() => setMode("games")}>By Games</button>
            <Leaderboard data={data} />
        </div>
    );
}
