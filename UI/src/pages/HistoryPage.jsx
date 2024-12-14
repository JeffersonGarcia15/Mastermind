import { useState, useEffect } from "react";
import { getHistory } from "../utils/api";
import { GameHistory } from "../components/UserGame";

export function HistoryPage() {
    const [games, setGames] = useState([]);

    useEffect(() => {
        async function fetchData() {
            const { data, error } = await getHistory();
            if (data) {
                setGames(data || []);
            }
            else {
                console.log(error);
            }
        }
        fetchData();
    }, []);

    return (
        <div>
            <h2>Past Games</h2>
            <GameHistory games={games} />
        </div>
    );
}