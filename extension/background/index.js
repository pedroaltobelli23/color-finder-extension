chrome.action.onClicked.addListener(() => {
  chrome.storage.local.set({ openedByScript: false }); // User clicked icon
  console.log("openedByScript Set to false");
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "inject") {
    inject(message.tabId, message.method);
  }
});

function inject(tabId, methodClick) {
  chrome.tabs.sendMessage(tabId, { message: "init", method: methodClick }, (res) => {
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
      chrome.tabs.sendMessage(tabId, { message: "init", method: methodClick });
    }, 100);
  }, 100);
}

chrome.runtime.onMessage.addListener((req, sender, res) => {
  if (req.message === 'capture') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tab) => {
      chrome.tabs.captureVisibleTab(tab.windowId, { format: req.format, quality: req.quality }, (image) => {
        res({ message: 'image', image })
      })
    })
  }

  if (req.message === 'returnImage') {
    if (req.data) {
      if (req.data.open) {
        // Save the image and open the popup
        chrome.storage.local.set({ imagem: req.data.image, openedByScript: true }, () => {
          console.log("Image saved in storage and Popup open.");
          chrome.action.openPopup();
          res({ fullPage: false })
        });
      } else {
        // Just save the image
        chrome.storage.local.set({ imagem: req.data.image }, () => {
          console.log("Image saved in storage.");
          res({ fullPage: true })
        });
      }
    }
  }

  return true
})