// API Configuration
const API_CONFIG = {
    BASE_URL: 'http://127.0.0.1:5000/api',
    ENDPOINTS: {
        AUTH: {
            SIGNUP: '/auth/register',
            LOGIN: '/auth/login'
        },
        ADMIN: {
            ASSIGN_PLAN: '/admin/assign-plan',
            SUBSCRIPTION_USERS: '/admin/subscription-users'
        },
        USER: {
            DASHBOARD: '/user/dashboard'
        },
        TTS: {
            GENERATE_FULL: '/voice/generate-full',
            GENERATE: '/voice/generate',
            CLONE_VOICE: '/voice/clone-voice',
            LIST_VOICES: '/voice/voices',
            DOWNLOAD_AUDIO: '/voice/download'
        },
        TRANSLATION: {
            TRANSLATE: '/translate/translate'
        }
    }
};

// API Helper Functions
const API = {
    // Make API request
    async request(endpoint, options = {}) {
        const url = API_CONFIG.BASE_URL + endpoint;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);

            // Check if response is ok
            if (!response.ok) {
                // Try to get error message from response
                let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.message || errorData.error || errorMessage;
                } catch (e) {
                    // If response is not JSON, use status text
                }
                throw new Error(errorMessage);
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error('API Error:', error);
            // Network error or other issues
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                throw new Error('Network error: Please check if the backend server is running');
            }
            throw error;
        }
    },

    // Auth APIs
    async signup(userData) {
        return this.request(API_CONFIG.ENDPOINTS.AUTH.SIGNUP, {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    },

    async login(credentials) {
        return this.request(API_CONFIG.ENDPOINTS.AUTH.LOGIN, {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
    },

    // Get auth headers with JWT token
    getAuthHeaders() {
        const token = localStorage.getItem('jwt_token');
        if (token) {
            // Remove 'Bearer ' prefix if it exists, we'll add it properly
            const cleanToken = token.replace('Bearer ', '');
            return { 'Authorization': `Bearer ${cleanToken}` };
        }
        return {};
    },

    // User Dashboard API
    async getUserDashboard() {
        return this.request(API_CONFIG.ENDPOINTS.USER.DASHBOARD, {
            method: 'GET',
            headers: this.getAuthHeaders()
        });
    },

    // TTS APIs
    async generateTTS(ttsData) {
        return this.request(API_CONFIG.ENDPOINTS.TTS.GENERATE_FULL, {
            method: 'POST',
            headers: this.getAuthHeaders(),
            body: JSON.stringify(ttsData)
        });
    },

    // Admin API
    async assignPlan(planData) {
        return this.request('/admin/assign-plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(planData)
        });
    },

    // Clone Voice API (FormData)
    async cloneVoice(formData) {
        const url = API_CONFIG.BASE_URL + API_CONFIG.ENDPOINTS.TTS.CLONE_VOICE;
        const headers = this.getAuthHeaders();
        // Don't set Content-Type for FormData, browser will set it automatically

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: headers,
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'API request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    async listVoices(searchQuery = '') {
        const url = searchQuery ?
            `${API_CONFIG.ENDPOINTS.TTS.LIST_VOICES}?search=${searchQuery}` :
            API_CONFIG.ENDPOINTS.TTS.LIST_VOICES;

        return this.request(url, {
            method: 'GET',
            headers: this.getAuthHeaders()
        });
    },

    async downloadAudio(audioId) {
        const url = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.TTS.DOWNLOAD_AUDIO}/${audioId}`;
        const headers = this.getAuthHeaders();

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    ...headers,
                    'Accept': 'audio/mpeg, audio/mp3, application/octet-stream'
                }
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.message || `Download failed: ${response.status}`);
            }

            return await response.blob();
        } catch (error) {
            console.error('Download API Error:', error);
            throw error;
        }
    },

    // Translation API
    async translateText(translationData) {
        return this.request(API_CONFIG.ENDPOINTS.TRANSLATION.TRANSLATE, {
            method: 'POST',
            headers: this.getAuthHeaders(),
            body: JSON.stringify(translationData)
        });
    }
};