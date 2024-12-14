export function HomePage() {
    return (
        <div>
            <h1>Welcome to Mastermind!</h1>
            <p>Rules:</p>
            <ul>
                <li>Digits range from 0 to 7 only.</li>
                <li>A black circle indicates a correct digit in the correct position.</li>
                <li>A white circle indicates a correct digit in the wrong position.</li>
                <li>A red circle indicates an incorrect digit.</li>
                <li>The circles are randomized, making it challenging to deduce which exact positions are correct.</li>
                <li>2 difficulties: Medium(4 numbers) and Hard(6 numbers)</li>
            </ul>
            <p>Playing in hard mode allows you to win +5 points every time you win!</p>
            <p>Please note: The hint circles for previous guesses may appear in a different randomized order after submitting a new guess. This is expected behavior for now.</p>
            <p>Try to guess the solution within 10 attempts!</p>
            <b><i>Note: Leaving a game as a user allows you to resume it once you go back to the /game page. However, if you are NOT logged in you will lose your progress. At the moment, you cannot log in, in the middle of an on going guest game, and store the progress.</i></b><br />
            <b><i>This is because the Game record is created as soon as you send the request, modifying a game to go from guest to a user_id will require extra changes in the frontend and backend for which I do not count with enough time to implement them.</i></b>
        </div>
    );
}