/* eslint-disable react/prop-types */
export function HintCircles({ correct_positions, correct_numbers_only, total }) {
    const blacks = Array(correct_positions).fill("black");
    const whites = Array(correct_numbers_only).fill("white");
    const emptyCount = Math.max(total - correct_positions - correct_numbers_only, 0);
    const empty = Array(emptyCount).fill("red"); // Empty circles
    const circles = [...blacks, ...whites, ...empty];

    // Shuffle the circles array to randomize the order
    for (let i = circles.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [circles[i], circles[j]] = [circles[j], circles[i]];
    }

    return (
        <div style={{ marginTop: "5px" }}>
            {circles.map((c, i) => (
                <span key={i} style={{
                    display: "inline-block",
                    width: "15px",
                    height: "15px",
                    backgroundColor: c,
                    borderRadius: "50%",
                    marginRight: "3px",
                    border: "1px solid #000"
                }}></span>
            ))}
        </div>
    );
}