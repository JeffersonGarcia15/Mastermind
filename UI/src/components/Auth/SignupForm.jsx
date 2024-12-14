import { useState } from "react";
import PropTypes from "prop-types";
import { signup } from "../../utils/api";

export function SignupForm({ onSignupSuccess }) {
    const [username, setUserName] = useState("");
    const [password, setPassword] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();
        const { data, error } = await signup(username, password);
        if (data) {
            onSignupSuccess();
        } else {
            alert(error || "Signup failed");
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <h2>Signup</h2>
            <input
                placeholder="Name"
                value={username}
                onChange={e => setUserName(e.target.value)}
                required
            />
            <input
                placeholder="Password"
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
            />
            <button type="submit">Signup</button>
        </form>
    );
}

SignupForm.propTypes = {
    onSignupSuccess: PropTypes.func.isRequired
};