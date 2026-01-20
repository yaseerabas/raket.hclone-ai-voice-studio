// Admin settings - ye values admin dashboard se aayengi
let adminSettings = {
  maxCharacters: 60000, // Default value, admin se update hogi
  charactersRemaining: 0 // Actual remaining characters from usage
};

// Selected voice options
let selectedOptions = {
  language: 'en-us',
  maleVoice: null,
  femaleVoice: null,
  kidsVoice: null,
  voiceStyle: 'default'
};

// Language data storage
let ttsLanguages = {};
let translationLanguages = {};

// Load language data from JSON files
async function loadLanguageData() {
  try {
    // Load TTS languages (for tone)
    const ttsResponse = await fetch('tts_languages.json');
    const ttsData = await ttsResponse.json();
    ttsLanguages = ttsData.languages;
    
    // Load Translation languages (for source/target)
    const translationResponse = await fetch('translation_language.json');
    const translationData = await translationResponse.json();
    translationLanguages = translationData.languages;
    
    // Populate dropdowns after loading data
    populateToneDropdown();
    populateSourceLanguageDropdown();
    populateTargetLanguageDropdown();
    
  } catch (error) {
    console.error('Failed to load language data:', error);
  }
}

// Populate Tone dropdown with TTS languages
function populateToneDropdown() {
  const toneDropdown = document.querySelector('[data-dropdown="tone"] .dropdown-options');
  if (!toneDropdown) return;
  
  // Clear existing options except search
  const searchDiv = toneDropdown.querySelector('.dropdown-search');
  toneDropdown.innerHTML = '';
  if (searchDiv) {
    toneDropdown.appendChild(searchDiv);
  } else {
    // Add search bar if it doesn't exist
    const newSearchDiv = document.createElement('div');
    newSearchDiv.className = 'dropdown-search';
    newSearchDiv.innerHTML = '<input type="text" placeholder="Search languages..." class="language-search" />';
    toneDropdown.appendChild(newSearchDiv);
  }
  
  // Add language options
  Object.entries(ttsLanguages).forEach(([name, code]) => {
    const option = document.createElement('div');
    option.className = 'dropdown-option';
    option.setAttribute('data-value', code);
    option.textContent = name;
    toneDropdown.appendChild(option);
  });
  
  // Set default selection
  const selected = document.querySelector('[data-dropdown="tone"] .dropdown-selected span');
  if (selected && Object.keys(ttsLanguages).length > 0) {
    selected.textContent = Object.keys(ttsLanguages)[0]; // Default to first language
  }
}

// Populate Source Language dropdown
function populateSourceLanguageDropdown() {
  const sourceDropdown = document.querySelector('[data-dropdown="source-language"] .dropdown-options');
  if (!sourceDropdown) return;
  
  // Clear existing options except search
  const searchDiv = sourceDropdown.querySelector('.dropdown-search');
  sourceDropdown.innerHTML = '';
  if (searchDiv) {
    sourceDropdown.appendChild(searchDiv);
  } else {
    // Add search bar if it doesn't exist
    const newSearchDiv = document.createElement('div');
    newSearchDiv.className = 'dropdown-search';
    newSearchDiv.innerHTML = '<input type="text" placeholder="Search languages..." class="language-search" />';
    sourceDropdown.appendChild(newSearchDiv);
  }
  
  // Add language options
  Object.entries(translationLanguages).forEach(([name, code]) => {
    const option = document.createElement('div');
    option.className = 'dropdown-option';
    option.setAttribute('data-value', code);
    option.textContent = name;
    sourceDropdown.appendChild(option);
  });
  
  // Set default selection
  const selected = document.querySelector('[data-dropdown="source-language"] .dropdown-selected span');
  if (selected) {
    selected.textContent = 'Select Source Language';
  }
}

