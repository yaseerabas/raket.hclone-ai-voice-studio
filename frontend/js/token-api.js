// Token consumption API simulation
class TokenAPI {
    constructor() {
        this.subscriptions = this.loadSubscriptions();
    }
    
    loadSubscriptions() {
        const stored = localStorage.getItem('subscriptions');
        const dummy = [
            {
                id: 1,
                email: 'john@example.com',
                plan: 'Middle Plan',
                tokens: 450,
                startDate: '2025-01-01',
                expiryDate: '2025-02-01',
                status: 'Active'
            },
            {
                id: 2,
                email: 'sarah@example.com',
                plan: 'High Plan',
                tokens: 800,
                startDate: '2025-01-05',
                expiryDate: '2025-02-05',
                status: 'Active'
            }
        ];
        
        if (stored) {
            return [...dummy, ...JSON.parse(stored)];
        }
        return dummy;
    }
    
    saveSubscriptions() {
        const userSubs = this.subscriptions.filter(s => s.createdAt);
        localStorage.setItem('subscriptions', JSON.stringify(userSubs));
    }
    
    // Consume token for a user
    consumeToken(email) {
        const user = this.subscriptions.find(s => s.email === email && s.status === 'Active');
        
        if (!user) {
            return { error: 'No active subscription found', success: false };
        }
        
        if (user.tokens <= 0) {
            user.status = 'Expired';
            this.saveSubscriptions();
            return { error: 'No tokens remaining', success: false };
        }
        
        user.tokens--;
        
        if (user.tokens === 0) {
            user.status = 'Expired';
        }
        
        this.saveSubscriptions();
        
        return {
            success: true,
            tokensRemaining: user.tokens,
            status: user.status,
            message: `Token consumed. ${user.tokens} tokens remaining.`
        };
    }
    
    // Get user subscription info
    getUserInfo(email) {
        const user = this.subscriptions.find(s => s.email === email);
        
        if (!user) {
            return { error: 'User not found', success: false };
        }
        
        return {
            success: true,
            user: {
                email: user.email,
                plan: user.plan,
                tokens: user.tokens,
                status: user.status,
                startDate: user.startDate,
                expiryDate: user.expiryDate
            }
        };
    }
    
    // Check if user can use service
    canUseService(email) {
        const user = this.subscriptions.find(s => s.email === email);
        
        if (!user) {
            return { canUse: false, reason: 'No subscription found' };
        }
        
        if (user.status !== 'Active') {
            return { canUse: false, reason: 'Subscription not active' };
        }
        
        if (user.tokens <= 0) {
            return { canUse: false, reason: 'No tokens remaining' };
        }
        
        const now = new Date();
        const expiryDate = new Date(user.expiryDate);
        
        if (now > expiryDate) {
            user.status = 'Expired';
            this.saveSubscriptions();
            return { canUse: false, reason: 'Subscription expired' };
        }
        
        return { canUse: true, tokens: user.tokens };
    }
}

// Global instance
window.tokenAPI = new TokenAPI();

// Example usage functions
function simulateVoiceGeneration(userEmail) {
    const canUse = window.tokenAPI.canUseService(userEmail);
    
    if (!canUse.canUse) {
        alert(`Cannot generate voice: ${canUse.reason}`);
        return false;
    }
    
    const result = window.tokenAPI.consumeToken(userEmail);
    
    if (result.success) {
        alert(`Voice generated successfully! ${result.message}`);
        return true;
    } else {
        alert(`Error: ${result.error}`);
        return false;
    }
}

// Auto-check expired subscriptions every minute
setInterval(() => {
    const api = window.tokenAPI;
    api.subscriptions.forEach(user => {
        if (user.status === 'Active') {
            const now = new Date();
            const expiryDate = new Date(user.expiryDate);
            
            if (now > expiryDate) {
                user.status = 'Expired';
            }
        }
    });
    api.saveSubscriptions();
}, 60000);

console.log('Token API loaded successfully!');