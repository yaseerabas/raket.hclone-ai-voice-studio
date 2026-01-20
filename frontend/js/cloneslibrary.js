// Clones Library JavaScript

// Function to create new clone
function createNewClone() {
  document.getElementById('createCloneModal').style.display = 'block';
}

// Function to close create clone modal
function closeCreateCloneModal() {
  document.getElementById('createCloneModal').style.display = 'none';
  document.getElementById('createCloneForm').reset();
  document.getElementById('fileName').textContent = '';
}

// Function to handle file upload
function handleFileUpload(input) {
  const file = input.files[0];
  const fileName = document.getElementById('fileName');
  
  if (file) {
    // Check file size (25MB = 25 * 1024 * 1024 bytes)
    const maxSize = 25 * 1024 * 1024;
    
    if (file.size > maxSize) {
      alert('File size must be less than 25MB!');
      input.value = '';
      fileName.textContent = '';
      return;
    }
    
    // Check file type
    const allowedTypes = ['audio/mp3', 'audio/wav', 'audio/x-m4a', 'audio/mp4'];
    if (!allowedTypes.includes(file.type) && !file.name.match(/\.(mp3|wav|m4a)$/i)) {
      alert('Please upload MP3, WAV, or M4A files only!');
      input.value = '';
      fileName.textContent = '';
      return;
    }
    
    fileName.textContent = `Selected: ${file.name} (${(file.size / (1024 * 1024)).toFixed(2)} MB)`;
  }
}

// Handle form submission with API integration
document.addEventListener('DOMContentLoaded', function() {
  // Load existing clones from API
  loadExistingClones();
  
  document.getElementById('createCloneForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const cloneName = document.getElementById('cloneName').value;
    const gender = document.querySelector('input[name="gender"]:checked')?.value;
    const language = document.getElementById('cloneLanguage').value;
    const voiceFile = document.getElementById('voiceFile').files[0];
    
    if (!cloneName || !gender || !language || !voiceFile) {
      alert('Please fill all required fields!');
      return;
    }
    
    // Show loading state
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Creating Clone...';
    submitBtn.disabled = true;
    
    try {
      // Create FormData for file upload
      const formData = new FormData();
      formData.append('voice_file', voiceFile);
      formData.append('voice_name', cloneName);
      
      // API call to clone voice
      const response = await API.cloneVoice(formData);
      
      // Create new clone card
      createCloneCard(cloneName, gender, language, response.clone_id);
      
      // Close modal
      closeCreateCloneModal();
      
      alert(`Voice clone "${cloneName}" created successfully!`);
      
    } catch (error) {
      console.error('Clone creation error:', error);
      alert(error.message || 'Failed to create voice clone. Please try again.');
    } finally {
      // Reset button state
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    }
  });
});

// Function to create new clone card with API integration
function createCloneCard(name, gender, language, cloneId = null) {
  const clonesGrid = document.querySelector('.clones-grid');
  
  const cloneCard = document.createElement('div');
  cloneCard.className = 'clone-card';
  cloneCard.setAttribute('data-clone-id', cloneId || name.toLowerCase().replace(/\s+/g, '-'));
  cloneCard.innerHTML = `
    <div class="clone-header">
      <div class="clone-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#4ecca3" stroke-width="2">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
        </svg>
      </div>
      <h3 class="clone-name">${name}</h3>
      <button class="delete-btn" onclick="deleteClone('${name}', '${cloneId}')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="3,6 5,6 21,6"></polyline>
          <path d="M19,6v14a2,2 0 0,1-2,2H7a2,2 0 0,1-2-2V6m3,0V4a2,2 0 0,1,2-2h4a2,2 0 0,1,2,2v2"></path>
        </svg>
      </button>
    </div>
    <div class="clone-details">
      <div class="clone-info">
        <span class="info-label">Gender</span>
        <span class="info-value">${gender}</span>
      </div>
      <div class="clone-info">
        <span class="info-label">Language</span>
        <span class="info-value">${getLanguageName(language)}</span>
      </div>
      <div class="clone-feature">
        <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="#4ecca3" stroke-width="2">
          <polygon points="12 2 15.09 8.26 22 9 17 14.74 18.18 21.02 12 17.77 5.82 21.02 7 14.74 2 9 8.91 8.26 12 2"></polygon>
        </svg>
        <span>Ultra-Realistic Voice Enabled</span>
      </div>
    </div>
  `;
  
  clonesGrid.appendChild(cloneCard);
  
  // Update dashboard dropdown
  updateDashboardDropdown(name, gender, cloneId);
}

// Function to update dashboard dropdown with new clone
function updateDashboardDropdown(name, gender) {
  // Note: We rely on server-side storage only now, no client-side storage
  // The API will handle storing and retrieving user-specific voice clones
}