// Populate Target Language dropdown
function populateTargetLanguageDropdown() {
  const targetDropdown = document.querySelector('[data-dropdown="target-language"] .dropdown-options');
  if (!targetDropdown) return;
  
  // Clear existing options except search
  const searchDiv = targetDropdown.querySelector('.dropdown-search');
  targetDropdown.innerHTML = '';
  if (searchDiv) {
    targetDropdown.appendChild(searchDiv);
  } else {
    // Add search bar if it doesn't exist
    const newSearchDiv = document.createElement('div');
    newSearchDiv.className = 'dropdown-search';
    newSearchDiv.innerHTML = '<input type="text" placeholder="Search languages..." class="language-search" />';
    targetDropdown.appendChild(newSearchDiv);
  }
  
  // Add language options
  Object.entries(translationLanguages).forEach(([name, code]) => {
    const option = document.createElement('div');
    option.className = 'dropdown-option';
    option.setAttribute('data-value', code);
    option.textContent = name;
    targetDropdown.appendChild(option);
  });
  
  // Set default selection
  const selected = document.querySelector('[data-dropdown="target-language"] .dropdown-selected span');
  if (selected) {
    selected.textContent = 'Select Target Language';
  }
}

function updateCharacterCount() {
  const textInput = document.getElementById('textInput');
  const characterCounter = document.getElementById('characterCounter');
  const remainingCounter = document.getElementById('remainingCounter');
  
  const currentLength = textInput.value.length;
  const actualRemaining = adminSettings.charactersRemaining;
  
  // Update bottom counter only (real-time)
  characterCounter.textContent = `${currentLength} characters`;
  
  if (adminSettings.maxCharacters === 0) {
    remainingCounter.textContent = `No subscription - Get credits to generate voices`;
    remainingCounter.style.color = '#ff4d4d';
  } else if (actualRemaining === 0) {
    remainingCounter.textContent = `Remaining: 0 characters (quota exhausted - upgrade plan)`;
    remainingCounter.style.color = '#ff4d4d';
  } else {
    remainingCounter.textContent = `Remaining: ${actualRemaining.toLocaleString()} characters`;
    
    // Change colors based on remaining characters
    if (actualRemaining < 1000) {
      remainingCounter.style.color = '#ff4d4d';
    } else if (actualRemaining < 5000) {
      remainingCounter.style.color = '#ffa500';
    } else {
      remainingCounter.style.color = '#4ecca3';
    }
  }
}

// Function to update status card after voice generation
function updateUsageStats(charactersUsed) {
  const usedChars = document.getElementById('usedChars');
  const totalChars = document.getElementById('totalChars');
  const usageLabel = document.getElementById('usageLabel');
  const progressFill = document.getElementById('progressFill');
  
  const maxChars = adminSettings.maxCharacters;
  
  // Handle division by zero
  let usagePercent = 0;
  if (maxChars > 0) {
    usagePercent = ((charactersUsed / maxChars) * 100).toFixed(1);
  } else if (charactersUsed > 0) {
    usagePercent = 100;
  }
  
  // Update top status card
  usedChars.textContent = charactersUsed.toLocaleString();
  totalChars.textContent = maxChars.toLocaleString();
  usageLabel.textContent = `Usage: ${usagePercent}%`;
  progressFill.style.width = `${usagePercent}%`;
  
  // Change colors based on usage
  if (maxChars === 0) {
    progressFill.style.background = '#ff4d4d';  // Red for no subscription
  } else if (charactersUsed > maxChars * 0.9) {
    progressFill.style.background = '#ff4d4d';
  } else if (charactersUsed > maxChars * 0.7) {
    progressFill.style.background = '#ffa500';
  } else {
    progressFill.style.background = '#4ecca3';
  }
}

