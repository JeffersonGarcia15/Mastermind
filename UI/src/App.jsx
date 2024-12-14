import { useState, useEffect } from "react";
import { Routes, Route, Link, useNavigate } from "react-router";
import { AuthPage, GameDetailsPage, GamePage, HistoryPage, HomePage, LeaderboardPage } from "./pages";
import { authenticate, logout } from "./utils/api";

export default function App() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

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

  async function handleLogout() {
    await logout();
    navigate("/");
    setUser(null);
    window.location.reload();
  }

  return (
    <div>
      <nav>
        <Link to="/">Home</Link> |
        {user ? (
          <>
            <button onClick={handleLogout} style={{ margin: "0 5px" }}>Logout</button>
            <Link to="/game">Game</Link> | {user && <Link to="/history">History</Link>} | <Link to="/leaderboard">Leaderboard</Link>
          </>
        ) : (
          <>
            <Link to="/auth">Login/Signup</Link> | <Link to="/game">Game</Link> | <Link to="/leaderboard">Leaderboard</Link>
          </>
        )}
      </nav>
      <Routes>
        <Route path="/auth" element={<AuthPage setUser={setUser} />} />
        <Route path="/game/:gameId" element={<GameDetailsPage />} />
        <Route path="/game" element={<GamePage user={user} />} />
        <Route path="/history" element={user ? <HistoryPage /> : <div>Please login to view history.</div>} />
        <Route path="/" element={<HomePage />} />
        <Route path="/leaderboard" element={<LeaderboardPage />} />
      </Routes>
    </div>
  );
}