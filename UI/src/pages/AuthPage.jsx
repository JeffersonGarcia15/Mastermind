import { useState } from "react";
import { LoginForm, SignupForm } from "../components/Auth";
import { useNavigate } from "react-router";
import { login } from "../utils/api";

export function AuthPage() {
    const [mode, setMode] = useState("login");
    const navigate = useNavigate();

    function handleLoginSuccess() {
        navigate("/");
        window.location.reload();
    }

    function handleSignupSuccess() {
        navigate("/");
        window.location.reload();
    }

    async function handleDemoUser(e) {
        e.preventDefault();
        const name = import.meta.env.VITE_DEMO_NAME;
        const password = import.meta.env.VITE_DEMO_PASSWORD;
        const { data, error } = await login(name, password);
        if (data) {
            handleLoginSuccess();
        } else {
            console.log(error);
            alert("Something went wrong when trying to use the demo user");
        }
    }

    return (
        <div>
            <button onClick={() => setMode("login")}>Login</button>
            <button onClick={() => setMode("signup")}>Signup</button>
            <button onClick={handleDemoUser}>Demo User</button>
            {mode === "login" ? <LoginForm onLoginSuccess={handleLoginSuccess} /> : <SignupForm onSignupSuccess={handleSignupSuccess} />}
        </div>
    );
}