# Abra Code Abra - Simple Test Backend

A minimal Flask backend to test your Chrome extension without needing database setup.

## ⚡ Quick Start (2 minutes)

### Option 1: Automatic Setup

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
python app.py
```

**Windows:**
```bash
setup.bat
venv\Scripts\activate
python app.py
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
python app.py
```

## 🎯 What You'll See

When you run `python app.py`, you should see:

```
============================================================
🪄 Abra Code Abra - Simple Test Backend
============================================================

📍 Server starting at: http://localhost:5000
📍 Dashboard: http://localhost:5000
📍 API Endpoint: http://localhost:5000/api/extension/collect

💡 Configure your Chrome extension to use: http://localhost:5000

⏸️  Press CTRL+C to stop

 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

## 🌐 Open the Dashboard

Go to **http://localhost:5000** in your browser

You should see:
- ✅ Backend Running status
- 📊 Statistics (Total, Today, Last Collection)
- 📋 Recent feedback tweets (empty at first)
- Auto-refreshes every 5 seconds

## 🔧 Configure Chrome Extension

1. Open your Chrome extension popup
2. Set **API URL** to: `http://localhost:5000`
3. Add **Keywords**: `bug, issue, broken, crash, error`
4. Add **Monitored Accounts**: `@YourProduct` (optional)
5. Click **Save Configuration**
6. Click **Start Collecting**

## 🐦 Test Collection

1. Go to **Twitter/X** (https://twitter.com or https://x.com)
2. Browse your timeline
3. The extension will collect tweets matching your keywords
4. Go back to **http://localhost:5000** to see collected tweets!

## 📡 Available Endpoints

### Dashboard
- **URL**: `http://localhost:5000`
- **Method**: GET
- **Description**: Visual dashboard with auto-refresh

### Health Check
- **URL**: `http://localhost:5000/api/health`
- **Method**: GET
- **Description**: Check if backend is running

### Collect Tweets
- **URL**: `http://localhost:5000/api/extension/collect`
- **Method**: POST
- **Description**: Main endpoint for Chrome extension
- **Example Body**:
```json
{
  "tweets": [
    {
      "tweet_id": "123456789",
      "content": "Found a bug in the app!",
      "author_username": "johndoe",
      "created_at": "2024-01-30T10:00:00Z",
      "url": "https://twitter.com/johndoe/status/123456789"
    }
  ]
}
```

### Get Stats
- **URL**: `http://localhost:5000/api/extension/stats`
- **Method**: GET
- **Description**: Get statistics for extension

### Get All Tweets
- **URL**: `http://localhost:5000/api/tweets`
- **Method**: GET
- **Description**: Get all collected tweets

### Export Data
- **URL**: `http://localhost:5000/api/tweets/export`
- **Method**: GET
- **Description**: Export tweets as JSON

### Reset Data
- **URL**: `http://localhost:5000/api/reset`
- **Method**: POST
- **Description**: Clear all collected data

## 🧪 Test with curl

```bash
# Test the collect endpoint
curl -X POST http://localhost:5000/api/extension/collect \
  -H "Content-Type: application/json" \
  -d '{
    "tweets": [
      {
        "tweet_id": "test123",
        "content": "Found a bug in the app!",
        "author_username": "testuser",
        "created_at": "2024-01-30T10:00:00Z",
        "url": "https://twitter.com/testuser/status/test123"
      }
    ]
  }'
```

Expected response:
```json
{
  "success": true,
  "processed": 1,
  "total": 1,
  "message": "Successfully collected 1 tweet(s)"
}
```

## 📊 What Happens

1. **Chrome extension** scans Twitter/X pages
2. **Extracts tweets** matching your keywords
3. **Sends to backend** at `/api/extension/collect`
4. **Backend stores** tweets in memory
5. **Updates statistics** (total, count, timestamp)
6. **Dashboard shows** collected tweets
7. **Console logs** all activity

## 🎬 Demo Flow

For your hackathon presentation:

1. ✅ **Show empty dashboard** (http://localhost:5000)
2. ✅ **Load Chrome extension** and configure it
3. ✅ **Enable collection** in extension popup
4. ✅ **Go to Twitter** and scroll through feed
5. ✅ **Show dashboard updating** with collected tweets
6. ✅ **Show terminal logs** as tweets arrive in real-time
7. ✅ **Explain the flow** from browser → extension → backend

## 🐛 Troubleshooting

### Port 5000 already in use
**Solution**: Change port in `app.py`:
```python
app.run(debug=True, port=5001, host='0.0.0.0')
```
Then update Chrome extension config to `http://localhost:5001`

### Extension can't connect
**Problem**: CORS errors
**Solution**: Make sure flask-cors is installed:
```bash
pip install flask-cors
```

### No tweets showing up
**Check these:**
- [ ] Backend is running (check terminal)
- [ ] Extension is enabled (check popup)
- [ ] You're on Twitter/X website
- [ ] Keywords match tweet content
- [ ] Check browser console for errors (F12)
- [ ] Check extension console (right-click popup → Inspect)

### Backend crashes on request
**Solution**: Check terminal for error message
- Usually missing dependency or JSON parsing issue
- Make sure you're sending proper JSON format

## 📝 Features

✅ **No database needed** - Uses in-memory storage  
✅ **Visual dashboard** - See tweets in real-time  
✅ **Auto-refresh** - Updates every 5 seconds  
✅ **CORS enabled** - Works with Chrome extension  
✅ **Duplicate detection** - Won't store same tweet twice  
✅ **Detailed logging** - See all activity in terminal  
✅ **Multiple endpoints** - Easy debugging and testing  
✅ **Export capability** - Download tweets as JSON  

## 🚀 Next Steps

After testing with this simple backend:

1. ✅ Verify Chrome extension works end-to-end
2. ✅ Test different keywords and accounts
3. ✅ Prepare demo for hackathon
4. ⏩ Later: Add PostgreSQL database
5. ⏩ Later: Add AI processing (embeddings, clustering)
6. ⏩ Later: Add GitHub integration
7. ⏩ Later: Build full React dashboard

## 💡 Tips

- Keep terminal open to see real-time logs
- Refresh dashboard manually if auto-refresh fails
- Use `/api/reset` to clear data between tests
- Check both extension console and backend terminal for errors
- Test with simple keywords first (like "bug", "help")

## 📦 File Structure

```
backend/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── setup.sh           # Setup script (Mac/Linux)
├── setup.bat          # Setup script (Windows)
└── README.md          # This file
```

## 🎓 For Hackathon

This backend is perfect for:
- ✅ Quick testing and iteration
- ✅ Live demo during presentation
- ✅ Showing real-time data collection
- ✅ Explaining the architecture
- ✅ No complex setup needed

## 🤝 Need Help?

Common issues:
1. **Can't install flask**: Make sure you're in virtual environment
2. **Port conflict**: Change port number in app.py
3. **CORS errors**: Reinstall flask-cors
4. **No data showing**: Check extension is on Twitter and enabled

---

**Built for Agentathon 2026 | Presidency University**

Good luck with your hackathon! 🚀