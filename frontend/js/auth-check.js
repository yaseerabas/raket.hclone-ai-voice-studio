(function() {
  const user = localStorage.getItem('voiceAppUser');
  const authButtons = document.querySelector('.nav-auth-buttons');
  const userInfo = document.getElementById('userInfo');
  
  if (user && authButtons) {
    // Update desktop nav buttons
    authButtons.innerHTML = '<a href="dashboard.html" class="nav-signin">Dashboard</a><a href="#" class="nav-signup" onclick="localStorage.removeItem(\'voiceAppUser\'); window.location.href=\'index.html\'">Logout</a>';
    
    // Update mobile nav if exists
    const mobileNav = document.getElementById('mobileNav');
    if (mobileNav) {
      mobileNav.innerHTML = `
        <a href="index.html" class="mobile-nav-item">Home</a>
        <a href="services.html" class="mobile-nav-item">Services</a>
        <a href="pricing.html" class="mobile-nav-item">Pricing</a>
        <a href="contact.html" class="mobile-nav-item">Contact</a>
        <a href="dashboard.html" class="mobile-nav-item">Dashboard</a>
        <a href="#" class="mobile-nav-item" onclick="localStorage.removeItem('voiceAppUser'); window.location.href='index.html'">Logout</a>
      `;
    }
  }
})();
