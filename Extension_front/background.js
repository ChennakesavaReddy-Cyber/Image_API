chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: 'analyzeImage',
        title: 'Analyze with Image Detective',
        contexts: ['image']
    });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === 'analyzeImage') {
        const imageUrl = info.srcUrl;

        chrome.runtime.sendMessage({
            action: 'analyzeImage',
            imageUrl: imageUrl
        });
    }
});