// Enhanced dropdown functionality for all dropdowns
function setupDropdowns() {
  const dropdowns = document.querySelectorAll('.custom-dropdown');
  
  dropdowns.forEach(dropdown => {
    const selected = dropdown.querySelector('.dropdown-selected');
    const options = dropdown.querySelector('.dropdown-options');
    
    // Toggle dropdown on click
    selected.onclick = function(e) {
      e.stopPropagation();
      
      // Close all other dropdowns first
      dropdowns.forEach(otherDropdown => {
        if (otherDropdown !== dropdown) {
          const otherOptions = otherDropdown.querySelector('.dropdown-options');
          otherOptions.style.display = 'none';
          otherOptions.classList.remove('show');
        }
      });
      
      // Toggle current dropdown
      if (options.style.display === 'block') {
        options.style.display = 'none';
        options.classList.remove('show');
      } else {
        options.style.display = 'block';
        options.classList.add('show');
        
        // Focus search input if it exists
        const searchInput = dropdown.querySelector('.language-search');
        if (searchInput) {
          setTimeout(() => searchInput.focus(), 100);
        }
      }
    };
    
    // Handle option selection - use event delegation for dynamic options
    options.onclick = function(e) {
      const option = e.target.closest('.dropdown-option');
      if (!option) return;
      
      e.stopPropagation();
      const text = option.textContent.trim();
      const value = option.getAttribute('data-value');
      const icon = option.querySelector('svg');
      
      // Update selected display
      const span = selected.querySelector('span');
      span.innerHTML = '';
      
      if (icon) {
        const clonedIcon = icon.cloneNode(true);
        span.appendChild(clonedIcon);
      }
      
      span.appendChild(document.createTextNode(' ' + text));
      
      // Store selected value
      dropdown.setAttribute('data-selected', value || text);
      
      // Hide dropdown
      options.style.display = 'none';
      options.classList.remove('show');
    };
    
    // Search functionality for language dropdown
    const searchInput = dropdown.querySelector('.language-search');
    if (searchInput) {
      searchInput.oninput = function(e) {
        e.stopPropagation();
        const searchTerm = this.value.toLowerCase();
        const optionItems = dropdown.querySelectorAll('.dropdown-option');
        
        optionItems.forEach(option => {
          const text = option.textContent.toLowerCase();
          if (text.includes(searchTerm)) {
            option.style.display = 'block';
          } else {
            option.style.display = 'none';
          }
        });
      };
      
      // Prevent dropdown from closing when clicking on search input
      searchInput.onclick = function(e) {
        e.stopPropagation();
      };
    }
  });
  
  // Close all dropdowns when clicking outside
  document.onclick = function(e) {
    dropdowns.forEach(dropdown => {
      if (!dropdown.contains(e.target)) {
        const options = dropdown.querySelector('.dropdown-options');
        options.style.display = 'none';
        options.classList.remove('show');
      }
    });
  };
}

// Function to update admin settings (call this from admin dashboard)
function updateAdminSettings(newMaxChars) {
  adminSettings.maxCharacters = newMaxChars;
  // Update textarea max length
  document.getElementById('textInput').setAttribute('maxlength', newMaxChars);
  // Refresh display
  updateCharacterCount();
}

// Initialize on page load with API integration
window.onload = async function() {
  // Load language data first
  await loadLanguageData();
  
  setupDropdowns();
  await loadUserDashboard();
  await loadVoiceClones();
  loadProfilePicture();
  
  // Update character count after dashboard data is loaded
  updateCharacterCount();
  
  // Restore audio player state if audio was generated
  restoreAudioPlayer();
};

