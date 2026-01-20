document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("form");
  const userInput = document.getElementById("user");
  const passInput = document.getElementById("pass");
  const formErr = document.getElementById("formErr");

  if (!form) return;

  form.addEventListener("submit", function(e) {
    e.preventDefault();
    
    const email = userInput.value.trim().toLowerCase();
    const password = passInput.value;
    
    // Clear previous errors
    formErr.textContent = "";
    
    // Check if admin credentials
    if (email === 'admin@raketh.com' && password === 'admin123') {
      sessionStorage.setItem('adminAuth', 'true');
      window.location.replace("admin-dashboard.html");
      return;
    }
    
    // Get registered users
    const users = JSON.parse(localStorage.getItem('registeredUsers') || '[]');
    
    // Find user
    const user = users.find(u => u.email.toLowerCase() === email && u.password === password);
    
    if (user) {
      localStorage.setItem('voiceAppUser', JSON.stringify(user));
      window.location.replace("index.html");
    } else {
      formErr.textContent = "Incorrect email or password.";
      formErr.style.color = "red";
    }
  });
});