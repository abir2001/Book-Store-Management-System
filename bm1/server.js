const express = require('express');
const path = require('path');
const cors = require('cors');
const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// API endpoints
app.get('/api/books', (req, res) => {
  // Code to get books from the Python backend API
});

app.post('/api/cart', (req, res) => {
  // Code to add to cart in the Python backend API
});

// Add more endpoints as needed

app.listen(port, () => {
  console.log(`Server running on http://localhost:${3306}`);
});
