# About
Image Detective is a digital forensics tool designed to analyze images for signs of AI generation, manipulation (Photoshop), and to trace original sources across the web.
It combines custom computer vision algorithms with the TinEye API to provide a comprehensive transparency report for any image.

## Image Detective - AI Detection & Source Finder

A powerful Chrome extension that detects AI-generated images, Photoshop manipulation, and finds image sources across the web using advanced forensic analysis and reverse image search.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)


## Features

### **AI & Photoshop Detection**
- **Error Level Analysis (ELA)**: Identifies different compression levels to spot localized edits.
- **Noise Pattern Analysis**: Detects inconsistencies in pixel-level noise common in AI-generated content.
- **Color Distribution Analysis**: Analyzes histogram variance to find artificial color patterns.
- **Edge Consistency Analysis**: Scans for "too-perfect" or unnatural edges.

### **Reverse Image Search**
- Search millions of web pages to find image sources
- Identify first appearance online
- Track image usage across the internet
- Support for TinEye, SerpAPI (Google Lens), and other providers

### **Beautiful User Interface**
- Modern gradient design with dark theme
- Tab-based interface (Upload File / Image URL)
- Real-time analysis with loading states
- Color-coded confidence scores
- Detailed forensic test results

### **Usage Tracking**
- Monthly quota monitoring
- Visual progress bar
- Automatic quota reset each month

## Demo

### **Upload & Analyze**
1. Click extension icon
2. Upload image or paste URL
3. Get instant AI detection results
4. See reverse image search matches

### **Right-Click Analysis**
1. Right-click any image on the web
2. Select "Analyze with Image Detective"
3. Results appear instantly

### **Example Results**

 AI Detection: High Risk (72.5%)
 This image is likely AI-generated

Forensic Tests:
• ELA (Photoshop Detection): 65.0%
• Noise Pattern (AI Detection): 80.0%
• Color Distribution: 70.0%
• Edge Consistency: 75.0%

 Image Source Search
42 matches found on the web
First appeared: March 15, 2021 on example.com


## Installation

### Prerequisites

- **Python 3.8+**
- **Google Chrome** (or Chromium-based browser)
- **PyCharm** (recommended) or any Python IDE
- **Flask**

### Step 1: Clone or Download

```bash
[git clone https://github.com/yourusername/image-detective.git](https://github.com/ChennakesavaReddy-Cyber/Image_API.git)
cd image-detective
```

Or download ZIP and extract.

### Step 2: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Manual installation:**
```bash
pip install flask flask-cors opencv-python pillow numpy requests
```

### Step 3: Set Up Browser Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer mode** (toggle in top-right)
3. Click **Load unpacked**
4. Navigate to `Extension_front` folder
5. Click **Select Folder**
6. Extension is now installed!

### Step 4: Create Extension Icons (if missing)

```bash
cd Extension_front
mkdir icons
python create_icons.py  # Creates icon16.png, icon48.png, icon128.png
```


## Usage

### Starting the Backend Server

```bash
cd backend
python app.py
```

**You should see:**
```
============================================================
IMAGE DETECTIVE API SERVER
============================================================
Server running on: http://localhost:5000
Health check: http://localhost:5000/health
Get quota: http://localhost:5000/quota
Analyze endpoint: http://localhost:5000/analyze (POST)
============================================================
```

** Keep this terminal window open while using the extension!**

### Using the Extension

#### **Method 1: Upload Image**
1. Click the extension icon in Chrome toolbar
2. Click "Upload File" tab
3. Choose an image (JPG, PNG, GIF, WebP)
4. Wait 2-5 seconds for analysis
5. View results

#### **Method 3: Right-Click Context Menu**
1. Right-click any image on any webpage
2. Select "Analyze with Image Detective"
3. Results appear instantly

## How It Works

### AI Detection Algorithm

Image Detective uses 4 forensic tests to detect manipulation:

#### **1. Error Level Analysis (ELA)**
- Re-compresses the image at different quality levels
- Compares original vs. re-compressed version
- Edited areas compress differently than original areas
- **High score**: Likely Photoshopped

#### **2. Noise Pattern Analysis**
- Analyzes digital noise using Laplacian edge detection
- Real photos have random, natural noise
- AI-generated images have uniform noise patterns
- **High score**: Likely AI-generated

#### **3. Color Distribution**
- Creates histograms for RGB channels
- Measures color variance and distribution
- AI images often have unnatural color patterns
- **High score**: Suspicious color patterns

#### **4. Edge Consistency**
- Uses Canny edge detection algorithm
- Measures edge density and patterns
- AI images have inconsistent edges
- **High score**: Likely AI artifacts

### Final Verdict Calculation

python
overall_score = (ela_score + noise_score + color_score + edge_score) / 4

if overall_score > 70:
    verdict = "High Risk" (Likely AI/fake)
elif overall_score > 40:
    verdict = "Medium Risk" (Suspicious)
else:
    verdict = "Low Risk" (Likely authentic)

### Reverse Image Search

The extension searches for identical or similar images across the web:

