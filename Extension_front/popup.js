const API_URL = 'https://supreme-invention-x56wxgxgxj67364w7-5000.app.github.dev';

document.addEventListener('DOMContentLoaded', () => {
    loadQuota();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('uploadBtn').addEventListener('click', () => {
        document.getElementById('fileInput').click();
    });

    document.getElementById('fileInput').addEventListener('change', handleFileSelect);
}

async function loadQuota() {
    try {
        const response = await fetch(`${API_URL}/quota`);
        const data = await response.json();

        const percentage = (data.used / data.limit) * 100;

        document.getElementById('quotaText').textContent =
            `${data.remaining} searches remaining this month (${data.used}/${data.limit})`;

        document.getElementById('quotaFill').style.width = `${percentage}%`;

        const fill = document.getElementById('quotaFill');
        if (percentage > 80) {
            fill.style.background = '#ef4444';
        } else if (percentage > 50) {
            fill.style.background = '#f59e0b';
        }

    } catch (error) {
        document.getElementById('quotaText').textContent =
            'Could not load quota. Is the API server running?';
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
        showError('Please select an image file');
        return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
        analyzeImage(event.target.result);
    };
    reader.readAsDataURL(file);
}

async function analyzeImage(imageDataUrl) {
    showLoading();
    hideError();

    try {
        document.getElementById('imagePreview').src = imageDataUrl;

        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: imageDataUrl
            })
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();

        hideLoading();

        if (data.success) {
            displayResults(data);
            loadQuota(); // Update quota
        } else {
            showError(data.error || 'Analysis failed');
        }

    } catch (error) {
        hideLoading();
        showError('Error: ' + error.message + '. Make sure the API server is running on localhost:5000');
    }
}

function displayResults(data) {
    document.getElementById('results').style.display = 'block';

    displayAIDetection(data.ai_detection);

    displayTinEyeResults(data.tineye);
}

function displayAIDetection(aiData) {
    const verdictBox = document.getElementById('verdictBox');
    const verdictIcon = document.getElementById('verdictIcon');
    const verdictTitle = document.getElementById('verdictTitle');
    const verdictDesc = document.getElementById('verdictDesc');

    verdictBox.className = 'verdict-box';

    if (aiData.verdict === 'High Risk') {
        verdictBox.classList.add('verdict-high');
        verdictIcon.textContent = '⚠️';
        verdictTitle.textContent = 'High Risk';
        verdictDesc.textContent = `${aiData.confidence}% confidence - Likely AI-generated or edited`;
    } else if (aiData.verdict === 'Medium Risk') {
        verdictBox.classList.add('verdict-medium');
        verdictIcon.textContent = '⚡';
        verdictTitle.textContent = 'Medium Risk';
        verdictDesc.textContent = `${aiData.confidence}% confidence - Suspicious patterns detected`;
    } else {
        verdictBox.classList.add('verdict-low');
        verdictIcon.textContent = '✅';
        verdictTitle.textContent = 'Low Risk';
        verdictDesc.textContent = `${aiData.confidence}% confidence - Likely authentic`;
    }

    if (aiData.is_ai_generated) {
        verdictDesc.textContent += ' (AI-generated)';
    } else if (aiData.is_photoshopped) {
        verdictDesc.textContent += ' (Photoshopped)';
    }

    const testsList = document.getElementById('testsList');
    testsList.innerHTML = '';

    aiData.tests.forEach(test => {
        const testItem = document.createElement('div');
        testItem.className = 'test-item';

        const testName = document.createElement('span');
        testName.className = 'test-name';
        testName.textContent = test.name;

        const testScore = document.createElement('span');
        testScore.className = 'test-score';

        if (test.score > 60) {
            testScore.classList.add('score-high');
        } else if (test.score > 40) {
            testScore.classList.add('score-medium');
        } else {
            testScore.classList.add('score-low');
        }

        testScore.textContent = `${test.score}%`;

        testItem.appendChild(testName);
        testItem.appendChild(testScore);
        testsList.appendChild(testItem);
    });
}

function displayTinEyeResults(tineyeData) {
    const container = document.getElementById('tinyeyeResults');

    if (tineyeData.error) {
        container.innerHTML = `
            <div class="error">
                <strong>TinEye Error:</strong> ${tineyeData.error}
                ${tineyeData.note ? `<p style="margin-top: 8px; font-size: 0.9em;">${tineyeData.note}</p>` : ''}
            </div>
        `;
        return;
    }

    container.innerHTML = `
        <div class="tineye-stats">
            <div class="big-number">${tineyeData.total_matches}</div>
            <div>Total matches found on the web</div>
        </div>
    `;

    if (tineyeData.first_appearance) {
        const firstAppearance = document.getElementById('firstAppearance');
        firstAppearance.style.display = 'block';

        document.getElementById('firstDate').textContent =
            new Date(tineyeData.first_appearance.date).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });

        const firstUrl = document.getElementById('firstUrl');
        firstUrl.href = tineyeData.first_appearance.url;
        firstUrl.textContent = tineyeData.first_appearance.domain;
    }

    if (tineyeData.top_matches && tineyeData.top_matches.length > 0) {
        const matchesContainer = document.getElementById('topMatches');
        matchesContainer.style.display = 'block';

        const matchesList = matchesContainer.querySelector('.matches-list') || matchesContainer;

        tineyeData.top_matches.forEach(match => {
            const matchItem = document.createElement('div');
            matchItem.className = 'match-item';

            matchItem.innerHTML = `
                <a href="${match.url}" target="_blank">${match.domain}</a>
                <div class="match-meta">
                    Crawled: ${new Date(match.crawl_date).toLocaleDateString()} • ${match.size}
                </div>
            `;

            matchesContainer.appendChild(matchItem);
        });
    }
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';

    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

function hideError() {
    document.getElementById('error').style.display = 'none';
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'analyzeImage') {
        analyzeImage(request.imageUrl);
    }
});