// Load user dashboard data from API
async function loadUserDashboard() {
  try {
    const dashboardData = await API.getUserDashboard();
    
    // Update user info
    if (dashboardData.user) {
      const userName = dashboardData.user.name || dashboardData.user.email.split('@')[0] || 'User';
      document.getElementById('welcomeMessage').textContent = `Welcome, ${userName}`;
      
      // Store user info in localStorage for persistence
      localStorage.setItem('current_user', JSON.stringify({
        id: dashboardData.user.id,
        email: dashboardData.user.email,
        name: userName,
        user_type: dashboardData.user.user_type,
        has_subscription: dashboardData.user.has_subscription || false
      }));
    }
    
    // Update usage stats if available
    if (dashboardData.usage) {
      const charactersUsed = dashboardData.usage.characters_used || 0;
      const totalCharacters = dashboardData.usage.total_characters || 0;
      
      // Check if user has a subscription
      const hasSubscription = dashboardData.user && dashboardData.user.has_subscription;
      
      if (!hasSubscription) {
        // User has no subscription - show 0 credits and buy subscription message
        adminSettings.maxCharacters = 0;
        adminSettings.charactersRemaining = 0;
        document.getElementById('textInput').setAttribute('maxlength', '0');
        
        // Update display to show 0 credits
        updateUsageStats(0);
        document.getElementById('totalChars').textContent = '0';
        document.getElementById('usedChars').textContent = '0';
        
        // Add a visual indicator for no subscription
        const statusCard = document.querySelector('.status-card');
        if (statusCard && !document.getElementById('subscriptionAlert')) {
          const alert = document.createElement('div');
          alert.id = 'subscriptionAlert';
          alert.style.cssText = 'background: #ff6b6b; color: white; padding: 12px; border-radius: 8px; margin-top: 16px; text-align: center; font-weight: 500;';
          alert.innerHTML = '⚠️ No Active Subscription - <a href="pricing.html" style="color: #fff; text-decoration: underline; font-weight: bold;">Buy Subscription</a> to start generating voices!';
          statusCard.appendChild(alert);
        }
      } else {
        // User has subscription - show proper credits
        const charactersRemaining = dashboardData.usage.characters_remaining || 0;
        
        // Update admin settings with user's plan limit and remaining characters
        adminSettings.maxCharacters = totalCharacters;
        adminSettings.charactersRemaining = charactersRemaining;
        document.getElementById('textInput').setAttribute('maxlength', totalCharacters);
        
        // Update display
        updateUsageStats(charactersUsed);
        document.getElementById('totalChars').textContent = totalCharacters.toLocaleString();
        
        // Remove subscription alert if it exists
        const existingAlert = document.getElementById('subscriptionAlert');
        if (existingAlert) {
          existingAlert.remove();
        }
        
        // Show subscription info in status card
        if (dashboardData.subscription && dashboardData.subscription.plan_name) {
          const statusCard = document.querySelector('.status-card');
          const projectName = statusCard.querySelector('.project-name');
          if (projectName && !document.getElementById('planInfo')) {
            const planInfo = document.createElement('div');
            planInfo.id = 'planInfo';
            planInfo.style.cssText = 'font-size: 12px; color: #4ecca3; margin-top: 4px;';
            planInfo.textContent = `Plan: ${dashboardData.subscription.plan_name}`;
            projectName.appendChild(planInfo);
          }
        }
      }
      
      // Store usage in localStorage
      localStorage.setItem('totalCharactersUsed', charactersUsed.toString());
      localStorage.setItem('totalCharactersLimit', totalCharacters.toString());
    }
    
    console.log('Dashboard data loaded successfully');
    
  } catch (error) {
    console.error('Failed to load dashboard data:', error);
    
    // Load from localStorage as fallback
    const storedUser = localStorage.getItem('current_user');
    if (storedUser) {
      const user = JSON.parse(storedUser);
      document.getElementById('welcomeMessage').textContent = `Welcome, ${user.name}`;
    }
    
    const storedUsage = parseInt(localStorage.getItem('totalCharactersUsed') || '0');
    const storedLimit = parseInt(localStorage.getItem('totalCharactersLimit') || '0');
    updateUsageStats(storedUsage);
    if (storedLimit > 0) {
      document.getElementById('totalChars').textContent = storedLimit.toLocaleString();
    }
  }
}

// Function to load voice clones from API
async function loadVoiceClones() {
  try {
    // Load clones from API
    const response = await API.request('/voice/voices', {
      method: 'GET',
      headers: API.getAuthHeaders()
    });
    const clones = response || [];
    
    const voiceCloneDropdown = document.querySelector('[data-dropdown="voice-clone"] .dropdown-options');
    
    if (voiceCloneDropdown) {
      // Clear all existing options
      voiceCloneDropdown.innerHTML = '';
      
      // Add search bar
      const searchDiv = document.createElement('div');
      searchDiv.className = 'dropdown-search';
      searchDiv.innerHTML = '<input type="text" placeholder="Search voice clones..." class="clone-search" />';
      voiceCloneDropdown.appendChild(searchDiv);
      
      // Add user's API clones to dropdown
      clones.forEach(clone => {
        const option = document.createElement('div');
        option.className = 'dropdown-option';
        // Use speaker_id if available, otherwise fall back to clone id
        option.setAttribute('data-value', clone.speaker_id || clone.id);
        option.innerHTML = `
          <svg class="dropdown-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
          </svg>
          ${clone.voice_name}
        `;
        voiceCloneDropdown.appendChild(option);
      });
      
      // Add search functionality
      const searchInput = voiceCloneDropdown.querySelector('.clone-search');
      if (searchInput) {
        searchInput.oninput = function(e) {
          e.stopPropagation();
          const searchTerm = this.value.toLowerCase();
          const options = voiceCloneDropdown.querySelectorAll('.dropdown-option');
          
          options.forEach(option => {
            const text = option.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
              option.style.display = 'block';
            } else {
              option.style.display = 'none';
            }
          });
        };
        
        searchInput.onclick = function(e) {
          e.stopPropagation();
        };
      }
      
      // Re-setup dropdown functionality for new options
      setupDropdowns();
    }
    
  } catch (error) {
    console.error('Failed to load voice clones:', error);
    // Fallback to local storage
    loadVoiceClonesLocal();
  }
}

