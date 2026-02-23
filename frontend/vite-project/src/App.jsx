import React, { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [sql, setSql] = useState("");
  const [loading, setLoading] = useState(false);

  const generateSQL = async () => {
    if (!query) return;
    setLoading(true);
    setSql("");

    try {
      const res = await fetch("http://127.0.0.1:5000/generate-sql", {
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
      <h1>🧠 AI SQL Query Generator</h1>

      <textarea
        placeholder="Enter your request (e.g., Get all users joined last month)"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button onClick={generateSQL}>
        {loading ? "Generating..." : "Generate SQL"}
      </button>

      {sql && (
        <div className="result">
          <h3>Generated SQL:</h3>
          <pre>{sql}</pre>
        </div>
      )}
    </div>
  );
}

export default App;