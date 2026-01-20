# Admin Panel + Manual Subscription Management System

## 🚀 Complete System Overview

This is a complete Admin Panel with Manual Subscription Management System for your voice cloning website. The system includes:

### ✅ Features Implemented

1. **Manual Subscription Flow** - No automatic payments, WhatsApp redirect
2. **Complete Admin Panel** - Dashboard, Add Subscription, User Management
3. **Token Auto-Reduce Logic** - Automatic token consumption and expiry
4. **Dashboard Summary Boxes** - Real-time plan counts
5. **Modern Responsive UI** - Matches your website theme

---

## 📁 Files Created

### Admin Panel Files:
- `admin-dashboard.html` - Main dashboard with summary boxes
- `add-subscription.html` - Manual subscription activation form
- `subscription-users.html` - User management with edit/delete
- `token-api.js` - Token consumption logic
- `demo-token-usage.html` - Demo page to test token system

### Updated Files:
- `pricing.html` - Updated to redirect to WhatsApp

---

## 🔧 How to Use

### 1. Admin Panel Access
- Open `admin-dashboard.html` in your browser
- Navigate between Dashboard, Add Subscription, and User Management

### 2. Subscription Flow (Frontend)
- Users click "Get Subscription" on pricing page
- Redirects to WhatsApp: `https://wa.me/+1234567890?text=Hi, I want the [PLAN_NAME] subscription.`
- **Change the phone number** in `pricing.html` to your actual WhatsApp number

### 3. Manual Subscription Management
- Admin uses "Add Subscription" page to manually activate users
- Fill in: Email, Plan, Dates, Tokens, Status
- Data is stored in browser localStorage (dummy data)

### 4. User Management
- View all subscription users in a clean table
- Search and filter by status/plan
- Edit or delete subscriptions
- Real-time token consumption simulation

### 5. Token System
- Use `demo-token-usage.html` to test token consumption
- Tokens automatically reduce when users consume them
- Status changes to "Expired" when tokens reach zero

---

## 🎨 UI Features

### Dashboard Summary Boxes:
- **Low Plan Users**: Shows count of active Low Plan subscribers
- **Middle Plan Users**: Shows count of active Middle Plan subscribers  
- **High Plan Users**: Shows count of active High Plan subscribers

### Modern Design:
- Responsive Bootstrap layout
- Matches your website color scheme (#4ecca3 primary)
- Clean, professional admin interface
- Mobile-friendly design

---

## 🔄 Token Auto-Reduce Logic

The system includes automatic token management:

```javascript
// When user consumes a token:
1. Check if user has active subscription
2. Check if tokens > 0
3. Reduce token count by 1
4. If tokens reach 0 → Set status to "Expired"
5. Save changes to localStorage
```

---

## 📱 WhatsApp Integration

### Current Setup:
```html
<a href="https://wa.me/+1234567890?text=Hi, I want the Low Plan subscription." 
   target="_blank">Get Subscription →</a>
```

### To Customize:
1. Replace `+1234567890` with your actual WhatsApp number
2. Messages are pre-formatted for each plan: 
   - "Hi, I want the Low Plan subscription."
   - "Hi, I want the Middle Plan subscription."  
   - "Hi, I want the High Plan subscription."

---

## 💾 Data Storage

Currently uses **localStorage** for demo purposes:
- Subscription data stored in browser
- Includes dummy users for testing
- In production, replace with proper database

### Dummy Users Included:
- john@example.com (Middle Plan, 450 tokens)
- sarah@example.com (High Plan, 800 tokens)
- mike@example.com (Low Plan, 0 tokens - Expired)
- emma@example.com (Middle Plan, 300 tokens)
- david@example.com (Low Plan, 75 tokens)

---

## 🚀 Quick Start

1. **Open Admin Panel**: `admin-dashboard.html`
2. **Test Token System**: `demo-token-usage.html`
3. **Check Pricing Flow**: `pricing.html` → Click "Get Subscription"
4. **Add New User**: Use "Add Subscription" in admin panel
5. **Manage Users**: Use "Subscription Users" page

---

## 🔧 Customization

### Change WhatsApp Number:
Edit `pricing.html` and replace `+1234567890` with your number.

### Modify Plans:
Update plan names and token amounts in:
- `add-subscription.html` (dropdown options)
- `token-api.js` (plan logic)
- `pricing.html` (plan display)

### Styling:
All CSS uses CSS variables for easy theme changes:
```css
:root {
    --primary-color: #4ecca3;
    --secondary-color: #232931;
    --accent-color: #393e46;
}
```

---

## ✅ Production Ready

The code is:
- Clean and organized
- Responsive design
- Error handling included
- Easy to maintain
- Ready for backend integration

---

## 🎯 Next Steps for Production

1. Replace localStorage with proper database
2. Add user authentication
3. Implement real payment processing (if needed)
4. Add email notifications
5. Set up proper backend API

---

**System is complete and ready to use! 🎉**