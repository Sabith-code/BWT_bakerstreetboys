// content.js - Runs on Twitter/X pages to extract tweets

console.log('Abra Code Abra: Content script loaded');

// Configuration
let CONFIG = {
  API_URL: 'http://localhost:5100',
  KEYWORDS: [],
  MONITORED_ACCOUNTS: [],
  enabled: false
};

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

// Load configuration from storage
chrome.storage.sync.get(['api_url', 'keywords', 'monitored_accounts', 'collection_enabled'], (result) => {
  CONFIG.API_URL = normalizeApiUrl(result.api_url);
  CONFIG.KEYWORDS = result.keywords || [];
  CONFIG.MONITORED_ACCOUNTS = result.monitored_accounts || [];
  CONFIG.enabled = result.collection_enabled || false;
  
  console.log('Abra Code Abra: Configuration loaded', CONFIG);
  
  if (CONFIG.enabled) {
    startCollecting();
  }
});

// Listen for configuration updates
chrome.storage.onChanged.addListener((changes, namespace) => {
  if (changes.collection_enabled) {
    CONFIG.enabled = changes.collection_enabled.newValue;
    if (CONFIG.enabled) {
      startCollecting();
    } else {
      stopCollecting();
    }
  }
  if (changes.keywords) {
    CONFIG.KEYWORDS = changes.keywords.newValue || [];
  }
  if (changes.monitored_accounts) {
    CONFIG.MONITORED_ACCOUNTS = changes.monitored_accounts.newValue || [];
  }
  if (changes.api_url) {
    CONFIG.API_URL = normalizeApiUrl(changes.api_url.newValue);
  }
});

// Track processed tweets to avoid duplicates
const processedTweets = new Set();
let collectionInterval = null;

/**
 * Extract tweet data from a tweet element
 */
function extractTweetData(tweetElement) {
  try {
    // Find the tweet link to get the tweet ID
    const tweetLink = tweetElement.querySelector('a[href*="/status/"]');
    if (!tweetLink) return null;
    
    const tweetUrl = tweetLink.href;
    const tweetId = tweetUrl.split('/status/')[1]?.split('?')[0];
    if (!tweetId) return null;
    
    // Skip if already processed
    if (processedTweets.has(tweetId)) return null;
    
    // Extract tweet text
    const tweetTextElement = tweetElement.querySelector('[data-testid="tweetText"]');
    if (!tweetTextElement) return null;
    const tweetText = tweetTextElement.innerText;
    
    // Extract author information
    const authorElement = tweetElement.querySelector('[data-testid="User-Name"]');
    if (!authorElement) return null;
    
    // Get username (handle)
    const usernameElement = authorElement.querySelector('a[href^="/"]');
    const username = usernameElement?.href.split('/').pop() || 'unknown';
    
    // Get display name
    const displayNameElement = authorElement.querySelector('span');
    const displayName = displayNameElement?.innerText || username;
    
    // Extract timestamp
    const timeElement = tweetElement.querySelector('time');
    const timestamp = timeElement?.getAttribute('datetime') || new Date().toISOString();
    
    // Check if tweet matches our criteria
    const isRelevant = checkRelevance(tweetText, username);
    if (!isRelevant) return null;
    
    // Mark as processed
    processedTweets.add(tweetId);
    
    return {
      tweet_id: tweetId,
      content: tweetText,
      author_username: username,
      author_display_name: displayName,
      created_at: timestamp,
      url: tweetUrl,
      collected_at: new Date().toISOString()
    };
    
  } catch (error) {
    console.error('Error extracting tweet data:', error);
    return null;
  }
}

/**
 * Check if a tweet is relevant based on keywords and monitored accounts
 */
