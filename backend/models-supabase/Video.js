// --- Supabase Model: Video.js ---

const { supabase } = require('../config/supabase');

class Video {
    // Create a new video
    static async create(videoData) {
        try {
            const { data, error } = await supabase
                .from('videos')
                .insert([{
                    cid: videoData.cid,
                    storage_type: videoData.storageType || 'ipfs',
                    video_file_hash: videoData.videoFileHash || null,
                    farmer_wallet: videoData.farmerWallet,
                    crop: videoData.crop,
                    pesticide: videoData.pesticide || null,
                    location: videoData.location,
                    pesticide_company: videoData.pesticideCompany || null,
                    purpose: videoData.purpose || 'agristream'
                }])
                .select()
                .single();

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Error creating video:', error);
            throw error;
        }
    }

    // Find video by CID
    static async findByCid(cid) {
        try {
            const { data, error } = await supabase
                .from('videos')
                .select('*')
                .eq('cid', cid)
                .single();

            if (error && error.code !== 'PGRST116') throw error;
            return data;
        } catch (error) {
            console.error('Error finding video by CID:', error);
            throw error;
        }
    }

    // Find video by ID
    static async findById(id) {
        try {
            const { data, error } = await supabase
                .from('videos')
                .select('*')
                .eq('id', id)
                .single();

            if (error && error.code !== 'PGRST116') throw error;
            return data;
        } catch (error) {
            console.error('Error finding video by ID:', error);
            throw error;
        }
    }

    // Find videos by farmer
    static async findByFarmer(farmerWallet) {
        try {
            const { data, error } = await supabase
                .from('videos')
                .select('*')
                .eq('farmer_wallet', farmerWallet)
                .order('upload_timestamp', { ascending: false });

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Error finding videos by farmer:', error);
            throw error;
        }
    }

    // Find videos by purpose
    static async findByPurpose(purpose) {
        try {
            const { data, error } = await supabase
                .from('videos')
                .select('*')
                .eq('purpose', purpose)
                .order('upload_timestamp', { ascending: false });

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Error finding videos by purpose:', error);
            throw error;
        }
    }

    // Get all videos
    static async findAll(filters = {}) {
        try {
            let query = supabase.from('videos').select('*');

            if (filters.farmerWallet) {
                query = query.eq('farmer_wallet', filters.farmerWallet);
            }
            if (filters.purpose) {
                query = query.eq('purpose', filters.purpose);
            }
            if (filters.crop) {
                query = query.ilike('crop', `%${filters.crop}%`);
            }

            query = query.order('upload_timestamp', { ascending: false });

            const { data, error } = await query;

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Error finding all videos:', error);
            throw error;
        }
    }

    // Update video
    static async update(id, updates) {
        try {
            const { data, error } = await supabase
                .from('videos')
                .update(updates)
                .eq('id', id)
                .select()
                .single();

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Error updating video:', error);
            throw error;
        }
    }

    // Delete video
    static async delete(id) {
        try {
            const { error } = await supabase
                .from('videos')
                .delete()
                .eq('id', id);

            if (error) throw error;
            return true;
        } catch (error) {
            console.error('Error deleting video:', error);
            throw error;
        }
    }
}

module.exports = Video;
