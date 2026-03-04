from flask import Flask, request, jsonify, render_template_string
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

def dashboard_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Abra Code Abra - Comments Dashboard</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style>
            :root {
                color-scheme: light;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1100px;
                margin: 0 auto;
                padding: 24px 16px 40px;
                background: #f9fafb;
                color: #111827;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 12px;
                margin-bottom: 20px;
            }
            .header h1 {
                margin: 0;
                font-size: 28px;
            }
            .status {
                background: #10b981;
                color: #ffffff;
                border-radius: 999px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 600;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 12px;
                margin-bottom: 20px;
            }
            .card {
                background: #ffffff;
                border-radius: 10px;
                padding: 16px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            }
            .label {
                color: #6b7280;
                font-size: 13px;
                margin-bottom: 8px;
            }
            .value {
                font-size: 26px;
                font-weight: 700;
            }
            .list {
                background: #ffffff;
                border-radius: 10px;
                padding: 16px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            }
            .list h2 {
                margin: 0 0 12px;
                font-size: 18px;
            }
            .item {
                border-left: 4px solid #3b82f6;
                padding: 12px;
                border-radius: 6px;
                background: #f9fafb;
                margin-bottom: 10px;
            }
            .item-meta {
                font-size: 13px;
                color: #6b7280;
                margin-bottom: 6px;
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }
            .item-text {
                line-height: 1.5;
                white-space: pre-wrap;
            }
            .empty {
                color: #9ca3af;
                padding: 20px;
                text-align: center;
            }
            a {
                color: #2563eb;
                text-decoration: none;
            }
            .footer {
                margin-top: 14px;
                color: #6b7280;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🪄 Abra Code Abra Dashboard</h1>
            <span class="status">Live</span>
        </div>

        <div class="stats">
            <div class="card">
                <div class="label">Total Comments</div>
                <div id="totalCollected" class="value">0</div>
            </div>
            <div class="card">
                <div class="label">Today's Count</div>
                <div id="todayCount" class="value">0</div>
            </div>
            <div class="card">
                <div class="label">Last Collection</div>
                <div id="lastCollection" class="value" style="font-size:16px;">Never</div>
            </div>
        </div>

        <div class="list">
            <h2>Recent Comments</h2>
            <div id="commentsList" class="empty">No comments collected yet. Start the extension and scan X/Twitter.</div>
        </div>

        <div class="footer">Auto-updates every 5 seconds · API: /api/dashboard/comments</div>

        <script>
            function escapeHtml(text) {
                const map = {
                    '&': '&amp;',
                    '<': '&lt;',
                    '>': '&gt;',
                    '"': '&quot;',
                    "'": '&#039;'
                };
                return String(text || '').replace(/[&<>"']/g, function(m) { return map[m]; });
            }

            function renderComments(comments) {
                const container = document.getElementById('commentsList');

                if (!comments || comments.length === 0) {
                    container.className = 'empty';
                    container.innerHTML = 'No comments collected yet. Start the extension and scan X/Twitter.';
                    return;
                }

                container.className = '';
                container.innerHTML = comments.map(function(comment) {
                    const author = escapeHtml(comment.author_username || 'unknown');
                    const text = escapeHtml(comment.content || '');
                    const createdAt = escapeHtml((comment.created_at || '').replace('T', ' ').replace('Z', ''));
                    const link = comment.url ? '<a href="' + encodeURI(comment.url) + '" target="_blank" rel="noopener noreferrer">Open Source</a>' : '';

                    return '<div class="item">' +
                        '<div class="item-meta"><strong>@' + author + '</strong><span>' + createdAt + '</span>' + (link ? '<span>' + link + '</span>' : '') + '</div>' +
                        '<div class="item-text">' + text + '</div>' +
                    '</div>';
                }).join('');
            }

            async function refreshDashboard() {
                try {
                    const response = await fetch('/api/dashboard/comments');
                    const data = await response.json();

                    document.getElementById('totalCollected').textContent = data.stats.total_collected;
                    document.getElementById('todayCount').textContent = data.stats.today_count;
                    document.getElementById('lastCollection').textContent = data.stats.last_collection || 'Never';
                    renderComments(data.comments || []);
                } catch (error) {
                    console.error('Dashboard refresh failed:', error);
                }
            }

            refreshDashboard();
            setInterval(refreshDashboard, 5000);
        </script>
    </body>
    </html>
    """


@app.route('/')
def home():
    """Default route serves dashboard"""
    return render_template_string(dashboard_html())


@app.route('/dashboard')
def dashboard():
    """Dedicated dashboard route for extension popup"""
    return render_template_string(dashboard_html())

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


@app.route('/api/dashboard/comments', methods=['GET'])
def dashboard_comments():
    """Dashboard data endpoint with most recent comments first."""
    recent_comments = list(reversed(collected_tweets[-20:]))
    return jsonify({
        'stats': stats,
        'comments': recent_comments
    })

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