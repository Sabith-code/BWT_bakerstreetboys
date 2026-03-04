// background.js - Background service worker

console.log('Abra Code Abra: Background service worker started');

// Default configuration
const DEFAULT_CONFIG = {
  api_url: 'http://localhost:5100',
  keywords: ['bug', 'issue', 'broken', 'crash', 'not working', 'feature request'],
  monitored_accounts: [],
  collection_enabled: false,
  collected_count: 0
};

// Initialize storage with defaults
chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed/updated');
  
  chrome.storage.sync.get(Object.keys(DEFAULT_CONFIG), (result) => {
    // Set defaults for missing values
    const updates = {};
    for (const key in DEFAULT_CONFIG) {
      if (result[key] === undefined) {
        updates[key] = DEFAULT_CONFIG[key];
      }
    }
    
    if (Object.keys(updates).length > 0) {
      chrome.storage.sync.set(updates);
      console.log('Initialized storage with defaults:', updates);
    }
  });
});

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Background received message:', message);
  
  switch (message.type) {
    case 'TWEETS_COLLECTED':
      // Show notification when tweets are collected
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon48.png',
        title: 'Feedback Collected',
        message: `Collected ${message.count} tweet(s)`,
        priority: 1
      });
      break;
      
    case 'COLLECTION_ERROR':
      // Show error notification
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon48.png',
        title: 'Collection Error',
        message: message.error,
        priority: 2
      });
      break;
  }
  
  sendResponse({ received: true });
  return true;
});

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
  console.log('Extension icon clicked');
});

// Keep service worker alive
const keepAlive = () => {
  chrome.storage.local.set({ lastAlive: Date.now() });
};

// Ping every 20 seconds
setInterval(keepAlive, 20000);
keepAlive();