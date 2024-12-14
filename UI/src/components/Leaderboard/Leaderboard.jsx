import PropTypes from "prop-types";

export function Leaderboard({ data, mode }) {
    return (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
                <tr>
                    <th style={thStyle}>Ranking</th>
                    <th style={thStyle}>Name</th>
                    <th style={thStyle}>{mode === "score" ? "Score" : "Games"}</th>
                </tr>
            </thead>
            <tbody>
                {data.length === 0 ? (
                    <tr>
                        <td colSpan="3" style={{ textAlign: "center", padding: "10px" }}>
                            No data available.
                        </td>
                    </tr>
                ) : (
                    data.map((user, index) => (
                        <tr key={user.name} style={trStyle}>
                            <td style={tdStyle}>{index + 1}</td>
                            <td style={tdStyle}>{user.name}</td>
                            <td style={tdStyle}>{user.total_score ? user.total_score : user.total_games}</td>
                        </tr>
                    ))
                )}
            </tbody>
        </table>
    );
}

Leaderboard.propTypes = {
    data: PropTypes.arrayOf(
        PropTypes.shape({
            name: PropTypes.string.isRequired,
            total_score: PropTypes.number,
        })
    ).isRequired,
    mode: PropTypes.oneOf(["score", "games"]).isRequired,
};

const thStyle = {
    border: "1px solid #dddddd",
    textAlign: "left",
    padding: "8px",
    backgroundColor: "#f2f2f2",
};

const tdStyle = {
    border: "1px solid #dddddd",
    textAlign: "left",
    padding: "8px",
};

const trStyle = {
    backgroundColor: "#ffffff",
};