// Fallback function for local voice clones
function loadVoiceClonesLocal() {
  const clones = JSON.parse(localStorage.getItem('voiceClones') || '[]');
  const voiceCloneDropdown = document.querySelector('[data-dropdown="voice-clone"] .dropdown-options');
  
  if (voiceCloneDropdown) {
    // Clear existing dynamic options (keep only default ones)
    const defaultOptions = voiceCloneDropdown.querySelectorAll('.dropdown-option');
    const defaultCloneNames = ['naveed', 'shahzad', 'naveed-m', 'naveed-i', 'mrc', 'm-r'];
    
    // Remove non-default options
    defaultOptions.forEach(option => {
      const value = option.getAttribute('data-value');
      if (!defaultCloneNames.includes(value)) {
        option.remove();
      }
    });
    
    // Add saved clones to dropdown
    clones.forEach(clone => {
      const option = document.createElement('div');
      option.className = 'dropdown-option';
      option.setAttribute('data-value', clone.name.toLowerCase().replace(/\s+/g, '-'));
      option.innerHTML = `
        <svg class="dropdown-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
        </svg>
        ${clone.name} (${clone.gender})
      `;
      voiceCloneDropdown.appendChild(option);
    });
    
    // Re-setup dropdown functionality for new options
    setupDropdowns();
  }
}

