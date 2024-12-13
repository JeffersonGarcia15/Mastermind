import { useState, useEffect } from "react";
import { Routes, Route, Link } from "react-router";
import { AuthPage, GameDetailsPage, GamePage, HistoryPage, HomePage, LeaderboardPage } from "./pages";
import { authenticate } from "./utils/api";

export default function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    async function checkAuth() {
      try {
        const { data } = await authenticate();
        if (data) {
          setUser(data);
        }
      } catch (err) {
        console.log("User not authenticated", err);
      }
    }
    checkAuth();

  }, []);
  console.log("USER", user);
  return (
    <div>
      <nav>
        <Link to="/">Home</Link> | <Link to="/auth">Login/Signup</Link> | <Link to="/game">Game</Link> | <Link to="/history">History</Link> | <Link to="/leaderboard">Leaderboard</Link>
      </nav>
      <Routes>
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/game/:id" element={<GameDetailsPage />} />
        <Route path="/game" element={<GamePage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/" element={<HomePage />} />
        <Route path="/leaderboard" element={<LeaderboardPage />} />
      </Routes>
    </div>
  );
}