// Function to update profile UI
function updateProfileUI() {
  const user = JSON.parse(localStorage.getItem('voiceAppUser') || '{}');
  if (user.name) {
    document.getElementById('welcomeMessage').textContent = `Welcome, ${user.name}`;
    
    const profilePic = document.getElementById('profilePic');
    if (user.profilePic) {
      profilePic.style.backgroundImage = `url(${user.profilePic})`;
      profilePic.style.backgroundSize = 'cover';
      profilePic.style.backgroundPosition = 'center';
      profilePic.textContent = '';
    } else {
      profilePic.textContent = user.name.charAt(0).toUpperCase();
    }
  }
}

// Function to get language name from code
function getLanguageName(code) {
  const languages = {
    'en-us': 'English (US)',
    'en-uk': 'English (UK)',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'ur': 'Urdu',
    'tr': 'Turkish',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'no': 'Norwegian',
    'da': 'Danish',
    'fi': 'Finnish'
  };
  return languages[code] || code;
}

// Function to delete clone with API integration
async function deleteClone(cloneName, cloneId) {
  if (confirm(`Are you sure you want to delete "${cloneName}" voice clone?`)) {
    try {
      // If cloneId exists, call backend API
      if (cloneId && cloneId !== cloneName.toLowerCase().replace(/\s+/g, '-')) {
        await API.request(`/voice/voices/${cloneId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            ...API.getAuthHeaders()
          }
        });
      }
      
      // Find and remove the clone card
      const cloneCards = document.querySelectorAll('.clone-card');
      cloneCards.forEach(card => {
        const nameElement = card.querySelector('.clone-name');
        if (nameElement && nameElement.textContent.trim() === cloneName) {
          // Add fade out animation
          card.style.transition = 'all 0.3s ease';
          card.style.opacity = '0';
          card.style.transform = 'scale(0.8)';
          
          // Remove after animation
          setTimeout(() => {
            card.remove();
          }, 300);
        }
      });
      
      // LocalStorage removal is no longer needed - server handles this
      
      console.log(`Deleted clone: ${cloneName}`);
      
    } catch (error) {
      console.error('Delete clone error:', error);
      alert('Failed to delete voice clone: ' + error.message);
    }
  }
}

// Function to go back to dashboard
function goToDashboard() {
  window.location.href = 'dashboard.html';
}

// Function to download cloned voice
async function downloadClone(voiceId, voiceName) {
  try {
    const token = localStorage.getItem('jwt_token');
    if (!token) {
      alert('Please login to download voice files.');
      window.location.href = 'signin.html';
      return;
    }

    const response = await fetch(`${API_CONFIG.BASE_URL}/voice/voices/${voiceId}/download`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token.replace('Bearer ', '')}`,
        'Accept': 'audio/wav, application/octet-stream'
      }
    });

    if (!response.ok) {
      if (response.status === 401) {
        alert('Session expired. Please login again.');
        localStorage.removeItem('jwt_token');
        window.location.href = 'signin.html';
        return;
      }
      throw new Error(`Download failed: ${response.status}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${voiceName}.wav`;
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);

    alert('Voice downloaded successfully!');

  } catch (error) {
    console.error('Download error:', error);
    alert('Failed to download voice file: ' + error.message);
  }
}

// Function to go home (logout)
function goHome() {
  if (confirm('Are you sure you want to logout?')) {
    localStorage.removeItem('voiceAppUser');
    window.location.href = 'index.html';
  }
}

// Function to open profile modal (if needed)
function openProfileModal() {
  // Redirect to dashboard or implement profile modal
  window.location.href = 'dashboard.html';
}

// Initialize page on load
document.addEventListener('DOMContentLoaded', function() {
  updateProfileUI();
  loadSavedClones();
  
  // Add hover effects to clone cards
  const cloneCards = document.querySelectorAll('.clone-card');
  cloneCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-5px)';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });
});

// Function to load saved clones from API and localStorage
async function loadSavedClones() {
  try {
    // Load from API first
    const apiClones = await API.request('/voice/voices', {
      method: 'GET',
      headers: API.getAuthHeaders()
    });
    const clonesGrid = document.querySelector('.clones-grid');
    
    // Clear existing clones
    clonesGrid.innerHTML = '';
    
    // Add API clones
    apiClones.forEach(clone => {
      const cloneCard = document.createElement('div');
      cloneCard.className = 'clone-card';
      cloneCard.setAttribute('data-clone-id', clone.id);
      cloneCard.innerHTML = `
        <div class="clone-header">
          <div class="clone-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="#4ecca3" stroke-width="2">
              <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
              <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            </svg>
          </div>
          <h3 class="clone-name">${clone.voice_name}</h3>
          <div class="clone-actions">
            <button class="download-btn" onclick="downloadClone('${clone.id}', '${clone.voice_name}')">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7,10 12,15 17,10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
            </button>
            <button class="delete-btn" onclick="deleteClone('${clone.voice_name}', '${clone.id}')">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3,6 5,6 21,6"></polyline>
                <path d="M19,6v14a2,2 0 0,1-2,2H7a2,2 0 0,1-2-2V6m3,0V4a2,2 0 0,1,2-2h4a2,2 0 0,1,2,2v2"></path>
              </svg>
            </button>
          </div>
        </div>
        <div class="clone-details">
          <div class="clone-info">
            <span class="info-label">Voice ID</span>
            <span class="info-value">${clone.id}</span>
          </div>
          <div class="clone-info">
            <span class="info-label">Status</span>
            <span class="info-value">Active</span>
          </div>
          <div class="clone-feature">
            <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="#4ecca3" stroke-width="2">
              <polygon points="12 2 15.09 8.26 22 9 17 14.74 18.18 21.02 12 17.77 5.82 21.02 7 14.74 2 9 8.91 8.26 12 2"></polygon>
            </svg>
            <span>Ultra-Realistic Voice Enabled</span>
          </div>
        </div>
      `;
      
      clonesGrid.appendChild(cloneCard);
    });
    
  } catch (error) {
    console.error('Failed to load voice clones from API:', error);
    alert('Failed to load voice clones: ' + error.message);
  }
}

