document.getElementById("injectButton").addEventListener("click", async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.runtime.sendMessage({ action: "inject", tabId: tab.id, method: 'crop' });

    const h3 = document.createElement("h3");
    h3.textContent = "Select area in the current tab";
    h3.id = "injectMessage";
    document.body.appendChild(h3);

    const button = document.getElementById("injectButton");
    button.disabled = true;
});

document.getElementById("fullpageButton").addEventListener("click", async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.runtime.sendMessage({ action: "inject", tabId: tab.id, method: 'page' });

    const button = document.getElementById("fullpageButton");
    button.disabled = true;
});