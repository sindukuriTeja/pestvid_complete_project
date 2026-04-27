// SIMPLE SERVER - NO DATABASE NEEDED!
// Uses JSON files instead

const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const path = require('path');

dotenv.config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.static(path.join(__dirname, '../public')));

console.log('✅ Simple JSON File Database Ready');

// Routes
const { router: authRoutes } = require('./routes-simple/auth');
app.use('/api/auth', authRoutes);

// Test route
app.get('/', (req, res) => {
    res.json({ 
        message: 'PestiVid Backend API (Simple JSON) is running!',
        database: 'JSON Files',
        status: 'online'
    });
});

// Error handling
app.use((req, res, next) => {
    res.status(404).json({ message: 'Not Found' });
});

app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ message: err.message });
});

// Start server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
    console.log(`📊 Database: JSON Files (No setup needed!)`);
    console.log(`🌐 API: http://localhost:${PORT}`);
});