// Load existing clones from API on page load
async function loadExistingClones() {
  try {
    const token = localStorage.getItem('jwt_token');
    if (!token) {
      console.log('No token found, redirecting to login');
      window.location.href = 'signin.html';
      return;
    }

    const response = await fetch(`${API_CONFIG.BASE_URL}/voice/voices`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token.replace('Bearer ', '')}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('jwt_token');
      alert('Session expired. Please login again.');
      window.location.href = 'signin.html';
      return;
    }

    if (!response.ok) {
      throw new Error('Failed to load clones');
    }

    const clones = await response.json();
    const clonesGrid = document.querySelector('.clones-grid');
    
    // Clear existing dynamic clones (keep static ones if any)
    const existingCards = clonesGrid.querySelectorAll('.clone-card[data-dynamic="true"]');
    existingCards.forEach(card => card.remove());
    
    // Display message if no clones
    if (clones.length === 0) {
      const emptyMessage = document.createElement('div');
      emptyMessage.className = 'empty-state';
      emptyMessage.style.cssText = 'grid-column: 1/-1; text-align: center; padding: 40px; color: #999;';
      emptyMessage.innerHTML = `
        <svg style="width: 64px; height: 64px; margin: 0 auto 20px; opacity: 0.5;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
        </svg>
        <h3>No Voice Clones Yet</h3>
        <p>Create your first voice clone to get started!</p>
      `;
      clonesGrid.appendChild(emptyMessage);
      return;
    }
    
    // Add user's clones to the grid
    clones.forEach(clone => {
      const cloneCard = document.createElement('div');
      cloneCard.className = 'clone-card';
      cloneCard.setAttribute('data-dynamic', 'true');
      cloneCard.setAttribute('data-clone-id', clone.id);
      cloneCard.innerHTML = `
        <div class="clone-header">
          <div class="clone-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="#4ecca3" stroke-width="2">
              <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
              <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            </svg>
          </div>
          <h3 class="clone-name">${clone.voice_name}</h3>
          <button class="delete-btn" onclick="deleteCloneById(${clone.id})">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3,6 5,6 21,6"></polyline>
              <path d="M19,6v14a2,2 0 0,1-2,2H7a2,2 0 0,1-2-2V6m3,0V4a2,2 0 0,1,2-2h4a2,2 0 0,1,2,2v2"></path>
            </svg>
          </button>
        </div>
        <div class="clone-details">
          <div class="clone-info">
            <span class="info-label">Speaker ID</span>
            <span class="info-value">${clone.speaker_id || 'N/A'}</span>
          </div>
          <div class="clone-info">
            <span class="info-label">Created</span>
            <span class="info-value">${new Date(clone.created_at || Date.now()).toLocaleDateString()}</span>
          </div>
          <div class="clone-feature">
            <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="#4ecca3" stroke-width="2">
              <polygon points="12 2 15.09 8.26 22 9 17 14.74 18.18 21.02 12 17.77 5.82 21.02 7 14.74 2 9 8.91 8.26 12 2"></polygon>
            </svg>
            <span>Ultra-Realistic Voice Enabled</span>
          </div>
        </div>
      `;
      
      clonesGrid.appendChild(cloneCard);
    });

    console.log(`Loaded ${clones.length} voice clones for current user`);

  } catch (error) {
    console.error('Failed to load existing clones:', error);
    alert('Failed to load your voice clones. Please try refreshing the page.');
  }
}

// Delete clone by ID
async function deleteCloneById(cloneId) {
  if (!confirm('Are you sure you want to delete this voice clone?')) {
    return;
  }

  try {
    const token = localStorage.getItem('jwt_token');
    if (!token) {
      alert('Please login to delete clones');
      return;
    }

    const response = await fetch(`${API_CONFIG.BASE_URL}/voice/voices/${cloneId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token.replace('Bearer ', '')}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error('Failed to delete clone');
    }

    alert('Voice clone deleted successfully!');
    location.reload(); // Reload to refresh the list

  } catch (error) {
    console.error('Failed to delete clone:', error);
    alert('Failed to delete voice clone. Please try again.');
  }
}