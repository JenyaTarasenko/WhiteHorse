// src/components/Scanner/Scanner.jsx
import React, { useState } from "react";

export default function DomenScan() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleScan = async () => {
    setError("");
    setResult(null);
  
    if (!url) {
      setError("Введите URL (например https://example.com)");
      return;
    }
  
    setLoading(true);
    try {
          const resp = await fetch("http://127.0.0.1:8001/api/test-scan/", {
          method: "POST",
          headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          Accept: "application/json",
        },
        body: new URLSearchParams({ url }), // 👈 именно сюда передаём URL
      });
  
      const data = await resp.json();
      if (!resp.ok) {
        setError(data.error || "Ошибка сервера");
      } else {
        setResult(data);
      }
    } catch (e) {
      setError("Network error: не удалось связаться с сервером");
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <div style={{ maxWidth: 900, margin: "24px auto", padding: 16 }}>
      <h2>Quick Scanner</h2>

      <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com"
          style={{ flex: 1, padding: 8, fontSize: 14 }}
        />
        <button onClick={handleScan} disabled={loading} style={{ padding: "8px 16px" }}>
          {loading ? "Сканирую..." : "Сканировать"}
        </button>
      </div>

      {error && <div style={{ color: "crimson", marginBottom: 12 }}>{error}</div>}

      {result && (
        <div style={{
          background: "#f6f8fa",
          padding: 12,
          borderRadius: 8,
          fontFamily: "monospace",
          whiteSpace: "pre-wrap",
          maxHeight: "60vh",
          overflow: "auto",
        }}>
          <strong>Результат (JSON):</strong>
          <pre style={{ marginTop: "8px", color:"black" }}>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
