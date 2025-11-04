import React, { useState } from "react";
import axios from "axios";

function RegisterForm({onSuccess}) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [domain, setDomain] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    try {
      const response = await axios.post("http://127.0.0.1:8001/api/register/", {
        username,
        password,
        domain,
        
      });

      if (response.status === 201) {
        setMessage(response.data.message || "✅ Вы успешно зарегистрировались!");
          // 🔹 очищаем форму
        setUsername("");
        setPassword("");
        setDomain("");
           // 🔹 очищаем сообщение через 3 секунды
        setTimeout(() => {
        setMessage("");
        onSuccess(); // 🔥 ВАЖНО: именно это переключает компонент!
        }, 1000);
        
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Ошибка при регистрации");
      setTimeout(() => setError(""), 4000);
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "auto" }}>
      <h2>Регистрация</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Имя пользователя"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        /><br />

        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        /><br />

        <input
          type="text"
          placeholder="Ваш домен (example.com)"
          value={domain}
          onChange={(e) => setDomain(e.target.value)}
        /><br />

        <button type="submit">Зарегистрироваться</button>
      </form>

      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default RegisterForm;
