// Admin credentials - change these as needed
const ADMIN_CREDENTIALS = {
    email: 'admin@raketh.com',
    password: 'admin123'
};

function checkAdminLogin(email, password) {
    if (email === ADMIN_CREDENTIALS.email && password === ADMIN_CREDENTIALS.password) {
        sessionStorage.setItem('adminAuth', 'true');
        return true;
    }
    return false;
}

// Check if current user is admin
function isAdmin() {
    return sessionStorage.getItem('adminAuth') === 'true';
}

// Redirect to admin panel if admin is logged in
function redirectIfAdmin() {
    if (isAdmin()) {
        window.location.href = 'admin-dashboard.html';
    }
}