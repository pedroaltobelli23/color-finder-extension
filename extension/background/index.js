chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "inject") {
      inject(message.tabId);
  }
});

function inject(tabId) {
  chrome.tabs.sendMessage(tabId, { message: "init" }, (res) => {
    if (res) {
      clearTimeout(timeout);
    }
  });

  var timeout = setTimeout(() => {
      chrome.scripting.insertCSS({ files: ["vendor/jquery.Jcrop.min.css"], target: { tabId } });
      chrome.scripting.insertCSS({ files: ["content/index.css"], target: { tabId } });

      chrome.scripting.executeScript({ files: ["vendor/jquery.min.js"], target: { tabId } });
      chrome.scripting.executeScript({ files: ["vendor/jquery.Jcrop.min.js"], target: { tabId } });
      chrome.scripting.executeScript({ files: ["content/crop.js"], target: { tabId } });
      chrome.scripting.executeScript({ files: ["content/index.js"], target: { tabId } });

      setTimeout(() => {
          chrome.tabs.sendMessage(tabId, { message: "init" });
      }, 100);
  }, 100);
}

chrome.runtime.onMessage.addListener((req, sender, res) => {
  if (req.message === 'capture') {
    chrome.tabs.query({active: true, currentWindow: true}, (tab) => {
      chrome.tabs.captureVisibleTab(tab.windowId, {format: req.format, quality: req.quality}, (image) => {
        res({message: 'image', image})
      })
    })
  }
  return true
})