// Replace this placeholder with the HTTPS URL assigned to your deployed Flask API.
const API_BASE_URL = "https://quick-comment-analyzer-chromeextension.onrender.com";
const ANALYZE_ENDPOINT = `${API_BASE_URL}/api/v1/analyze`;

chrome.runtime.onInstalled.addListener(() => {
  // Avoid duplicate context-menu entries when the extension is reloaded.
  chrome.contextMenus.removeAll(() => {
    chrome.contextMenus.create({
      id: "analyzeSentiment",
      title: "Get Sentiment Rating",
      contexts: ["selection"]
    });
  });
});

async function showMessage(tabId, message) {
  if (typeof tabId !== "number") return;

  try {
    await chrome.scripting.executeScript({
      target: { tabId },
      func: (text) => window.alert(text),
      args: [message]
    });
  } catch (error) {
    console.error("Could not display the sentiment result:", error);
  }
}

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId !== "analyzeSentiment") return;

  const selectedText = (info.selectionText || "").trim();

  if (!selectedText) {
    await showMessage(tab?.id, "Please select some text before analyzing it.");
    return;
  }

  // A placeholder URL will fail until the real deployed backend URL is configured.
  if (API_BASE_URL.includes("YOUR-RENDER-SERVICE")) {
    await showMessage(
      tab?.id,
      "The Quick Comment Analyzer API has not been configured yet. Add your deployed HTTPS backend URL to background.js and manifest.json."
    );
    return;
  }

  try {
    const response = await fetch(ANALYZE_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ review: selectedText })
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.error || `API request failed (HTTP ${response.status}).`);
    }

    if (!data.stars || !data.label || !data.confidence) {
      throw new Error("The API returned an unexpected response.");
    }

    await showMessage(
      tab?.id,
      `Rating: ${data.stars}\nCategory: ${data.label}\nAI Confidence: ${data.confidence}`
    );
  } catch (error) {
    console.error("Sentiment analysis failed:", error);
    await showMessage(
      tab?.id,
      `Could not analyze this text. Please check your internet connection and try again.\n\nDetails: ${error.message}`
    );
  }
});