import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [type, setType] = useState("image");

  const submit = async () => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("type", type);

    await axios.post("http://localhost:5000/upload", formData);
    alert("Processed successfully");
  };

  return (
    <div style={{ textAlign: "center", marginTop: 50 }}>
      <h2>AI Attendance System</h2>

      <select onChange={e => setType(e.target.value)}>
        <option value="image">Image Upload</option>
        <option value="video">Video Upload</option>
      </select>
      <br /><br />

      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <br /><br />

      <button onClick={submit}>Upload</button>
    </div>
  );
}

export default App;