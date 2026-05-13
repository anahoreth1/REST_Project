import { useState } from "react";
import api from "../api/api";

export default function Register() {
  const [name, setUsername] = useState("");
  const [email, setEmail] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post("/users/", {
        name,
        email,
      });

      alert("User created!");
      console.log(res.data);
    } catch (err) {
      console.log(err);
      alert("Error");
    }
  };

  return (
    <div>
      <h2>Register</h2>

      <form onSubmit={handleSubmit}>
        <input placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
        <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />

        <button type="submit">Register</button>
      </form>
    </div>
  );
}