// Voice generation functionality with API integration
async function generateVoice(event) {
  // Prevent form submission and page reload
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }
  
  const textInput = document.getElementById('textInput');
  const text = textInput.value.trim();
  
  if (!text) {
    alert('Please enter some text to generate voice.');
    return false;
  }
  
  // Check if user has sufficient credits
  if (adminSettings.charactersRemaining === 0 && adminSettings.maxCharacters > 0) {
    alert('You have exhausted your character quota. Please upgrade your plan or contact support.');
    return false;
  }
  
  if (adminSettings.maxCharacters === 0) {
    alert('You do not have an active subscription. Please subscribe to generate voices.');
    window.location.href = 'pricing.html';
    return false;
  }
  
  // Check if user is trying to generate more than remaining
  if (text.length > adminSettings.charactersRemaining) {
    alert(`Text length (${text.length}) exceeds your remaining characters (${adminSettings.charactersRemaining}). Please reduce your text or upgrade your plan.`);
    return false;
  }
  
  // Check if user is logged in
  const token = localStorage.getItem('jwt_token');
  if (!token) {
    alert('Please login to generate voice.');
    window.location.href = 'signin.html';
    return false;
  }
  
  // Get selected values from dropdowns
  const tone = document.querySelector('[data-dropdown="tone"]').getAttribute('data-selected') || 'en';
  const sourceLanguage = document.querySelector('[data-dropdown="source-language"]').getAttribute('data-selected');
  const targetLanguage = document.querySelector('[data-dropdown="target-language"]').getAttribute('data-selected');
  const voiceModel = getSelectedVoiceModel();
  
  console.log('Generating voice with:', { text, tone, sourceLanguage, targetLanguage, voiceModel });
  
  // Show loading state
  const generateBtn = document.querySelector('.btn-primary');
  const originalText = generateBtn.textContent;
  generateBtn.textContent = 'Generating...';
  generateBtn.disabled = true;
  
  try {
    // API call for TTS generation
    const ttsData = {
      text: text,
      language: tone,
      voice_model: voiceModel
    };
    
    // Only include source_language if it's selected (not default placeholder)
    if (sourceLanguage && !sourceLanguage.includes('Select') && sourceLanguage !== 'Source Language') {
      ttsData.source_language = sourceLanguage;
    }
    
    // Only include target_language if it's selected (not default placeholder)
    if (targetLanguage && !targetLanguage.includes('Select') && targetLanguage !== 'Target Language') {
      ttsData.target_language = targetLanguage;
    };
    
    const response = await fetch(`${API_CONFIG.BASE_URL}/voice/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token.replace('Bearer ', '')}`
      },
      body: JSON.stringify(ttsData)
    });
    
    if (!response.ok) {
      if (response.status === 401) {
        alert('Session expired. Please login again.');
        localStorage.removeItem('jwt_token');
        window.location.href = 'signin.html';
        return false;
      }
      
      let errorMessage = 'Failed to generate voice';
      try {
        const errorData = await response.json();
        errorMessage = errorData.error || errorData.message || errorMessage;
      } catch (e) {
        errorMessage = `Server error: ${response.status}`;
      }
      
      throw new Error(errorMessage);
    }
    
    const responseData = await response.json();
    
    // Reload dashboard to get updated usage stats from server
    await loadUserDashboard();
    
    // Update character counter 
    updateCharacterCount();
    
    // Enable audio player and hide placeholder
    const audioPreview = document.getElementById('audioPreview');
    const audioElement = audioPreview.querySelector('audio');
    const placeholder = audioPreview.querySelector('.audio-placeholder');
    
    if (responseData.file_path || responseData.audio_id) {
      // Create download URL for generated audio
      let audioUrl;
      
      if (responseData.audio_id) {
        audioUrl = `${API_CONFIG.BASE_URL}/voice/stream/${responseData.audio_id}`;
        audioElement.setAttribute('data-audio-id', responseData.audio_id);
        // Store audio_id in sessionStorage to persist across page operations
        sessionStorage.setItem('current_audio_id', responseData.audio_id);
        sessionStorage.setItem('current_audio_url', audioUrl);
        
        // Fetch audio as blob for preview (audio element can't use custom headers)
        try {
          const audioResponse = await fetch(audioUrl, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token.replace('Bearer ', '')}`,
              'Accept': 'audio/mpeg, audio/wav, audio/mp3, application/octet-stream'
            }
          });
          
          if (audioResponse.ok) {
            const audioBlob = await audioResponse.blob();
            const blobUrl = URL.createObjectURL(audioBlob);
            audioElement.src = blobUrl;
            
            // Store blob URL for later cleanup
            if (audioElement._blobUrl) {
              URL.revokeObjectURL(audioElement._blobUrl);
            }
            audioElement._blobUrl = blobUrl;
          }
        } catch (err) {
          console.error('Failed to load audio preview:', err);
        }
      } else if (responseData.file_path) {
        // If direct file path is provided, try to stream it
        audioUrl = `${API_CONFIG.BASE_URL}/voice/stream/${responseData.audio_id || 'latest'}`;
        audioElement.src = audioUrl;
      }
      
      // Enable audio player and hide placeholder
      audioElement.removeAttribute('disabled');
      if (placeholder) {
        placeholder.style.display = 'none';
      }
      audioPreview.style.display = 'block';
      
      // Show success message
      console.log('Voice generated successfully!');
      showSuccessMessage('Voice generated successfully!');
    }
    
    
  } catch (error) {
    console.error('TTS generation error:', error);
    
    let userMessage = 'Failed to generate voice. Please try again.';
    
    if (error.message.includes('Network') || error.message.includes('fetch')) {
      userMessage = 'Server connection failed. Please check if the server is running.';
    } else if (error.message.includes('401') || error.message.includes('Unauthorized')) {
      userMessage = 'Session expired. Please login again.';
      localStorage.removeItem('jwt_token');
      setTimeout(() => {
        window.location.href = 'signin.html';
      }, 2000);
    } else {
      userMessage = error.message || userMessage;
    }
    
    alert(userMessage);
    
  } finally {
    // Reset button
    generateBtn.textContent = originalText;
    generateBtn.disabled = false;
  }
}

// Helper function to get selected voice model
function getSelectedVoiceModel() {
  const maleVoiceEl = document.querySelector('[data-dropdown="male-voice"]');
  const femaleVoiceEl = document.querySelector('[data-dropdown="female-voice"]');
  const kidsVoiceEl = document.querySelector('[data-dropdown="kids-voice"]');
  const voiceCloneEl = document.querySelector('[data-dropdown="voice-clone"]');
  
  // Get values only if elements exist
  const maleVoice = maleVoiceEl ? maleVoiceEl.getAttribute('data-selected') : null;
  const femaleVoice = femaleVoiceEl ? femaleVoiceEl.getAttribute('data-selected') : null;
  const kidsVoice = kidsVoiceEl ? kidsVoiceEl.getAttribute('data-selected') : null;
  const voiceClone = voiceCloneEl ? voiceCloneEl.getAttribute('data-selected') : null;
  
  // Priority: voice clone > specific voice type > default
  if (voiceClone && voiceClone !== 'Select Voice Clone') {
    return voiceClone;
  } else if (maleVoice && maleVoice !== 'Select Male Voice') {
    return 'male';
  } else if (femaleVoice && femaleVoice !== 'Select Female Voice') {
    return 'female';
  } else if (kidsVoice && kidsVoice !== 'Select Kids Voice') {
    return 'kids';
  }
  return 'male'; // default
}

// Generate New Voice functionality
function generateNewVoice(event) {
  // Prevent form submission and page reload
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }
  
  // Clear the text input
  const textInput = document.getElementById('textInput');
  textInput.value = '';
  
  // Reset character counter
  updateCharacterCount();
  
  // Reset audio player
  const audioPreview = document.getElementById('audioPreview');
  const audioElement = audioPreview.querySelector('audio');
  const placeholder = audioPreview.querySelector('.audio-placeholder');
  
  if (audioElement) {
    // Clean up blob URL if exists
    if (audioElement._blobUrl) {
      URL.revokeObjectURL(audioElement._blobUrl);
      delete audioElement._blobUrl;
    }
    
    audioElement.src = '';
    audioElement.setAttribute('disabled', 'disabled');
    audioElement.removeAttribute('data-audio-id');
  }
  
  if (placeholder) {
    placeholder.style.display = 'block';
  }
  
  // Clear sessionStorage
  sessionStorage.removeItem('current_audio_id');
  sessionStorage.removeItem('current_audio_url');
  
  showSuccessMessage('Ready to generate new voice!');
}

// Download functionality
async function downloadMP3(event) {
  // Prevent form submission and page reload
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }
  
  const audioPreview = document.getElementById('audioPreview');
  const audioElement = audioPreview.querySelector('audio');
  
  // Check if audio is generated and available
  if (!audioElement.src || audioElement.hasAttribute('disabled')) {
    alert('Please generate voice first.');
    return false;
  }
  
  // Show loading state
  const downloadBtn = document.querySelector('.btn-secondary');
  const originalText = downloadBtn.textContent;
  downloadBtn.textContent = 'Downloading...';
  downloadBtn.disabled = true;
  
  try {
    // Get audio ID from element or sessionStorage
    let audioId = audioElement.getAttribute('data-audio-id');
    
    // Fallback to sessionStorage if not found in element
    if (!audioId) {
      audioId = sessionStorage.getItem('current_audio_id');
      if (audioId) {
        // Restore it to the element
        audioElement.setAttribute('data-audio-id', audioId);
      }
    }
    
    // Check if user is logged in
    const token = localStorage.getItem('jwt_token');
    
    if (!token) {
      alert('Please login to download audio.');
      window.location.href = 'signin.html';
      return false;
    }
    
    if (!audioId) {
      throw new Error('Audio ID not found. Please generate audio again.');
    }
    
    console.log('Starting download process...', { audioId });
    
    // Download via API with audio ID
    const response = await fetch(`${API_CONFIG.BASE_URL}/voice/download/${audioId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token.replace('Bearer ', '')}`,
        'Accept': 'audio/mpeg, audio/mp3, application/octet-stream'
      }
    });
    
    if (!response.ok) {
      if (response.status === 401) {
        alert('Session expired. Please login again.');
        localStorage.removeItem('jwt_token');
        window.location.href = 'signin.html';
        return false;
      }
      
      let errorMessage = `Download failed: ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.error || errorData.message || errorMessage;
      } catch (e) {
        errorMessage = `Download failed: ${response.status} ${response.statusText}`;
      }
      
      throw new Error(errorMessage);
    }
    
    const blob = await response.blob();
    
    // Verify blob has content
    if (blob.size === 0) {
      throw new Error('Downloaded file is empty');
    }
    
    // Download the file
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `generated_audio_${audioId}.wav`;
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    
    showSuccessMessage('Audio downloaded successfully!');
    console.log('Download completed successfully');
    
  } catch (error) {
    console.error('Download error:', error);
    
    let userMessage = 'Failed to download audio file.';
    
    if (error.message.includes('Network') || error.message.includes('fetch')) {
      userMessage = 'Server connection failed. Please check if the server is running.';
    } else if (error.message.includes('401') || error.message.includes('Unauthorized')) {
      userMessage = 'Session expired. Please login again.';
      localStorage.removeItem('jwt_token');
      setTimeout(() => {
        window.location.href = 'signin.html';
      }, 2000);
    } else if (error.message.includes('404')) {
      userMessage = 'Audio file not found. Please generate audio again.';
    } else if (error.message.includes('403')) {
      userMessage = 'Access denied. You can only download your own audio files.';
    } else {
      userMessage = error.message || userMessage;
    }
    
    alert(userMessage);
    
  } finally {
    // Reset button
    downloadBtn.textContent = originalText;
    downloadBtn.disabled = false;
  }
}

