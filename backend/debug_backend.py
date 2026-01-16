"""
Debug script to check backend configuration
Run this from the backend/ folder: python debug_backend.py
"""

import os
import sys

print("=" * 60)
print("Backend Configuration Debugging")
print("=" * 60)
print()

# Check 1: Python version
print("✓ Checking Python version...")
print(f"  Python {sys.version}")
if sys.version_info < (3, 9):
    print("  ⚠️  WARNING: Python 3.9+ recommended")
print()

# Check 2: .env file exists
print("✓ Checking .env file...")
if os.path.exists(".env"):
    print("  ✅ .env file found")
    with open(".env", "r") as f:
        content = f.read()
        if "ANTHROPIC_API_KEY" in content:
            print("  ✅ ANTHROPIC_API_KEY found in .env")
            # Check if it's the placeholder
            if "your-key-here" in content or "sk-ant-your" in content:
                print("  ❌ ERROR: API key is still a placeholder!")
                print("  → Replace with your actual API key from console.anthropic.com")
        else:
            print("  ❌ ERROR: ANTHROPIC_API_KEY not found in .env")
else:
    print("  ❌ ERROR: .env file not found")
    print("  → Create backend/.env with your API key")
print()

# Check 3: Load environment variables
print("✓ Checking environment variables...")
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    if api_key.startswith("sk-ant-"):
        print(f"  ✅ API key loaded: {api_key[:20]}...")
    else:
        print(f"  ⚠️  WARNING: API key doesn't start with 'sk-ant-'")
        print(f"     Current value: {api_key[:20]}...")
else:
    print("  ❌ ERROR: ANTHROPIC_API_KEY not loaded from environment")
print()

# Check 4: Required packages
print("✓ Checking required packages...")
required_packages = {
    "fastapi": "fastapi",
    "uvicorn": "uvicorn",
    "pandas": "pandas",
    "anthropic": "anthropic",
    "python-dotenv": "dotenv",  # Package name vs import name differ!
    "pydantic": "pydantic"
}

missing_packages = []
for package_name, import_name in required_packages.items():
    try:
        __import__(import_name)
        print(f"  ✅ {package_name}")
    except ImportError:
        print(f"  ❌ {package_name} - NOT INSTALLED")
        missing_packages.append(package_name)

if missing_packages:
    print()
    print("  Install missing packages with:")
    print(f"  pip install {' '.join(missing_packages)}")
print()

# Check 5: Test Anthropic API
if api_key and api_key.startswith("sk-ant-"):
    print("✓ Testing Anthropic API connection...")
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            messages=[{"role": "user", "content": "Say 'API test successful!'"}]
        )
        
        print("  ✅ API connection successful!")
        print(f"  Response: {response.content[0].text}")
    except Exception as e:
        print(f"  ❌ API connection failed: {str(e)}")
        print()
        print("  Possible issues:")
        print("  1. Invalid API key")
        print("  2. Network connection problem")
        print("  3. API quota exceeded")
        print()
        print("  Check your API key at: https://console.anthropic.com/")
else:
    print("⚠️  Skipping API test (no valid API key)")
print()

# Check 6: Test file imports
print("✓ Checking backend files...")
files_to_check = ["main.py", "models.py", "ai_service.py"]
for file in files_to_check:
    if os.path.exists(file):
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file} - NOT FOUND")
print()

# Check 7: Test ai_service import
print("✓ Testing ai_service import...")
try:
    from ai_service import FinancialAIService
    print("  ✅ FinancialAIService imported successfully")
    
    # Try to initialize
    try:
        service = FinancialAIService()
        print("  ✅ FinancialAIService initialized")
    except ValueError as e:
        print(f"  ⚠️  Cannot initialize: {str(e)}")
except ImportError as e:
    print(f"  ❌ Import failed: {str(e)}")
print()

# Summary
print("=" * 60)
print("SUMMARY")
print("=" * 60)

issues = []

if not os.path.exists(".env"):
    issues.append("Create .env file in backend/ folder")

if api_key and (not api_key.startswith("sk-ant-") or "your-key-here" in api_key):
    issues.append("Add valid Claude API key to .env file")

if missing_packages:
    issues.append(f"Install missing packages: pip install {' '.join(missing_packages)}")

if issues:
    print()
    print("❌ ISSUES FOUND:")
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. {issue}")
    print()
    print("Fix these issues and run this script again.")
else:
    print()
    print("✅ Everything looks good!")
    print()
    print("Next steps:")
    print("  1. Start the backend: uvicorn main:app --reload")
    print("  2. Test the API at: http://localhost:8000/docs")
    print("  3. Start the frontend: npm run dev (from frontend folder)")

print("=" * 60)