// Admin Dashboard JavaScript Functions with API Integration

// Load recent activity from API
async function loadRecentActivity() {
  try {
    const response = await API.request('/admin/recent-activity?limit=5', {
      method: 'GET'
    });

    if (response.activity && response.activity.length > 0) {
      const activityContainer = document.querySelector('.list-group');
      if (activityContainer) {
        activityContainer.innerHTML = response.activity.map(activity => `
          <div class="list-group-item border-0 px-0">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <strong>${activity.user_email}</strong> - ${activity.plan_name} Plan activated
              </div>
              <small class="text-muted">${formatTimeAgo(activity.timestamp)}</small>
            </div>
          </div>
        `).join('');
      }
    }
  } catch (error) {
    console.error('Failed to load recent activity:', error);
    // Keep default dummy data if API fails
  }
}

// Format timestamp to "time ago" format
function formatTimeAgo(timestamp) {
  if (!timestamp) return 'Unknown time';

  const now = new Date();
  const time = new Date(timestamp);
  const diffInSeconds = Math.floor((now - time) / 1000);

  if (diffInSeconds < 60) return 'Just now';
  if (diffInSeconds < 120) return '1 minute ago';
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
  if (diffInSeconds < 7200) return '1 hour ago';
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
  if (diffInSeconds < 172800) return '1 day ago';
  return `${Math.floor(diffInSeconds / 86400)} days ago`;
}

// Update stats from API
async function updateStats() {
  try {
    const response = await API.request('/admin/stats', {
      method: 'GET'
    });

    if (response) {
      // Get plan counts from API
      const plansResponse = await API.request('/admin/plans', {
        method: 'GET'
      });

      // Count users by plan
      let basicCount = 0, proCount = 0, premiumCount = 0, enterpriseCount = 0;

      if (plansResponse && plansResponse.plans) {
        plansResponse.plans.forEach(plan => {
          if (plan.name === 'Basic') basicCount = plan.user_count || 0;
          else if (plan.name === 'Pro') proCount = plan.user_count || 0;
          else if (plan.name === 'Premium') premiumCount = plan.user_count || 0;
          else if (plan.name === 'Enterprise') enterpriseCount = plan.user_count || 0;
        });
      }

      // Update cards with real data
      document.getElementById('totalUsersCount').textContent = response.total_users || 0;
      document.getElementById('lowPlanCount').textContent = basicCount;
      document.getElementById('middlePlanCount').textContent = proCount;
      document.getElementById('highPlanCount').textContent = premiumCount;
      document.getElementById('enterprisePlanCount').textContent = enterpriseCount;
    }
  } catch (error) {
    console.error('Failed to update stats:', error);
    // Keep dummy data if API fails
    document.getElementById('totalUsersCount').textContent = '0';
    document.getElementById('lowPlanCount').textContent = '0';
    document.getElementById('middlePlanCount').textContent = '0';
    document.getElementById('highPlanCount').textContent = '0';
    document.getElementById('enterprisePlanCount').textContent = '0';
  }
}

// Assign plan to user (API integration)
async function assignPlanToUser(email, planId) {
  try {
    const planData = {
      email: email,
      plan_id: planId
    };

    const response = await API.assignPlan(planData);
    return response;

  } catch (error) {
    console.error('Failed to assign plan:', error);
    throw error;
  }
}

// Logout function
function logout() {
  if (confirm('Are you sure you want to logout?')) {
    sessionStorage.removeItem('adminAuth');
    window.location.href = 'index.html';
  }
}

// Mobile sidebar functions
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');

  sidebar.classList.toggle('show');
  overlay.classList.toggle('show');
}

function closeSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');

  sidebar.classList.remove('show');
  overlay.classList.remove('show');
}

// Initialize admin dashboard
document.addEventListener('DOMContentLoaded', function () {
  // Load initial data
  updateStats();
  loadRecentActivity();
  loadPlans();

  // Update stats and activity every 30 seconds
  setInterval(() => {
    updateStats();
    loadRecentActivity();
  }, 30000);

  // Close sidebar when clicking nav links on mobile
  document.querySelectorAll('.sidebar .nav-link').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 768) {
        closeSidebar();
      }
    });
  });

  // Handle window resize
  window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
      closeSidebar();
    }
  });
});

