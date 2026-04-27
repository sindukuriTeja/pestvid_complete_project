// --- Supabase Model: Listing.js ---

const { supabase } = require('../config/supabase');

class Listing {
    // Create a new listing
    static async create(listingData) {
        try {
            const { data, error } = await supabase
                .from('listings')
                .insert([{
                    farmer_wallet: listingData.farmerWallet,
                    crop: listingData.crop,
                    location: listingData.location,
                    pesticide: listingData.pesticide || null,
                    pesticide_company: listingData.pesticideCompany || null,
                    cid: listingData.cid,
                    storage_type: listingData.storageType || 'ipfs',
                    video_file_hash: listingData.videoFileHash || null,
                    min_price: listingData.minPrice,
                    max_price: listingData.maxPrice,
                    status: listingData.status || 'active',
                    tx_hash: listingData.txHash || null
                }])
                .select()
                .single();

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Error creating listing:', error);
            throw error;
        }
    }

    // Find listing by ID
    static async findById(id) {
        try {
            const { data, error } = await supabase
                .from('listings')
                .select('*')
                .eq('id', id)
                .single();

            if (error && error.code !== 'PGRST116') throw error;
            return data;
        } catch (error) {
            console.error('Error finding listing by ID:', error);
            throw error;
        }
    }

    // Find listings by farmer
    static async findByFarmer(farmerWallet) {
        try {
            const { data, error } = await supabase
                .from('listings')
                .select('*')
                .eq('farmer_wallet', farmerWallet)
                .order('created_at', { ascending: false });

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Error finding listings by farmer:', error);
            throw error;
        }
    }

    // Find active listings
    static async findActive() {
        try {
            const { data, error } = await supabase
                .from('listings')
                .select('*')
                .eq('status', 'active')
                .order('created_at', { ascending: false });

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Error finding active listings:', error);
            throw error;
        }
    }

    // Get all listings
    static async findAll(filters = {}) {
        try {
            let query = supabase.from('listings').select('*');

            if (filters.farmerWallet) {
                query = query.eq('farmer_wallet', filters.farmerWallet);
            }
            if (filters.status) {
                query = query.eq('status', filters.status);
            }
            if (filters.crop) {
                query = query.ilike('crop', `%${filters.crop}%`);
            }
            if (filters.location) {
                query = query.ilike('location', `%${filters.location}%`);
            }

            query = query.order('created_at', { ascending: false });

            const { data, error } = await query;

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Error finding all listings:', error);
            throw error;
        }
    }

    // Update listing
    static async update(id, updates) {
        try {
            const { data, error } = await supabase
                .from('listings')
                .update(updates)
                .eq('id', id)
                .select()
                .single();

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Error updating listing:', error);
            throw error;
        }
    }

    // Update listing status
    static async updateStatus(id, status) {
        return await this.update(id, { status });
    }

    // Delete listing
    static async delete(id) {
        try {
            const { error } = await supabase
                .from('listings')
                .delete()
                .eq('id', id);

            if (error) throw error;
            return true;
        } catch (error) {
            console.error('Error deleting listing:', error);
            throw error;
        }
    }

    // Find listing by CID
    static async findByCid(cid) {
        try {
            const { data, error } = await supabase
                .from('listings')
                .select('*')
                .eq('cid', cid)
                .eq('status', 'active')
                .single();

            if (error && error.code !== 'PGRST116') throw error;
            return data;
        } catch (error) {
            console.error('Error finding listing by CID:', error);
            throw error;
        }
    }
}

module.exports = Listing;
