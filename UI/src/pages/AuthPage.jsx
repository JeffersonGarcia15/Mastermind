import { useState } from "react";
import { LoginForm, SignupForm } from "../components/Auth";
import { useNavigate } from "react-router";

export function AuthPage() {
    const [mode, setMode] = useState("login");
    const navigate = useNavigate();

    function handleLoginSuccess() {
        navigate("/");
    }

    function handleSignupSuccess() {
        navigate("/");
    }

    return (
        <div>
            <button onClick={() => setMode("login")}>Login</button>
            <button onClick={() => setMode("signup")}>Signup</button>
            {mode === "login" ? <LoginForm onLoginSuccess={handleLoginSuccess} /> : <SignupForm onSignupSuccess={handleSignupSuccess} />}
        </div>
    );
}
