// Configuration for the extension
const CONFIG = {
    // Backend API URL - change this to your deployed backend
    API_URL: 'http://localhost:5100',
    
    // Keywords to monitor (tweets containing these will be collected)
    KEYWORDS: [
      'bug',
      'issue',
      'broken',
      'crash',
      'error',
      'not working',
      'feature request',
      'please add',
      'would be nice',
      'suggestion'
    ],
    
    // Accounts to monitor (collect all tweets mentioning these)
    MONITORED_ACCOUNTS: [
      '@YourProductTwitter',  // Replace with your product's Twitter handle
      '@YourCompany'
    ],
    
    // Collection settings
    COLLECTION_INTERVAL: 60000, // Check every 60 seconds
    MAX_TWEETS_PER_BATCH: 50,
    
    // Storage keys
    STORAGE_KEYS: {
      ENABLED: 'collection_enabled',
      LAST_TWEET_ID: 'last_tweet_id',
      COLLECTED_COUNT: 'collected_count',
      API_URL: 'api_url',
      KEYWORDS: 'keywords',
      ACCOUNTS: 'monitored_accounts'
    }
  };
  
  // Make config available globally
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
  }