function checkRelevance(tweetText, username) {
  const lowerText = tweetText.toLowerCase();
  
  // If no keywords and no accounts configured, collect everything
  if (CONFIG.KEYWORDS.length === 0 && CONFIG.MONITORED_ACCOUNTS.length === 0) {
    console.log('Abra Code Abra: No keywords/accounts configured - collecting all tweets');
    return true;
  }
  
  // Check if tweet mentions any monitored accounts
  const mentionsMonitoredAccount = CONFIG.MONITORED_ACCOUNTS.length > 0 && 
    CONFIG.MONITORED_ACCOUNTS.some(account => 
      lowerText.includes(account.toLowerCase().replace('@', ''))
    );
  
  // Check if tweet contains any keywords
  const containsKeyword = CONFIG.KEYWORDS.length > 0 && 
    CONFIG.KEYWORDS.some(keyword => 
      lowerText.includes(keyword.toLowerCase())
    );
  
  const isRelevant = mentionsMonitoredAccount || containsKeyword;
  if (!isRelevant) {
    console.log(`Abra Code Abra: Tweet not matching - "${tweetText.substring(0, 50)}..."`);
  }
  
  return isRelevant;
}

/**
 * Send collected tweets to backend
 */
async function sendToBackend(tweets) {
  if (tweets.length === 0) return;
  
  try {
    console.log(`Sending ${tweets.length} tweets to backend...`);
    
    const response = await fetch(`${CONFIG.API_URL}/api/extension/collect`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ tweets })
    });
    
    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`);
    }
    
    const result = await response.json();
    console.log('Backend response:', result);
    
    // Update collected count
    chrome.storage.sync.get(['collected_count'], (data) => {
      const newCount = (data.collected_count || 0) + tweets.length;
      chrome.storage.sync.set({ collected_count: newCount });
    });
    
    // Show notification
    chrome.runtime.sendMessage({
      type: 'TWEETS_COLLECTED',
      count: tweets.length
    });
    
    return result;
    
  } catch (error) {
    console.error('Error sending to backend:', error);
    chrome.runtime.sendMessage({
      type: 'COLLECTION_ERROR',
      error: error.message
    });
  }
}

/**
 * Scan the page for tweets
 */
function scanForTweets() {
  console.log('Scanning for tweets...');
  
  // Find all tweet articles on the page
  const tweetElements = document.querySelectorAll('article[data-testid="tweet"]');
  console.log(`Found ${tweetElements.length} tweet elements`);
  
  const collectedTweets = [];
  
  tweetElements.forEach(tweetElement => {
    const tweetData = extractTweetData(tweetElement);
    if (tweetData) {
      collectedTweets.push(tweetData);
      console.log('Collected tweet:', tweetData.tweet_id);
    }
  });
  
  if (collectedTweets.length > 0) {
    sendToBackend(collectedTweets);
  }
}

/**
 * Start collecting tweets
 */
function startCollecting() {
  console.log('Starting tweet collection...');
  
  // Initial scan
  scanForTweets();
  
  // Set up periodic scanning
  if (collectionInterval) {
    clearInterval(collectionInterval);
  }
  
  collectionInterval = setInterval(() => {
    if (CONFIG.enabled) {
      scanForTweets();
    }
  }, 10000); // Scan every 10 seconds
  
  // Also scan when scrolling (with debounce)
  let scrollTimeout;
  window.addEventListener('scroll', () => {
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
      if (CONFIG.enabled) {
        scanForTweets();
      }
    }, 2000);
  });
}

/**
 * Stop collecting tweets
 */
function stopCollecting() {
  console.log('Stopping tweet collection...');
  if (collectionInterval) {
    clearInterval(collectionInterval);
    collectionInterval = null;
  }
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'SCAN_NOW') {
    scanForTweets();
    sendResponse({ success: true });
  }
  return true;
});

// Visual indicator that extension is active
function showActiveIndicator() {
  if (!CONFIG.enabled) return;
  
  // Create a small indicator in the corner
  const indicator = document.createElement('div');
  indicator.id = 'abra-code-abra-indicator';
  indicator.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #10b981;
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-family: system-ui;
    z-index: 10000;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  `;
  indicator.textContent = '✓ Collecting Feedback';
  
  // Remove any existing indicator
  const existing = document.getElementById('abra-code-abra-indicator');
  if (existing) existing.remove();
  
  document.body.appendChild(indicator);
  
  // Auto-hide after 3 seconds
  setTimeout(() => {
    indicator.style.opacity = '0';
    indicator.style.transition = 'opacity 0.5s';
    setTimeout(() => indicator.remove(), 500);
  }, 3000);
}

// Show indicator when enabled
chrome.storage.onChanged.addListener((changes) => {
  if (changes.collection_enabled?.newValue) {
    showActiveIndicator();
  }
});