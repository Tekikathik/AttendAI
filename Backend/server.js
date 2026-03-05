const express = require("express");
const cors = require("cors");
const multer = require("multer");
const path = require("path");
const { exec } = require("child_process");

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

// Multer storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "uploads/");
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname));
  }
});

const upload = multer({ storage });

// Upload + AI processing
app.post("/upload", upload.single("file"), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: "No file uploaded" });
  }

  const filePath = req.file.path;
  const fileType = req.body.type || "image";

  console.log("File uploaded:", filePath);

  const command = `python AI/ai_attendance.py "${filePath}" "${fileType}"`;

  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error("Python error:", error);
      return res.status(500).json({ error: "AI processing failed" });
    }

    console.log(stdout);
    res.json({ message: "Attendance processed successfully" });
  });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});