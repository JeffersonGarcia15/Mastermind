import { useState } from "react";
import PropTypes from "prop-types";

export function GameBoard({ length, onSubmitGuess }) {
    const [guess, setGuess] = useState(Array(length).fill(""));

    // Handle input changes with validation for digits 0-7
    function handleChange(i, val) {
        const newGuess = [...guess];
        // Allow only digits 0-7 and limit input length to 1
        if (/^[0-7]?$/.test(val)) { // Empty string or single digit 0-7
            newGuess[i] = val;
            setGuess(newGuess);
        }
    }

    function handleSubmit(e) {
        e.preventDefault();
        const guessString = guess.join("");

        if (guessString.length !== length) {
            alert(`Please enter all ${length} digits.`);
            return;
        }

        onSubmitGuess(guessString);
        setGuess(Array(length).fill("")); // Clear inputs after submission
    }

    return (
        <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
            <p>Enter digits [0-7] only</p>
            <div style={{ display: "flex", justifyContent: "center", marginBottom: "10px" }}>
                {guess.map((g, i) => (
                    <input
                        key={i}
                        type="text"
                        value={g}
                        onChange={e => handleChange(i, e.target.value)}
                        maxLength={1}
                        pattern="[0-7]"
                        title="Enter a digit between 0 and 7"
                        required
                        style={{ width: "40px", height: "40px", textAlign: "center", marginRight: "5px", fontSize: "18px" }}
                    />
                ))}
            </div>
            <button type="submit" style={{ padding: "10px 20px", fontSize: "16px" }}>Guess</button>
        </form>
    );
}

GameBoard.propTypes = {
    length: PropTypes.number.isRequired,
    onSubmitGuess: PropTypes.func.isRequired
};