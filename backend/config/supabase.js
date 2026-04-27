// --- Supabase Configuration ---

const { createClient } = require('@supabase/supabase-js');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

// Supabase credentials from environment variables
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_KEY; // Use service key for backend operations
const supabaseAnonKey = process.env.SUPABASE_ANON_KEY; // Use anon key for client-side operations

if (!supabaseUrl) {
    console.error('ERROR: SUPABASE_URL must be provided in .env file');
    process.exit(1);
}

// Use service key if available, otherwise fall back to anon key with warning
let keyToUse = supabaseServiceKey;
if (!supabaseServiceKey || supabaseServiceKey === 'YOUR_SERVICE_ROLE_KEY_HERE') {
    console.warn('⚠️  WARNING: SUPABASE_SERVICE_KEY not configured, using ANON_KEY');
    console.warn('⚠️  Some operations may fail. Get service_role key from:');
    console.warn('⚠️  https://supabase.com/dashboard/project/zdkeisiffbncmvonqhdf/settings/api');
    keyToUse = supabaseAnonKey;
}

// Create Supabase client with service role key (bypasses RLS for backend operations)
const supabase = createClient(supabaseUrl, keyToUse, {
    auth: {
        autoRefreshToken: false,
        persistSession: false
    }
});

// Create Supabase client with anon key (respects RLS, for client-side operations if needed)
const supabaseAnon = createClient(supabaseUrl, supabaseAnonKey);

console.log('✅ Supabase client initialized successfully');
console.log(`📍 Supabase URL: ${supabaseUrl}`);

module.exports = {
    supabase,
    supabaseAnon,
    supabaseUrl
};
