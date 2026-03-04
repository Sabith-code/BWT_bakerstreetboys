// popup.js - Popup UI logic

console.log('Popup script loaded');

// DOM elements
const toggleButton = document.getElementById('toggleButton');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const collectedCount = document.getElementById('collectedCount');
const lastSync = document.getElementById('lastSync');
const apiUrlInput = document.getElementById('apiUrl');
const keywordsInput = document.getElementById('keywords');
const accountsInput = document.getElementById('accounts');
const saveConfigButton = document.getElementById('saveConfig');
const scanNowButton = document.getElementById('scanNow');
const resetCountButton = document.getElementById('resetCount');
const openDashboardButton = document.getElementById('openDashboard');

// Current state
let isEnabled = false;
let config = {};

function normalizeApiUrl(value) {
  const fallback = 'http://localhost:5100';
  if (!value || typeof value !== 'string') {
    return fallback;
  }

  try {
    const parsed = new URL(value.trim());
    let pathname = parsed.pathname.replace(/\/+$/, '');
    pathname = pathname.replace(/\/(api|dashboard)$/i, '');
    parsed.pathname = pathname || '';
    parsed.search = '';
    parsed.hash = '';
    return parsed.toString().replace(/\/+$/, '');
  } catch {
    return fallback;
  }
}

/**
 * Load configuration from storage
 */
async function loadConfiguration() {
  return new Promise((resolve) => {
    chrome.storage.sync.get([
      'collection_enabled',
      'api_url',
      'keywords',
      'monitored_accounts',
      'collected_count'
    ], (result) => {
      config = {
        enabled: result.collection_enabled || false,
        apiUrl: normalizeApiUrl(result.api_url),
        keywords: result.keywords || [],
        accounts: result.monitored_accounts || [],
        count: result.collected_count || 0
      };
      resolve(config);
    });
  });
}

/**
 * Update UI based on current state
 */
function updateUI() {
  // Update status
  isEnabled = config.enabled;
  
  if (isEnabled) {
    statusDot.classList.add('active');
    statusText.textContent = 'Active';
    toggleButton.textContent = 'Stop Collecting';
    toggleButton.classList.add('active');
  } else {
    statusDot.classList.remove('active');
    statusText.textContent = 'Disabled';
    toggleButton.textContent = 'Start Collecting';
    toggleButton.classList.remove('active');
  }
  
  // Update stats
  collectedCount.textContent = config.count || 0;
  
  // Update form fields
  apiUrlInput.value = config.apiUrl;
  keywordsInput.value = config.keywords.join(', ');
  accountsInput.value = config.accounts.join(', ');
  
  // Update last sync time
  chrome.storage.local.get(['lastSync'], (result) => {
    if (result.lastSync) {
      const syncDate = new Date(result.lastSync);
      const now = new Date();
      const diffMinutes = Math.floor((now - syncDate) / 60000);
      
      if (diffMinutes < 1) {
        lastSync.textContent = 'Just now';
      } else if (diffMinutes < 60) {
        lastSync.textContent = `${diffMinutes}m ago`;
      } else {
        lastSync.textContent = `${Math.floor(diffMinutes / 60)}h ago`;
      }
    } else {
      lastSync.textContent = 'Never';
    }
  });
}

/**
 * Toggle collection on/off
 */
async function toggleCollection() {
  isEnabled = !isEnabled;
  
  await chrome.storage.sync.set({ collection_enabled: isEnabled });
  config.enabled = isEnabled;
  
  updateUI();
  
  if (isEnabled) {
    showToast('Collection started!', 'success');
  } else {
    showToast('Collection stopped', 'success');
  }
}

/**
 * Save configuration
 */
async function saveConfiguration() {
  // Parse inputs
  const keywords = keywordsInput.value
    .split(',')
    .map(k => k.trim())
    .filter(k => k.length > 0);
  
  const accounts = accountsInput.value
    .split(',')
    .map(a => a.trim())
    .filter(a => a.length > 0);
  
  const apiUrl = normalizeApiUrl(apiUrlInput.value.trim());
  
  // Validate API URL
  try {
    new URL(apiUrl);
  } catch (e) {
    showToast('Invalid API URL', 'error');
    return;
  }
  
  // Save to storage
  await chrome.storage.sync.set({
    api_url: apiUrl,
    keywords: keywords,
    monitored_accounts: accounts
  });
  
  config.apiUrl = apiUrl;
  config.keywords = keywords;
  config.accounts = accounts;
  
  showToast('Configuration saved!', 'success');
}

/**
 * Scan current page immediately
 */
async function scanCurrentPage() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  if (!tab.url.includes('twitter.com') && !tab.url.includes('x.com')) {
    showToast('Please navigate to Twitter/X first', 'error');
    return;
  }
  
  chrome.tabs.sendMessage(tab.id, { type: 'SCAN_NOW' }, (response) => {
    if (chrome.runtime.lastError) {
      showToast('Error: Reload the Twitter page', 'error');
    } else {
      showToast('Scanning page...', 'success');
      chrome.storage.local.set({ lastSync: Date.now() });
      setTimeout(updateUI, 1000);
    }
  });
}

/**
 * Reset collected count
 */
async function resetCollectedCount() {
  await chrome.storage.sync.set({ collected_count: 0 });
  config.count = 0;
  updateUI();
  showToast('Counter reset', 'success');
}

/**
 * Open dashboard in new tab
 */
function openDashboard() {
  chrome.tabs.create({ url: `${normalizeApiUrl(config.apiUrl)}/dashboard` });
}

/**
 * Show toast notification
 */
function showToast(message, type = 'success') {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.className = `toast show ${type}`;
  
  setTimeout(() => {
    toast.classList.remove('show');
  }, 3000);
}

// Event listeners
toggleButton.addEventListener('click', toggleCollection);
saveConfigButton.addEventListener('click', saveConfiguration);
scanNowButton.addEventListener('click', scanCurrentPage);
resetCountButton.addEventListener('click', resetCollectedCount);
openDashboardButton.addEventListener('click', openDashboard);

// Initialize popup
(async () => {
  await loadConfiguration();
  updateUI();
  
  // Update UI every 30 seconds
  setInterval(updateUI, 30000);
})();

// Listen for storage changes
chrome.storage.onChanged.addListener((changes) => {
  if (changes.collection_enabled) {
    config.enabled = changes.collection_enabled.newValue;
    updateUI();
  }
  if (changes.collected_count) {
    config.count = changes.collected_count.newValue;
    updateUI();
  }
});