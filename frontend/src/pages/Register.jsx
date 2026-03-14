import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";

function Register() {

  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [nameError, setNameError] = useState("");
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const validatePassword = (password) => {
    const regex = /^(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.*[0-9]).{8,}$/;
    return regex.test(password);
  };

  const handleRegister = async () => {

    setNameError("");
    setEmailError("");
    setPasswordError("");

    if (name === "") {
      setNameError("Name required");
      return;
    }

    if (!email.includes("@")) {
      setEmailError("Enter valid email");
      return;
    }

    if (!validatePassword(password)) {
      setPasswordError(
        "Password must be 8+ characters with uppercase, number & symbol"
      );
      return;
    }

    try {

      await API.post("/auth/register", null, {
        params: {
          name: name,
          email: email,
          password: password
        }
      });

      navigate("/login");

    } catch (err) {

      setEmailError(err.response?.data?.detail || "Registration failed");

    }
  };

  return (

    <div className="container d-flex justify-content-center align-items-center vh-100">

      <div className="card p-4 shadow" style={{ width: "400px" }}>

        <h3 className="text-center mb-4">Create Account</h3>

        <input
          type="text"
          placeholder="Full Name"
          className={`form-control mb-1 ${nameError ? "border-danger" : ""}`}
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        {nameError && <p style={{ color: "red" }}>{nameError}</p>}

        <input
          type="email"
          placeholder="Email"
          className={`form-control mb-1 ${emailError ? "border-danger" : ""}`}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        {emailError && <p style={{ color: "red" }}>{emailError}</p>}

        <input
          type="password"
          placeholder="Password"
          className={`form-control mb-1 ${passwordError ? "border-danger" : ""}`}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {passwordError && <p style={{ color: "red" }}>{passwordError}</p>}

        <button
          className="btn btn-success w-100 mt-2"
          onClick={handleRegister}
        >
          Register
        </button>

        <p className="text-center mt-3">
          Already have an account?
          <span
            style={{ color: "blue", cursor: "pointer" }}
            onClick={() => navigate("/login")}
          >
            Login
          </span>
        </p>

      </div>

    </div>
  );
}

export default Register;