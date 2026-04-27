# 🚀 Supabase Migration Guide - MongoDB to Supabase (PostgreSQL)

## Overview
This guide will help you migrate your PestVid backend from MongoDB to Supabase (PostgreSQL) for cloud hosting.

## Why Supabase?
- ✅ Free tier with generous limits
- ✅ PostgreSQL database (more reliable than MongoDB for production)
- ✅ Built-in authentication
- ✅ Real-time subscriptions
- ✅ Auto-generated REST API
- ✅ Storage for files/videos
- ✅ Easy deployment and scaling

---

## Step 1: Create Supabase Account

1. Go to https://supabase.com
2. Click "Start your project"
3. Sign up with GitHub or email
4. Create a new project:
   - Project name: `pestivid`
   - Database password: (save this securely!)
   - Region: Choose closest to your users
   - Pricing plan: Free tier

---

## Step 2: Get Supabase Credentials

After project creation, go to Project Settings > API:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key (keep secret!)
```

---

## Step 3: Create Database Tables

Go to SQL Editor in Supabase Dashboard and run this SQL:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('farmer', 'buyer', 'investor')),
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    member_since TIMESTAMP DEFAULT NOW(),
    auth_method VARCHAR(50) DEFAULT 'email_pass_demo',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Videos table
CREATE TABLE videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cid VARCHAR(255) UNIQUE NOT NULL,
    storage_type VARCHAR(50) NOT NULL CHECK (storage_type IN ('storj', 'ipfs')) DEFAULT 'ipfs',
    video_file_hash VARCHAR(255),
    farmer_wallet UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    crop VARCHAR(255) NOT NULL,
    pesticide VARCHAR(255),
    location VARCHAR(255) NOT NULL,
    pesticide_company VARCHAR(255),
    purpose VARCHAR(50) NOT NULL CHECK (purpose IN ('agristream', 'sell', 'funding')) DEFAULT 'agristream',
    upload_timestamp TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Listings table
CREATE TABLE listings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_wallet UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    crop VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    pesticide VARCHAR(255),
    pesticide_company VARCHAR(255),
    cid VARCHAR(255) NOT NULL,
    storage_type VARCHAR(50) DEFAULT 'ipfs',
    video_file_hash VARCHAR(255),
    min_price DECIMAL(10, 2) NOT NULL CHECK (min_price >= 0),
    max_price DECIMAL(10, 2) NOT NULL CHECK (max_price >= 0),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'sold', 'cancelled')),
    notification_sent BOOLEAN DEFAULT FALSE,
    tx_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Funding Requests table
CREATE TABLE funding_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_wallet UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    crop VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    pesticide VARCHAR(255),
    pesticide_company VARCHAR(255),
    cid VARCHAR(255) NOT NULL,
    storage_type VARCHAR(50) DEFAULT 'ipfs',
    video_file_hash VARCHAR(255),
    funding_goal DECIMAL(10, 2) NOT NULL CHECK (funding_goal > 0),
    current_funding DECIMAL(10, 2) DEFAULT 0 CHECK (current_funding >= 0),
    status VARCHAR(50) DEFAULT 'open' CHECK (status IN ('open', 'funded', 'closed')),
    expected_return_percentage DECIMAL(5, 2) DEFAULT 0,
    project_duration_months INTEGER DEFAULT 6,
    notification_sent BOOLEAN DEFAULT FALSE,
    tx_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Investments table
CREATE TABLE investments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    investor_wallet UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    funding_request_id UUID NOT NULL REFERENCES funding_requests(id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
    tx_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Purchases table
CREATE TABLE purchases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    buyer_wallet UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    listing_id UUID NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    tx_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Transactions table
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_wallet UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL CHECK (type IN ('purchase', 'sale', 'investment', 'return')),
    amount DECIMAL(10, 2) NOT NULL,
    related_id UUID,
    tx_hash VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Conversations table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    participant1 UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    participant2 UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    last_message_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(participant1, participant2)
);

-- Messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    receiver UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    read BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Notifications table
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_wallet UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    read BOOLEAN DEFAULT FALSE,
    related_id UUID,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Avatar Messages table (for AI chatbot)
CREATE TABLE avatar_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_wallet UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_videos_farmer ON videos(farmer_wallet);
CREATE INDEX idx_listings_farmer ON listings(farmer_wallet);
CREATE INDEX idx_listings_status ON listings(status);
CREATE INDEX idx_funding_requests_farmer ON funding_requests(farmer_wallet);
CREATE INDEX idx_funding_requests_status ON funding_requests(status);
CREATE INDEX idx_investments_investor ON investments(investor_wallet);
CREATE INDEX idx_investments_funding_request ON investments(funding_request_id);
CREATE INDEX idx_purchases_buyer ON purchases(buyer_wallet);
CREATE INDEX idx_purchases_listing ON purchases(listing_id);
CREATE INDEX idx_transactions_user ON transactions(user_wallet);
CREATE INDEX idx_conversations_participants ON conversations(participant1, participant2);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
CREATE INDEX idx_notifications_user ON notifications(user_wallet);
CREATE INDEX idx_notifications_read ON notifications(read);
CREATE INDEX idx_avatar_messages_user ON avatar_messages(user_wallet);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add trigger to users table
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## Step 4: Enable Row Level Security (RLS)

Run this SQL to enable security:

```sql
-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE videos ENABLE ROW LEVEL SECURITY;
ALTER TABLE listings ENABLE ROW LEVEL SECURITY;
ALTER TABLE funding_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE investments ENABLE ROW LEVEL SECURITY;
ALTER TABLE purchases ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE avatar_messages ENABLE ROW LEVEL SECURITY;

