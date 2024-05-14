const express = require("express");
const axios = require("axios");
const app = express();
const port = 3000; // Or any other available port you prefer

app.use(express.json());

app.post("/record_attendance", (req, res) => {
  // Forward the request to your Render server
  axios
    .post("https://test0-ugfq.onrender.com/record_attendance", req.body)
    .then((response) => {
      // Send the Render server's response back to the ESP32-CAM
      res.status(response.status).json(response.data);
    })
    .catch((error) => {
      console.error(error);
      res.status(500).json({ error: "Failed to forward request" });
    });
});

app.listen(port, () => {
  console.log(`Proxy server listening at http://localhost:${port}`);
});