1. **Image Hash Generation**: Creates perceptual hashes (pHash, dHash, aHash)
2. **API Query**: Sends image to reverse search API (TinEye or SerpAPI)
3. **Result Processing**: Identifies first appearance and top matches
4. **Display**: Shows when/where the image appeared online


## API Options

### Option 1: Mock Data (Default - FREE)

No API key required. Returns sample data for testing.

**Pros:**
- Free forever
- No signup required
- Works immediately

**Cons:**
- Fake results (always shows 42 matches)
- Not real reverse image search

### Option 2: TinEye API (Paid)

Professional reverse image search API.

**Setup:**

1. Sign up: https://api.tineye.com/
2. Purchase plan ($200 for 5,000 searches)
3. Set environment variable:

```bash
export TINEYE_API_KEY="your_tineye_key"
```

**Pricing:**
- **Bundles**: $200 for 5,000 searches (1 year expiry)
- **Monthly**: $300/month for 5,000 searches

### Option 3: Google Custom Search API

Google's official reverse image search.

**Setup:**

1. Go to: https://console.cloud.google.com/
2. Create project & enable Custom Search API
3. Get API key & Search Engine ID

**Pricing:**
- **FREE**: 100 queries/day
- **Paid**: $5 per 1,000 queries

---

## Project Structure

```
image-detective/
│
├── backend/                      # Flask API server
│   ├── app.py                   # Main server file
│   ├── test_api.py              # API testing script
│   └── requirements.txt         # Python dependencies
│
├── Extension_front/             # Chrome extension
│   ├── manifest.json           # Extension configuration
│   ├── popup.html             # Extension UI
│   ├── popup.js               # Extension logic
│   ├── styles.css             # Styling
│   ├── background.js          # Context menu handler
│   └── icons/                 # Extension icons
│       ├── icon16.png
│       ├── icon48.png
│       └── icon128.png
│
└── README.md                   # This file
```


## Configuration

### Backend Configuration

Edit `backend/app.py`:

```python
# Change server port
app.run(debug=True, port=5000, host='0.0.0.0')

# Change monthly quota limit
search_count = {'month': datetime.now().month, 'count': 0, 'limit': 100}

# Change maximum file size (in bytes)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### Extension Configuration

Edit `Extension_front/popup.js`:

```javascript
// Change API server URL
const API_URL = 'http://localhost:5000';

// Or use remote server
const API_URL = 'https://your-server.com';
```

### Color Theme Customization

Edit `Extension_front/styles.css`:

```css
/* Change gradient colors */
background: linear-gradient(135deg, #3533cd, #090852, #000000);

/* Change button colors */
background: linear-gradient(135deg, #3533cd, #764ba2);
```

---

## Troubleshooting

### Problem: "Could not load quota. Is the API server running?"

**Solution:**
```bash
cd backend
python app.py
```

Make sure you see: "Server running on: http://localhost:5000"

---

### Problem: Extension shows "404 Not Found"

**Solution:**
1. Check backend server is running
2. Visit http://localhost:5000/health in browser
3. Should return: `{"status": "ok"}`

---

### Problem: "Could not load icon" error when loading extension

**Solution:**

Create missing icons:

```bash
cd Extension_front
python create_icons.py
```

### Problem: Right-click context menu doesn't appear

**Solution:**
1. Go to `chrome://extensions/`
2. Find "Image Detective"
3. Click **Reload**
4. Try right-clicking again

---

### Problem: URL analysis doesn't work

**Cause:** CORS (Cross-Origin) restrictions

**Solution:**
1. Download the image instead
2. Use "Upload File" tab
3. Or use a proxy/CORS bypass

---

### Problem: All images show same score

**Note:** This is expected for certain image types:
- Screenshots = Always medium-high (they're digital, not camera photos)
- Digital art = Usually medium-high
- Stock photos = Usually low-medium

---

### Problem: Extension popup is blank

**Solution:**
1. Right-click extension popup
2. Select "Inspect"
3. Check Console tab for errors
4. Share error message for help

---

## Testing

### Test the Backend API

```bash
cd backend
python test_api.py
```

**Expected output:**
```
Testing Image Detective API:

1. Testing /health endpoint:
   Status Code: 200
   ✅ PASS

2. Testing /quota endpoint:
   Status Code: 200
   ✅ PASS

3. Testing /analyze endpoint:
   Status Code: 200
   ✅ PASS
```

### Test Cases

**Test 1: Real Photo (Low Risk)**
- Go to https://unsplash.com/
- Right-click any nature photo
- Expected: 15-35% score (Low Risk)

**Test 2: AI-Generated Image (High Risk)**
- Go to https://thispersondoesnotexist.com/
- Save the face image
- Upload to extension
- Expected: 60-80% score (High Risk)

**Test 3: Heavily Edited Photo (High Risk)**
- Google "photoshopped fail"
- Analyze any obviously edited image
- Expected: High ELA score (60%+)

---

## Contributing

Contributions are welcome! Here's how:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/image-detective.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Make changes
# Test thoroughly
# Submit PR
```

## Acknowledgments

- **OpenCV** - Computer vision library
- **TinEye** / **SerpAPI** - Reverse image search APIs
- **Flask** - Web framework
- **Pillow** - Image processing
- **Chrome Extensions API** - Browser integration