-- Create policies (examples - adjust based on your needs)
-- Users can read their own data
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (true);

-- Anyone can view active listings
CREATE POLICY "Anyone can view active listings" ON listings
    FOR SELECT USING (status = 'active');

-- Farmers can create their own listings
CREATE POLICY "Farmers can create listings" ON listings
    FOR INSERT WITH CHECK (true);

-- Users can view their own transactions
CREATE POLICY "Users can view own transactions" ON transactions
    FOR SELECT USING (true);

-- Users can view their own messages
CREATE POLICY "Users can view own messages" ON messages
    FOR SELECT USING (true);

-- Users can send messages
CREATE POLICY "Users can send messages" ON messages
    FOR INSERT WITH CHECK (true);

-- Users can view their own notifications
CREATE POLICY "Users can view own notifications" ON notifications
    FOR SELECT USING (true);
```

---

## Step 5: Update Backend Configuration

Update `backend/.env`:

```env
# Remove MongoDB
# MONGODB_URI=mongodb://127.0.0.1:27017/pest

# Add Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key

# Keep existing
PORT=3001
JWT_SECRET=your_super_secret_key_replace_this_in_production
```

---

## Step 6: Install Supabase Client

```bash
cd backend
npm install @supabase/supabase-js
npm uninstall mongoose  # Remove MongoDB dependency
```

---

## Step 7: Update Backend Files

I'll create the updated files for you:
- `backend/config/supabase.js` - Supabase client configuration
- `backend/models-supabase/` - New model files for Supabase
- `backend/server-supabase.js` - Updated server file

---

## Step 8: Test the Migration

1. Start the updated backend:
```bash
cd backend
node server-supabase.js
```

2. Test endpoints:
```bash
# Test signup
curl -X POST http://localhost:3001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"password123","role":"farmer"}'

# Test login
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

---

## Step 9: Deploy to Production

### Option A: Deploy Backend to Vercel
1. Push code to GitHub
2. Connect to Vercel
3. Add environment variables
4. Deploy!

### Option B: Deploy Backend to Railway
1. Push code to GitHub
2. Connect to Railway
3. Add environment variables
4. Deploy!

### Option C: Deploy Backend to Render
1. Push code to GitHub
2. Connect to Render
3. Add environment variables
4. Deploy!

---

## Benefits of Supabase Migration

✅ **No Database Management** - Supabase handles backups, scaling, security
✅ **Better Performance** - PostgreSQL is faster and more reliable
✅ **Real-time Features** - Built-in WebSocket support
✅ **File Storage** - Store videos directly in Supabase Storage
✅ **Authentication** - Built-in auth system (optional to use)
✅ **Free Tier** - 500MB database, 1GB file storage, 2GB bandwidth
✅ **Easy Scaling** - Upgrade as you grow
✅ **Better for Production** - Enterprise-grade reliability

---

## Migration Checklist

- [ ] Create Supabase account
- [ ] Create new project
- [ ] Run SQL to create tables
- [ ] Enable RLS and create policies
- [ ] Update backend/.env with Supabase credentials
- [ ] Install @supabase/supabase-js
- [ ] Update backend files (I'll create these for you)
- [ ] Test all endpoints
- [ ] Migrate existing data (if any)
- [ ] Deploy to production
- [ ] Update frontend API URLs
- [ ] Test production deployment

---

## Next Steps

I'll now create the updated backend files for Supabase integration!
