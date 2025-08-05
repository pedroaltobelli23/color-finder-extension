// Crop Button
document.getElementById("injectButton").addEventListener("click", async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.runtime.sendMessage({ action: "inject", tabId: tab.id});

    const h3 = document.createElement("h3");
    h3.textContent = "Select area in the current tab";
    h3.id = "injectMessage";
    document.body.appendChild(h3);
});

document.addEventListener("DOMContentLoaded", function () {
    const body = document.body;
    const themeIcon = document.getElementById("themeIcon");
    const themeToggle = document.getElementById("themeToggle");

    chrome.storage.local.get("openedByScript", (data) => {
        if (data.openedByScript) {
            chrome.storage.local.get('imagem', async function (data) {
                const imagem = data.imagem;
    
                // Step 1: Remove the button and text
                const button = document.getElementById("injectButton");
                const divText = document.getElementById("injectButtonDiv");
                if (button) button.remove();
                if (divText) divText.remove();
    
                // Step 2: Show loading screen
                const container = document.getElementById('imageContainer');
                const loadingDiv = document.createElement('div');
                loadingDiv.id = "loadingScreen";
                loadingDiv.innerHTML = `
                    <div class="d-flex flex-column align-items-center my-4">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <h5 class="mt-2">Analyzing image...</h5>
                    </div>`;
                container.appendChild(loadingDiv);
    
                try {
                    const response = await fetch('http://localhost:5000/api/image/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ image: imagem })
                    });
    
                    const result = await response.json();
                    console.log("API result:", result);

                    container.innerHTML = "";
                    console.log("pirnt de teste")
                    // container.innerHTML = result.resized_image
                    
                    // Wrapper Start
                    const wrapper = document.createElement('div');
                    wrapper.classList.add('wrapper');
                    wrapper.style.width = '600px'; // TODO: parameter not fixed value
                    wrapper.style.height = '400px'; // TODO: parameter not fixed value
                    
                    // Resized Image
                    const resized = document.createElement('img');
                    resized.src = 'data:image/png;base64,' + result.resized_image;
                    resized.classList.add('resized');

                    // Quantizated Image
                    const quantized = document.createElement('img');
                    quantized.src = 'data:image/png;base64,' + result.quantized_image;
                    quantized.classList.add('quantized');

                    // Tooltip
                    const tooltip = document.createElement('div');
                    tooltip.style.position = 'absolute';
                    tooltip.style.background = '#000000cc';
                    tooltip.style.color = '#fff';
                    tooltip.style.padding = '4px 8px';
                    tooltip.style.borderRadius = '4px';
                    tooltip.style.fontSize = '14px';
                    tooltip.style.pointerEvents = 'none';
                    tooltip.style.display = 'none';
                    tooltip.style.zIndex = '10';

                    // Append wrapper to container
                    wrapper.appendChild(resized);
                    wrapper.appendChild(quantized);
                    wrapper.appendChild(tooltip);
                    container.appendChild(wrapper);

                    // Canvas to read pixels
                    const canvas = document.createElement('canvas');
                    canvas.width = 600;
                    canvas.height = 400;
                    canvas.style.display = 'none';
                    document.body.appendChild(canvas);


                    const ctx = canvas.getContext('2d');

                    quantized.onload = () => {
                        ctx.drawImage(quantized, 0, 0, 600, 400);
                    };

                    // Inverter dicionário de cores (RGB → nome)
                    const rgbToName = {};
                    for (const [name, rgb] of Object.entries(result.colors)) {
                        rgbToName[rgb.join(',')] = name;
                    }

                    // Evento de mouse move
                    wrapper.addEventListener('mousemove', (e) => {
                        const rect = wrapper.getBoundingClientRect();
                        const x = Math.floor(e.clientX - rect.left);
                        const y = Math.floor(e.clientY - rect.top);

                        const pixel = ctx.getImageData(x, y, 1, 1).data;
                        const rgbKey = `${pixel[2]},${pixel[1]},${pixel[0]}`;
                        const colorName = rgbToName[rgbKey] || `rgb(${rgbKey})`;

                        console.log(colorName);
                        
                        tooltip.textContent = colorName;
                        tooltip.style.left = `${x + 10}px`;
                        tooltip.style.top = `${y + 10}px`;
                        tooltip.style.display = 'block';
                    });

                    // Esconder tooltip quando sai do wrapper
                    wrapper.addEventListener('mouseleave', () => {
                        tooltip.style.display = 'none';
                    });
                    
                } catch (error) {
                    console.error("API request failed:", error);
                    loadingDiv.innerHTML = `<h5 class="text-danger">Failed to analyze image.</h5>`;
                }
            });
        }
    
        chrome.storage.local.set({ openedByScript: false });
    });
    
    // Load saved theme
    chrome.storage.sync.get("theme", function (data) {
        if (data.theme === "dark") {
            body.classList.add("dark-mode");
            setIcon("dark");
        } else {
            body.classList.remove("dark-mode");
            setIcon("light");
        }
    });

    // Toggle dark mode
    themeToggle.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent navigation

        if (body.classList.contains("dark-mode")) {
            body.classList.remove("dark-mode");
            setIcon("light");
            chrome.storage.sync.set({ theme: "light" });
        } else {
            body.classList.add("dark-mode");
            setIcon("dark");
            chrome.storage.sync.set({ theme: "dark" });
        }
    });

    function setIcon(mode) {
        if (mode === "dark") {
            themeIcon.innerHTML = '<path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6m0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8M8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0m0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13m8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5M3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8m10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0m-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0m9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707M4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708"/>'
            themeIcon.classList.replace("bi-moon", "bi-sun");
        } else {
            themeIcon.innerHTML = '<path d="M6 .278a.77.77 0 0 1 .08.858 7.2 7.2 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277q.792-.001 1.533-.16a.79.79 0 0 1 .81.316.73.73 0 0 1-.031.893A8.35 8.35 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.75.75 0 0 1 6 .278M4.858 1.311A7.27 7.27 0 0 0 1.025 7.71c0 4.02 3.279 7.276 7.319 7.276a7.32 7.32 0 0 0 5.205-2.162q-.506.063-1.029.063c-4.61 0-8.343-3.714-8.343-8.29 0-1.167.242-2.278.681-3.286"/>';
            themeIcon.classList.replace("bi-sun", "bi-moon");
        }
    }
})