// Show/Hide sections
function showPlansSection() {
  document.getElementById('dashboard-section').style.display = 'none';
  document.getElementById('plans-section').style.display = 'block';

  // Update active nav link
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.remove('active');
  });
  event.target.classList.add('active');

  loadPlans();
}

function showDashboardSection() {
  document.getElementById('dashboard-section').style.display = 'block';
  document.getElementById('plans-section').style.display = 'none';
}

// Plans Management Functions
async function loadPlans() {
  try {
    const token = localStorage.getItem('jwt_token');
    const response = await fetch(`${API_CONFIG.BASE_URL}/admin/plans`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.ok) {
      const data = await response.json();
      displayPlans(data.plans || []);
    } else {
      console.error('Failed to load plans:', response.status);
    }
  } catch (error) {
    console.error('Error loading plans:', error);
  }
}

function displayPlans(plans) {
  const tbody = document.getElementById('plansTableBody');
  tbody.innerHTML = '';

  plans.forEach(plan => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td><strong>${plan.name}</strong></td>
      <td>${plan.character_limit.toLocaleString()} chars</td>
      <td><span class="badge bg-info">${plan.user_count || 0} users</span></td>
      <td>${plan.created_at ? new Date(plan.created_at).toLocaleDateString() : 'N/A'}</td>
      <td>
        <button class="btn btn-sm btn-outline-primary me-2" onclick="editPlan(${plan.id}, '${plan.name}', ${plan.character_limit})">
          <i class="fas fa-edit"></i> Edit
        </button>
        <button class="btn btn-sm btn-outline-danger" onclick="deletePlan(${plan.id}, '${plan.name}')">
          <i class="fas fa-trash"></i> Delete
        </button>
      </td>
    `;
    tbody.appendChild(row);
  });
}

function openAddPlanModal() {
  document.getElementById('planModalTitle').textContent = 'Add New Plan';
  document.getElementById('planId').value = '';
  document.getElementById('planName').value = '';
  document.getElementById('characterLimit').value = '';

  const modal = new bootstrap.Modal(document.getElementById('planModal'));
  modal.show();
}

function editPlan(id, name, characterLimit) {
  document.getElementById('planModalTitle').textContent = 'Edit Plan';
  document.getElementById('planId').value = id;
  document.getElementById('planName').value = name;
  document.getElementById('characterLimit').value = characterLimit;

  const modal = new bootstrap.Modal(document.getElementById('planModal'));
  modal.show();
}

async function savePlan() {
  const planId = document.getElementById('planId').value;
  const planName = document.getElementById('planName').value;
  const characterLimit = document.getElementById('characterLimit').value;

  if (!planName || !characterLimit) {
    alert('Please fill all fields');
    return;
  }

  try {
    const token = localStorage.getItem('jwt_token');
    const url = planId ?
      `${API_CONFIG.BASE_URL}/admin/plans/${planId}` :
      `${API_CONFIG.BASE_URL}/admin/plans`;

    const method = planId ? 'PUT' : 'POST';

    const response = await fetch(url, {
      method: method,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: planName,
        character_limit: parseInt(characterLimit)
      })
    });

    if (response.ok) {
      const modal = bootstrap.Modal.getInstance(document.getElementById('planModal'));
      modal.hide();

      alert(planId ? 'Plan updated successfully!' : 'Plan created successfully!');
      loadPlans();
      updateStats();
    } else {
      const error = await response.json();
      alert('Error: ' + (error.error || 'Failed to save plan'));
    }
  } catch (error) {
    console.error('Error saving plan:', error);
    alert('Error saving plan: ' + error.message);
  }
}

async function deletePlan(id, name) {
  if (!confirm(`Are you sure you want to delete the "${name}" plan?`)) {
    return;
  }

  try {
    const token = localStorage.getItem('jwt_token');
    const response = await fetch(`${API_CONFIG.BASE_URL}/admin/plans/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.ok) {
      alert('Plan deleted successfully!');
      loadPlans();
      updateStats();
    } else {
      const error = await response.json();
      alert('Error: ' + (error.error || 'Failed to delete plan'));
    }
  } catch (error) {
    console.error('Error deleting plan:', error);
    alert('Error deleting plan: ' + error.message);
  }
}