import { useState } from "react";
import PropTypes from "prop-types";
import { login } from "../../utils/api";

export function LoginForm({ onLoginSuccess }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();
        const { data, error } = await login(email, password);
        if (data) {
            onLoginSuccess();
        }
        else {
            alert(error || "Login failed");
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <h2>Login</h2>
            <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
            <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
            <button type="submit">Login</button>
        </form>
    );
}

LoginForm.propTypes = {
    onLoginSuccess: PropTypes.func.isRequired
};