document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Element Selection ---
    const leadForm = document.getElementById('lead-form');
    const searchQueryInput = document.getElementById('search-query');
    const maxResultsInput = document.getElementById('max-results');
    const startScrapingBtn = document.getElementById('start-scraping-btn');
    
    const progressSection = document.getElementById('progress-section');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    const statusMessage = document.getElementById('status-message');
    
    const resultsSummary = document.getElementById('results-summary');
    const downloadContainer = document.getElementById('download-container');
    const resultsTableContainer = document.getElementById('results-table-container');

    let statusInterval = null;
    let currentResults = [];

    // --- Event Listeners ---
    leadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = searchQueryInput.value.trim();
        if (!query) {
            alert('Please enter a search query.');
            return;
        }
        await startScraping(query, parseInt(maxResultsInput.value));
    });

    // --- Core Functions ---
    async function startScraping(query, maxResults) {
        if (statusInterval) clearInterval(statusInterval);
        resetUIForNewScrape();
        startScrapingBtn.disabled = true;
        progressSection.style.display = 'block';

        try {
            const response = await fetch('/api/start-scraping', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ query, max_results: maxResults })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to start scraping');
            }
            
            startProgressMonitoring();
        } catch (error) {
            handleScrapingError('Error starting scraping: ' + error.message);
        }
    }

    function startProgressMonitoring() {
        statusInterval = setInterval(async () => {
            try {
                const response = await fetch('/api/status');
                if (!response.ok) throw new Error('Could not fetch status.');
                
                const status = await response.json();
                updateProgressUI(status);
                
                if (!status.is_running) {
                    clearInterval(statusInterval);
                    statusInterval = null;
                    handleScrapingCompletion(status);
                }
            } catch (error) {
                handleScrapingError(error.message);
            }
        }, 1500); // Check every 1.5 seconds
    }

    function handleScrapingCompletion(status) {
        if (status.error) {
            handleScrapingError(status.error);
        } else if (status.results && status.results.length > 0) {
            currentResults = status.results;
            displayResults(currentResults);
            startScrapingBtn.textContent = '✅ Success!';
            startScrapingBtn.style.backgroundColor = 'var(--success-color)';
        } else {
            statusMessage.textContent = 'Scraping completed, but no leads were found.';
            resetUI();
        }
    }

    // --- UI Update Functions ---
    function updateProgressUI(status) {
        progressFill.style.width = status.progress + '%';
        progressText.textContent = `${status.progress}% Complete`;
        if (status.message) {
            statusMessage.textContent = status.message;
        }
        if (status.is_running) {
            startScrapingBtn.textContent = 'Scraping in Progress...';
        }
    }

    function displayResults(results) {
        // Show summary
        resultsSummary.innerHTML = `<strong>Scraping Complete!</strong> Found <strong>${results.length}</strong> leads.`;
        resultsSummary.classList.add('show');

        // Create and show download buttons
        createDownloadButtons();
        downloadContainer.classList.add('show');
        
        // Create and display results table
        const table = createTable(results);
        resultsTableContainer.innerHTML = '';
        resultsTableContainer.appendChild(table);
    }
    
    function createDownloadButtons() {
        downloadContainer.innerHTML = `
            <button id="download-json" class="secondary-button">Download JSON</button>
            <button id="download-csv" class="secondary-button">Download CSV</button>
        `;
        document.getElementById('download-json').addEventListener('click', () => downloadFile('json'));
        document.getElementById('download-csv').addEventListener('click', () => downloadFile('csv'));
    }

    function resetUI() {
        startScrapingBtn.disabled = false;
        startScrapingBtn.textContent = 'Start Scraping';
        startScrapingBtn.style.backgroundColor = 'var(--primary-color)';
    }

    function resetUIForNewScrape() {
        resetUI();
        progressSection.style.display = 'none';
        progressFill.style.width = '0%';
        progressText.textContent = 'Initializing...';
        statusMessage.textContent = '';
        resultsTableContainer.innerHTML = '';
        resultsSummary.innerHTML = '';
        resultsSummary.classList.remove('show');
        downloadContainer.innerHTML = '';
        downloadContainer.classList.remove('show');
        currentResults = [];
    }

    function handleScrapingError(errorMessage) {
        if (statusInterval) clearInterval(statusInterval);
        statusMessage.textContent = `Error: ${errorMessage}`;
        statusMessage.style.color = 'var(--error-color)';
        startScrapingBtn.textContent = 'Scraping Failed';
        startScrapingBtn.style.backgroundColor = 'var(--error-color)';
    }

    // --- Utility Functions ---
    function createTable(data) {
        const table = document.createElement('table');
        const thead = document.createElement('thead');
        const tbody = document.createElement('tbody');
        const headers = Object.keys(data[0]);
        
        const headerRow = document.createElement('tr');
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = headerText;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        
        data.forEach(row => {
            const tr = document.createElement('tr');
            headers.forEach(header => {
                const td = document.createElement('td');
                td.textContent = row[header] || '';
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });

        table.appendChild(thead);
        table.appendChild(tbody);
        return table;
    }

    function downloadFile(format) {
        if (currentResults.length === 0) return;
        const query = searchQueryInput.value.trim().replace(/\s+/g, '_');
        const filename = `leads_${query || 'export'}.${format}`;
        let content = '';
        let mimeType = '';

        if (format === 'json') {
            content = JSON.stringify(currentResults, null, 2);
            mimeType = 'application/json';
        } else { // csv
            content = Papa.unparse(currentResults);
            mimeType = 'text/csv';
        }

        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    window.addEventListener('beforeunload', () => {
        if (statusInterval) clearInterval(statusInterval);
    });
}); 