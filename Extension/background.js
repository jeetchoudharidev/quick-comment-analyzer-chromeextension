chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "analyzeSentiment",
    title: "Get Sentiment Rating",
    contexts: ["selection"] 
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "analyzeSentiment") {
    const selectedText = info.selectionText;
    
    fetch('http://127.0.0.1:5000/api/v1/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ review: selectedText })
    })
    .then(response => response.json())
    .then(data => {
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: (stars, category, confidence) => {
          alert(`Rating: ${stars}\nCategory: ${category}\nAI Confidence: ${confidence}`);
        },
        args: [data.stars, data.label, data.confidence]
      });
    })
    .catch(error => {
      console.error(error);
    });
  }
});