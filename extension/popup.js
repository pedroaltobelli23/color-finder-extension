document.getElementById("injectButton").addEventListener("click", async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.runtime.sendMessage({ action: "inject", tabId: tab.id });

    const h3 = document.createElement("h3");
    h3.textContent = "Injection started!";
    h3.id = "injectMessage";  // Set ID to prevent duplicates
    document.body.appendChild(h3);

    const bInject = document.getElementById("injectButton");
    bInject.disabled = true;
});