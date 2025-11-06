// // src/components/Scanner/Scanner.jsx
import React, { useState } from "react";

export default function DomenScan() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [progress, setProgress] = useState(0);

  const handleScan = async () => {
    setError("");
    setResult(null);

    if (!url) {
      setError("Введите URL (например https://example.com)");
      return;
    }

    setLoading(true);
    try {
      const resp = await fetch("http://127.0.0.1:8001/api/start-scan/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          Accept: "application/json",
        },
        body: new URLSearchParams({ url }),
      });

      const data = await resp.json();

      if (resp.ok) {
        console.log("✅ Сканирование запущено, task_id:", data.task_id || data.scan_id);
        pollResult(data.task_id || data.scan_id); // <-- запускаем опрос
      } else {
        setError(data.error || "Ошибка сервера при запуске сканирования");
      }
    } catch (e) {
      console.error("Ошибка при запуске сканирования:", e);
      setError("Network error: не удалось связаться с сервером");
    } finally {
      setLoading(false);
    }
  };

  const pollResult = (taskId) => {
    console.log("🚀 Начинаем опрос результата:", taskId);
    let attempts = 0;
    const maxAttempts = 40; // ~2 минуты

    const intervalId = setInterval(async () => {
      attempts++;
      setProgress((prev) => Math.min(prev + 3, 95));

      try {
        const res = await fetch(`http://127.0.0.1:8001/api/scan-result/${taskId}/`);
        const data = await res.json();
        console.log(`📡 Попытка #${attempts}:`, data);

        if (data.status === "completed") {
          clearInterval(intervalId);
          setProgress(100); // финал
          console.log("✅ Сканирование завершено:", data);
          setResult(data.data);
          setLoading(false);
        } else if (data.status === "FAILURE") {
          clearInterval(intervalId);
          setError("Ошибка при сканировании (Celery failure)");
          setLoading(false);
        } else if (attempts >= maxAttempts) {
          clearInterval(intervalId);
          setError("⏰ Время ожидания результата истекло.");
          setLoading(false);
        }
      } catch (err) {
        clearInterval(intervalId);
        console.error("Ошибка при получении результата:", err);
        setError("Ошибка при получении результата.");
        setLoading(false);
      }
    }, 3000);
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
        <div
          style={{
            background: "#f6f8fa",
            padding: 12,
            borderRadius: 8,
            fontFamily: "monospace",
            whiteSpace: "pre-wrap",
            maxHeight: "60vh",
            overflow: "auto",
          }}
        >
          <strong>Результат (JSON):</strong>
          <pre style={{ marginTop: "8px", color: "black" }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
