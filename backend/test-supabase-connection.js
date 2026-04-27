// Test Supabase Connection
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;

console.log('Testing Supabase Connection...\n');
console.log('URL:', supabaseUrl);
console.log('Key:', supabaseKey.substring(0, 20) + '...\n');

const supabase = createClient(supabaseUrl, supabaseKey);

async function testConnection() {
    try {
        // Try to query users table
        const { data, error } = await supabase
            .from('users')
            .select('count')
            .limit(1);

        if (error) {
            if (error.message.includes('does not exist') || error.code === 'PGRST205') {
                console.log('❌ Tables do not exist yet');
                console.log('');
                console.log('You need to create tables in Supabase:');
                console.log('1. Go to: https://supabase.com/dashboard/project/zdkeisiffbncmvonqhdf/sql/new');
                console.log('2. Copy SQL from CREATE_TABLES.sql');
                console.log('3. Paste and click Run');
                console.log('');
                console.log('Or run: SETUP_SUPABASE_AUTO.bat');
            } else {
                console.log('❌ Error:', error.message);
            }
        } else {
            console.log('✅ Connection successful!');
            console.log('✅ Tables exist!');
            console.log('✅ Ready to use!');
            console.log('');
            console.log('Start your backend: node server.js');
        }
    } catch (err) {
        console.log('❌ Connection failed:', err.message);
    }
}

testConnection();
