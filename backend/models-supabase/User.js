// --- Supabase Model: User.js ---

const { supabase } = require('../config/supabase');
const bcrypt = require('bcrypt');

class User {
    // Create a new user
    static async create(userData) {
        try {
            // Hash password before storing
            const salt = await bcrypt.genSalt(10);
            const hashedPassword = await bcrypt.hash(userData.password, salt);

            const { data, error } = await supabase
                .from('users')
                .insert([{
                    name: userData.name,
                    email: userData.email.toLowerCase(),
                    role: userData.role,
                    password: hashedPassword,
                    phone: userData.phone || null,
                    auth_method: userData.authMethod || 'email_pass_demo'
                }])
                .select()
                .single();

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Error creating user:', error);
            throw error;
        }
    }

    // Find user by email
    static async findByEmail(email) {
        try {
            const { data, error } = await supabase
                .from('users')
                .select('*')
                .eq('email', email.toLowerCase())
                .single();

            if (error && error.code !== 'PGRST116') throw error; // PGRST116 = no rows returned
            return data;
        } catch (error) {
            console.error('Error finding user by email:', error);
            throw error;
        }
    }

    // Find user by ID
    static async findById(id) {
        try {
            const { data, error } = await supabase
                .from('users')
                .select('*')
                .eq('id', id)
                .single();

            if (error && error.code !== 'PGRST116') throw error;
            return data;
        } catch (error) {
            console.error('Error finding user by ID:', error);
            throw error;
        }
    }

    // Compare password
    static async comparePassword(candidatePassword, hashedPassword) {
        try {
            return await bcrypt.compare(candidatePassword, hashedPassword);
        } catch (error) {
            console.error('Error comparing passwords:', error);
            throw new Error('Error comparing passwords');
        }
    }

    // Get public profile (exclude sensitive data)
    static getPublicProfile(user) {
        if (!user) return null;
        
        return {
            id: user.id,
            name: user.name,
            email: user.email,
            role: user.role,
            phone: user.phone,
            memberSince: user.member_since,
            createdAt: user.created_at,
            displayIdentifier: user.name.split(' ')[0] || user.id.substring(0, 6) + '...'
        };
    }

    // Update user
    static async update(id, updates) {
        try {
            // If password is being updated, hash it
            if (updates.password) {
                const salt = await bcrypt.genSalt(10);
                updates.password = await bcrypt.hash(updates.password, salt);
            }

            const { data, error } = await supabase
                .from('users')
                .update(updates)
                .eq('id', id)
                .select()
                .single();

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Error updating user:', error);
            throw error;
        }
    }

    // Delete user
    static async delete(id) {
        try {
            const { error } = await supabase
                .from('users')
                .delete()
                .eq('id', id);

            if (error) throw error;
            return true;
        } catch (error) {
            console.error('Error deleting user:', error);
            throw error;
        }
    }

    // Get all users (with optional filters)
    static async findAll(filters = {}) {
        try {
            let query = supabase.from('users').select('*');

            if (filters.role) {
                query = query.eq('role', filters.role);
            }

            const { data, error } = await query;

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Error finding all users:', error);
            throw error;
        }
    }
}

module.exports = User;
