// --- Main Backend Server File: server-supabase.js ---
// Supabase version - replaces MongoDB with PostgreSQL

const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const path = require('path');

// Load environment variables
dotenv.config();

// Create Express app
const app = express();

// --- Middleware Setup ---
const corsOptions = {
  origin: process.env.NODE_ENV === 'production' ? process.env.FRONTEND_URL : '*',
  optionsSuccessStatus: 200
};
app.use(cors(corsOptions));
app.use(express.json({ limit: '10mb' }));

// Serve static files
app.use(express.static(path.join(__dirname, '../public')));

// --- Initialize Supabase Connection ---
const { supabase } = require('./config/supabase');

console.log('✅ Supabase client initialized');

// --- API Routes ---
const { router: authRoutes } = require('./routes-supabase/auth');

app.use('/api/auth', authRoutes);
app.use('/api/users', require('./routes-supabase/users'));
app.use('/api/videos', require('./routes-supabase/videos'));
app.use('/api/listings', require('./routes-supabase/listings'));
app.use('/api/funding-requests', require('./routes-supabase/fundingRequests'));
app.use('/api/investments', require('./routes-supabase/investments'));
app.use('/api/purchases', require('./routes-supabase/purchases'));
app.use('/api/transactions', require('./routes-supabase/transactions'));
app.use('/api/messaging', require('./routes-supabase/messaging'));
app.use('/api/notifications', require('./routes-supabase/notifications'));
app.use('/api/conversations', require('./routes-supabase/conversations'));
app.use('/api/avatarmessages', require('./routes-supabase/avatarmessages'));
app.use('/api/ai', require('./routes/ai')); // AI routes don't need database changes

// Basic test route
app.get('/', (req, res) => {
    res.json({ 
        message: 'PestiVid Backend API (Supabase) is running!',
        database: 'Supabase PostgreSQL',
        status: 'online'
    });
});

// --- Error Handling Middleware ---
app.use((req, res, next) => {
    const err = new Error('Not Found');
    err.status = 404;
    next(err);
});

// Development error handler
if (app.get('env') === 'development') {
    app.use((err, req, res, next) => {
        console.error("Development Error:", err.stack);
        res.status(err.status || 500);
        res.json({
            message: err.message,
            error: err
        });
    });
}

// Production error handler
app.use((err, req, res, next) => {
    console.error("Production Error:", err.message);
    res.status(err.status || 500);
    res.json({
        message: err.message,
        error: {}
    });
});

// --- Server Start ---
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
    console.log(`📊 Database: Supabase PostgreSQL`);
    console.log(`🌐 API: http://localhost:${PORT}`);
});
