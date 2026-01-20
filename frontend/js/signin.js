const USER_KEY = "voiceAppUser";
const USERS_KEY = "registeredUsers";

// Admin credentials
const ADMIN_CREDENTIALS = {
    email: 'admin@raketh.com',
    password: 'admin123'
};

// Get all registered users (fallback)
function getRegisteredUsers() {
    return JSON.parse(localStorage.getItem(USERS_KEY) || '[]');
}

// Check admin login
function checkAdminLogin(email, password) {
    if (email === ADMIN_CREDENTIALS.email && password === ADMIN_CREDENTIALS.password) {
        sessionStorage.setItem('adminAuth', 'true');
        return true;
    }
    return false;
}

document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("form");
  const userInput = document.getElementById("user");
  const passInput = document.getElementById("pass");
  const formErr = document.getElementById("formErr");

  if (!form) return;

  form.addEventListener("submit", async function(e) {
    e.preventDefault();
    
    const email = userInput.value.trim();
    const password = passInput.value;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Clear previous errors
    formErr.textContent = '';
    
    // Show loading state
    if (submitBtn) {
      submitBtn.textContent = 'Signing in...';
      submitBtn.disabled = true;
    }
    
    try {
      // Check if admin credentials
      if (checkAdminLogin(email, password)) {
        // Store admin token for API calls
        const adminToken = 'admin_' + btoa(email + ':' + password);
        localStorage.setItem('jwt_token', adminToken);
        localStorage.setItem('user_type', 'admin');
        
        console.log('Admin login successful');
        window.location.replace("admin-dashboard.html");
        return;
      }
      
      // API call for user login
      const credentials = {
        email: email,
        password: password
      };
      
      const response = await API.login(credentials);
      
      // Store JWT token
      if (response.token) {
        localStorage.setItem('jwt_token', response.token);
      }
      
      // Store user data with name from signup or email
      const existingUsers = JSON.parse(localStorage.getItem('registeredUsers') || '[]');
      const existingUser = existingUsers.find(u => u.email === email);
      const userName = existingUser ? existingUser.name : email.split('@')[0];
      
      localStorage.setItem(USER_KEY, JSON.stringify({
        name: userName,
        email: email,
        loginAt: new Date().toISOString()
      }));
      
      console.log('User login successful');
      window.location.replace("index.html");
      
    } catch (error) {
      console.error('Login error:', error);
      formErr.textContent = error.message || "Login failed. Please check your credentials.";
      formErr.style.color = "red";
    } finally {
      // Reset button state
      if (submitBtn) {
        submitBtn.textContent = 'Sign In';
        submitBtn.disabled = false;
      }
    }
  });
});
