#!/bin/bash

# Quick Setup Script for Abra Code Abra Backend

echo "🪄 Abra Code Abra - Backend Setup"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Mac/Linux
    source venv/bin/activate
fi

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the backend:"
echo "   1. Activate venv: source venv/bin/activate"
echo "      (Windows: venv\\Scripts\\activate)"
echo "   2. Run: python app.py"
echo ""
echo "📍 Backend will run at: http://localhost:5000"
echo ""