// Select Clone functionality
function selectClone() {
  window.location.href = 'cloneslibrary.html';
}

// Home navigation
function goHome() {
  window.location.href = 'index.html';
}

// Show success message
function showSuccessMessage(message) {
  // Create or update success message element
  let successMsg = document.getElementById('successMessage');
  if (!successMsg) {
    successMsg = document.createElement('div');
    successMsg.id = 'successMessage';
    successMsg.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: #4ecca3;
      color: white;
      padding: 12px 20px;
      border-radius: 8px;
      z-index: 1000;
      font-size: 14px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      transform: translateX(100%);
      transition: transform 0.3s ease;
    `;
    document.body.appendChild(successMsg);
  }
  
  successMsg.textContent = message;
  successMsg.style.transform = 'translateX(0)';
  
  // Hide after 3 seconds
  setTimeout(() => {
    successMsg.style.transform = 'translateX(100%)';
  }, 3000);
}

// Profile modal functionality
function openProfileModal() {
  console.log('Profile modal clicked!');
  
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';
  
  input.onchange = function(event) {
    console.log('File selected:', event.target.files[0]);
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function(e) {
        console.log('File loaded, updating profile pic');
        const profilePic = document.getElementById('profilePic');
        if (profilePic) {
          profilePic.style.backgroundImage = `url(${e.target.result})`;
          profilePic.style.backgroundSize = 'cover';
          profilePic.style.backgroundPosition = 'center';
          profilePic.textContent = '';
          
          // Save to localStorage
          localStorage.setItem('userProfilePic', e.target.result);
          console.log('Profile picture updated and saved!');
        } else {
          console.error('Profile pic element not found!');
        }
      };
      reader.readAsDataURL(file);
    }
  };
  
  input.click();
}

// Restore audio player state from sessionStorage
async function restoreAudioPlayer() {
  const audioId = sessionStorage.getItem('current_audio_id');
  const audioUrl = sessionStorage.getItem('current_audio_url');
  
  if (audioId && audioUrl) {
    const audioPreview = document.getElementById('audioPreview');
    const audioElement = audioPreview.querySelector('audio');
    const placeholder = audioPreview.querySelector('.audio-placeholder');
    
    if (audioElement) {
      audioElement.setAttribute('data-audio-id', audioId);
      
      // Fetch audio as blob for preview
      try {
        const token = localStorage.getItem('jwt_token');
        if (token) {
          const audioResponse = await fetch(audioUrl, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token.replace('Bearer ', '')}`,
              'Accept': 'audio/mpeg, audio/wav, audio/mp3, application/octet-stream'
            }
          });
          
          if (audioResponse.ok) {
            const audioBlob = await audioResponse.blob();
            const blobUrl = URL.createObjectURL(audioBlob);
            audioElement.src = blobUrl;
            
            // Store blob URL for cleanup
            if (audioElement._blobUrl) {
              URL.revokeObjectURL(audioElement._blobUrl);
            }
            audioElement._blobUrl = blobUrl;
          }
        }
      } catch (err) {
        console.error('Failed to restore audio preview:', err);
      }
      
      audioElement.removeAttribute('disabled');
      if (placeholder) {
        placeholder.style.display = 'none';
      }
      audioPreview.style.display = 'block';
      console.log('Audio player state restored:', audioId);
    }
  }
}

// Load saved profile picture on page load
function loadProfilePicture() {
  console.log('Loading saved profile picture...');
  const savedPic = localStorage.getItem('userProfilePic');
  if (savedPic) {
    console.log('Found saved profile picture');
    const profilePic = document.getElementById('profilePic');
    if (profilePic) {
      profilePic.style.backgroundImage = `url(${savedPic})`;
      profilePic.style.backgroundSize = 'cover';
      profilePic.style.backgroundPosition = 'center';
      profilePic.textContent = '';
      console.log('Profile picture loaded successfully!');
    } else {
      console.error('Profile pic element not found during load!');
    }
  } else {
    console.log('No saved profile picture found');
  }
}