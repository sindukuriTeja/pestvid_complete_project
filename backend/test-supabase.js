// Quick test to verify Supabase connection

require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_KEY || process.env.SUPABASE_ANON_KEY;

console.log('\n🔍 Testing Supabase Connection...\n');
console.log('URL:', supabaseUrl);
console.log('Key:', supabaseKey ? supabaseKey.substring(0, 20) + '...' : 'NOT FOUND');

if (!supabaseUrl || !supabaseKey) {
    console.error('\n❌ ERROR: Missing Supabase credentials in .env file!');
    console.log('\nPlease add to backend/.env:');
    console.log('SUPABASE_URL=https://zdkeisiffbncmvonqhdf.supabase.co');
    console.log('SUPABASE_ANON_KEY=sb_publishable_M_An6qNKEZom2BJg13B-SA_PR8Q-kvx');
    console.log('SUPABASE_SERVICE_KEY=your_service_role_key_here\n');
    process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function testConnection() {
    try {
        // Try to query the users table
        const { data, error, count } = await supabase
            .from('users')
            .select('*', { count: 'exact', head: true });

        if (error) {
            if (error.message.includes('relation "public.users" does not exist')) {
                console.log('⚠️  Database tables not created yet!');
                console.log('\n📝 Next step: Create tables in Supabase');
                console.log('   1. Go to Supabase Dashboard');
                console.log('   2. Click SQL Editor');
                console.log('   3. Run the SQL from SUPABASE_SETUP_NOW.md\n');
                return;
            }
            throw error;
        }

        console.log('✅ Supabase connection successful!');
        console.log(`📊 Users table exists (${count || 0} records)`);
        console.log('\n🎉 Your backend is ready to use Supabase!\n');

    } catch (error) {
        console.error('\n❌ Connection failed:', error.message);
        console.log('\n💡 Troubleshooting:');
        console.log('   1. Check your .env file has correct credentials');
        console.log('   2. Verify your Supabase project is active');
        console.log('   3. Make sure you have internet connection\n');
    }
}

testConnection();
