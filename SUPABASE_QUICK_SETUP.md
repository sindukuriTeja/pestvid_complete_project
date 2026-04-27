# 🚀 Supabase Quick Setup - 15 Minutes to Cloud!

## Quick Overview
This guide gets your PestVid backend running on Supabase in 15 minutes.

---

## Step 1: Create Supabase Account (2 minutes)

1. Go to https://supabase.com
2. Click "Start your project"
3. Sign up (use GitHub for fastest signup)
4. Create new project:
   - Name: `pestivid`
   - Password: (save this!)
   - Region: Choose closest to you
   - Plan: Free

---

## Step 2: Setup Database (5 minutes)

1. In Supabase Dashboard, go to **SQL Editor**
2. Click "New Query"
3. Copy and paste the SQL from `SUPABASE_MIGRATION_GUIDE.md` (Step 3)
4. Click "Run" or press `Ctrl+Enter`
5. You should see "Success. No rows returned"

---

## Step 3: Get Your Credentials (1 minute)

1. Go to **Project Settings** > **API**
2. Copy these values:

```
Project URL: https://xxxxx.supabase.co
anon public key: eyJhbGc...
service_role key: eyJhbGc... (keep secret!)
```

---

## Step 4: Update Backend Config (2 minutes)

1. Open `backend/.env`
2. Add these lines:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-role-key-here

# Keep existing
PORT=3001
JWT_SECRET=your_super_secret_key_replace_this_in_production
```

---

## Step 5: Install Dependencies (2 minutes)

```bash
cd backend
npm install @supabase/supabase-js
```

---

## Step 6: Test Connection (3 minutes)

Create a test file `backend/test-supabase.js`:

```javascript
const { supabase } = require('./config/supabase');

async function testConnection() {
    console.log('Testing Supabase connection...');
    
    try {
        // Test query
        const { data, error } = await supabase
            .from('users')
            .select('count')
            .limit(1);
        
        if (error) throw error;
        
        console.log('✅ Supabase connection successful!');
        console.log('Database is ready to use.');
    } catch (error) {
        console.error('❌ Connection failed:', error.message);
    }
}

testConnection();
```

Run it:
```bash
node test-supabase.js
```

You should see: `✅ Supabase connection successful!`

---

## Step 7: Start Using Supabase (Now!)

### Option A: Use New Supabase Backend

I've created new model files in `backend/models-supabase/`:
- `User.js`
- `Video.js`
- `Listing.js`

To use them, update your route files to import from `models-supabase` instead of `models`.

### Option B: Keep MongoDB for Now

You can run both MongoDB and Supabase side-by-side during migration:
- Keep existing routes using MongoDB
- Create new routes using Supabase
- Gradually migrate

---

## Quick Test - Create a User

```javascript
// test-create-user.js
const User = require('./models-supabase/User');

async function testCreateUser() {
    try {
        const user = await User.create({
            name: 'Test Farmer',
            email: 'farmer@test.com',
            password: 'password123',
            role: 'farmer'
        });
        
        console.log('✅ User created:', user);
    } catch (error) {
        console.error('❌ Error:', error.message);
    }
}

testCreateUser();
```

---

## What's Next?

### For Development:
1. ✅ Supabase is ready
2. ✅ Test with Postman/curl
3. ✅ Update frontend to use new backend

### For Production:
1. Deploy backend to Vercel/Railway/Render
2. Update frontend API URLs
3. Enable Supabase RLS policies
4. Add proper error handling
5. Set up monitoring

---

## Common Issues & Solutions

### "Invalid API key"
- Check your `.env` file
- Make sure you copied the full key
- Restart your server after updating `.env`

### "relation does not exist"
- Run the SQL script in Supabase SQL Editor
- Check you're connected to the right project

### "Connection refused"
- Check your SUPABASE_URL is correct
- Make sure you have internet connection
- Verify project is not paused (free tier pauses after 1 week inactivity)

---

## Supabase Dashboard Features

### Tables
- View and edit data directly
- See real-time updates
- Export data as CSV

### SQL Editor
- Run custom queries
- Create functions
- Manage indexes

### Authentication
- Built-in user management
- Social login providers
- Email verification

### Storage
- Upload files/videos
- CDN delivery
- Access control

### API Docs
- Auto-generated REST API
- GraphQL support
- Real-time subscriptions

---

## Free Tier Limits

✅ 500 MB database storage
✅ 1 GB file storage
✅ 2 GB bandwidth per month
✅ 50,000 monthly active users
✅ Unlimited API requests
✅ Social OAuth providers
✅ 7-day log retention

Perfect for development and small production apps!

---

## Need Help?

1. Check Supabase docs: https://supabase.com/docs
2. Join Supabase Discord: https://discord.supabase.com
3. Check the full migration guide: `SUPABASE_MIGRATION_GUIDE.md`

---

## You're Done! 🎉

Your backend is now cloud-ready with Supabase!

Next: Deploy your backend and update frontend URLs.
