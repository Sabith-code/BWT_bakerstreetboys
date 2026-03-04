from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for Chrome extension

# In-memory storage (for testing - will reset when server restarts)
collected_tweets = []
stats = {
    'total_collected': 0,
    'today_count': 0,
    'last_collection': None
}

@app.route('/')
def home():
    """Home page with simple dashboard"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Abra Code Abra - Backend</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
                background: #f9fafb;
            }}
            .header {{
                text-align: center;
                margin-bottom: 40px;
            }}
            h1 {{
                color: #1f2937;
                font-size: 36px;
                margin-bottom: 8px;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            .stat-card {{
                background: white;
                padding: 24px;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            .stat-label {{
                color: #6b7280;
                font-size: 14px;
                margin-bottom: 8px;
            }}
            .stat-value {{
                color: #1f2937;
                font-size: 32px;
                font-weight: 700;
            }}
            .tweets {{
                background: white;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                padding: 24px;
            }}
            .tweet {{
                border-left: 4px solid #3b82f6;
                padding: 16px;
                margin-bottom: 16px;
                background: #f9fafb;
                border-radius: 4px;
            }}
            .tweet-meta {{
                color: #6b7280;
                font-size: 14px;
                margin-bottom: 8px;
            }}
            .tweet-content {{
                color: #1f2937;
                line-height: 1.6;
            }}
            .status {{
                display: inline-block;
                padding: 4px 12px;
                background: #10b981;
                color: white;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
            }}
            .empty {{
                text-align: center;
                color: #9ca3af;
                padding: 40px;
            }}
            code {{
                background: #f3f4f6;
                padding: 2px 6px;
                border-radius: 4px;
                font-family: monospace;
            }}
        </style>
        <script>
            // Auto-refresh every 5 seconds
            setTimeout(() => location.reload(), 5000);
        </script>
    </head>
    <body>
        <div class="header">
            <h1>🪄 Abra Code Abra</h1>
            <p style="color: #6b7280; font-size: 16px;">Feedback Collection Backend</p>
            <span class="status">Backend Running</span>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">Total Collected</div>
                <div class="stat-value">{stats['total_collected']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Today's Count</div>
                <div class="stat-value">{stats['today_count']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Last Collection</div>
                <div class="stat-value" style="font-size: 16px;">
                    {stats['last_collection'] or 'Never'}
                </div>
            </div>
        </div>
        
        <div class="tweets">
            <h2 style="margin-bottom: 20px;">Recent Feedback</h2>
            {''.join([f"""
                <div class="tweet">
                    <div class="tweet-meta">
                        <strong>@{tweet['author_username']}</strong> · 
                        {tweet['created_at'][:10]} · 
                        <a href="https://twitter.com/i/web/status/{tweet['tweet_id']}" target="_blank" style="color: #3b82f6;">View on Twitter</a>
                    </div>
                    <div class="tweet-content">{tweet['content']}</div>
                </div>
            """ for tweet in reversed(collected_tweets[-10:])]) or '<div class="empty">No feedback collected yet. Start your Chrome extension!</div>'}
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: #9ca3af; font-size: 14px;">
            <p>Backend API: <code>http://localhost:5000/api/extension/collect</code></p>
            <p>This page auto-refreshes every 5 seconds</p>
        </div>
    </body>
    </html>
    """

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Backend is running!',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/extension/collect', methods=['POST'])
def extension_collect():
    """
    Main endpoint for Chrome extension to send collected tweets
    """
    try:
        data = request.json
        tweets = data.get('tweets', [])
        
        if not tweets:
            return jsonify({
                'success': False,
                'error': 'No tweets provided'
            }), 400
        
        processed = 0
        
        for tweet in tweets:
            # Add to our in-memory storage
            tweet_data = {
                'tweet_id': tweet.get('tweet_id'),
                'content': tweet.get('content'),
                'author_username': tweet.get('author_username'),
                'created_at': tweet.get('created_at'),
                'url': tweet.get('url'),
                'collected_at': datetime.now().isoformat()
            }
            
            # Avoid duplicates
            if not any(t['tweet_id'] == tweet_data['tweet_id'] for t in collected_tweets):
                collected_tweets.append(tweet_data)
                processed += 1
        
        # Update stats
        stats['total_collected'] = len(collected_tweets)
        stats['today_count'] = len(collected_tweets)  # Simplified for testing
        stats['last_collection'] = datetime.now().strftime('%H:%M:%S')
        
        print(f"\n✅ Collected {processed} new tweet(s)!")
        print(f"📊 Total tweets: {len(collected_tweets)}")
        
        return jsonify({
            'success': True,
            'processed': processed,
            'total': len(tweets),
            'message': f'Successfully collected {processed} tweet(s)'
        })
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/extension/stats', methods=['GET'])
def extension_stats():
    """
    Get statistics for the extension popup
    """
    try:
        return jsonify({
            'today_count': stats['today_count'],
            'total_count': stats['total_collected'],
            'last_collection': stats['last_collection'],
            'recent': collected_tweets[-5:] if collected_tweets else []
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tweets', methods=['GET'])
def get_tweets():
    """
    Get all collected tweets (for debugging)
    """
    return jsonify({
        'count': len(collected_tweets),
        'tweets': collected_tweets
    })

@app.route('/api/tweets/export', methods=['GET'])
def export_tweets():
    """
    Export all tweets as JSON file
    """
    return jsonify({
        'exported_at': datetime.now().isoformat(),
        'count': len(collected_tweets),
        'tweets': collected_tweets
    })

@app.route('/api/reset', methods=['POST'])
def reset_data():
    """
    Reset all collected data (useful for testing)
    """
    global collected_tweets, stats
    collected_tweets = []
    stats = {
        'total_collected': 0,
        'today_count': 0,
        'last_collection': None
    }
    return jsonify({
        'success': True,
        'message': 'All data reset'
    })

# Log all requests for debugging
@app.before_request
def log_request():
    print(f"\n📨 {request.method} {request.path}")
    if request.is_json:
        print(f"📦 Body: {request.json}")

@app.after_request
def log_response(response):
    print(f"✅ Response: {response.status_code}")
    return response

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🪄 Abra Code Abra - Simple Test Backend")
    print("="*60)
    print("\n📍 Server starting at: http://localhost:5000")
    print("📍 Dashboard: http://localhost:5000")
    print("📍 API Endpoint: http://localhost:5000/api/extension/collect")
    print("\n💡 Configure your Chrome extension to use: http://localhost:5000")
    print("\n⏸️  Press CTRL+C to stop\n")
    
    app.run(debug=True, port=5100, host='0.0.0.0')