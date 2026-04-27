-- ============================================
-- PestVid Database Tables - Supabase
-- Copy this entire file and run in Supabase SQL Editor
-- ============================================

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

-- Avatar Messages table
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
