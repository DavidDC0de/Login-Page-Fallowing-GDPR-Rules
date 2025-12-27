import { useState } from "react";

function App() {
  // State for form data
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [gdprConsent, setGdprConsent] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    // send data to the backend 
    try {
      const response = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          password,
          gdpr_consent: gdprConsent,
        }),
      });

      // gets response form the backend
      const data = await response.json();

      //display response
      if (!response.ok) {
        setMessage(data.detail || "Registration failed");
      } else {
        setMessage(data.message);
        setEmail("");  //sets the boxes to blank
        setPassword("");
        setGdprConsent(false);
      }
    } catch {
      setMessage("Server error");
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "400px", margin: "auto" }}>
      <h2>Register</h2>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label><br />
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Password:</label><br />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div>
          <input
            type="checkbox"
            checked={gdprConsent}
            onChange={(e) => setGdprConsent(e.target.checked)}
          />
          <label>
            I consent to my personal data being used to create an account.
          </label>
        </div>

        <button type="submit">Register</button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}

export default App;
