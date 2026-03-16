import React, { useState } from "react";
import "./App.css";
import API from "./config";

function App() {
  const [query, setQuery] = useState("");
  const [sql, setSql] = useState("");
  const [loading, setLoading] = useState(false);

  const generateSQL = async () => {
    if (!query) return;
    setLoading(true);
    setSql("");

    try {
      const res = await fetch(`${API.BASE_URL}/generate-sql`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();
      setSql(data.sql);
    } catch (err) {
      setSql("Error generating SQL");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1>🧠 AI Image Generator</h1>

      <textarea
        placeholder="Enter your request (e.g., Generate image of nature)"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button onClick={generateSQL}>
        {loading ? "Generating..." : "Generate Image"}
      </button>

      {sql && (
        <div className="result">
          <h3>Generated Image:</h3>
          <pre>{sql}</pre>
        </div>
      )}
    </div>
  );
}

export default App;