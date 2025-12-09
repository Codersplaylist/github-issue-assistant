/**
 * Frontend JavaScript for GitHub Issue Assistant
 * Handles form submission, API communication, and UI updates
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';

// State
let currentAnalysis = null;

// DOM Elements
const analyzeForm = document.getElementById('analyzeForm');
const repoUrlInput = document.getElementById('repoUrl');
const issueNumberInput = document.getElementById('issueNumber');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const resultsContent = document.getElementById('resultsContent');
const metadata = document.getElementById('metadata');
const copyBtn = document.getElementById('copyBtn');
const errorNotification = document.getElementById('errorNotification');
const successNotification = document.getElementById('successNotification');
const errorMessage = document.getElementById('errorMessage');
const successMessage = document.getElementById('successMessage');

// Example chips
const exampleChips = document.querySelectorAll('.chip');

/**
 * Initialize event listeners
 */
function init() {
    analyzeForm.addEventListener('submit', handleSubmit);
    // copyBtn.addEventListener('copy', handleCopyJSON); // Removed: handleCopyJSON is not defined and causing script error

    // Example chips click handlers
    exampleChips.forEach(chip => {
        chip.addEventListener('click', () => {
            const repo = chip.dataset.repo;
            const issue = chip.dataset.issue;
            repoUrlInput.value = repo;
            issueNumberInput.value = issue;

            // Add visual feedback
            chip.style.transform = 'scale(0.95)';
            setTimeout(() => {
                chip.style.transform = '';
            }, 200);
        });
    });
}

/**
 * Handle form submission
 */
async function handleSubmit(e) {
    e.preventDefault();

    const repoUrl = repoUrlInput.value.trim();
    const issueNumber = parseInt(issueNumberInput.value);

    // Validate inputs
    if (!repoUrl || !issueNumber || issueNumber < 1) {
        showError('Please provide a valid repository URL and issue number');
        return;
    }

    // Show loading state
    showLoading();

    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                repo_url: repoUrl,
                issue_number: issueNumber
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Analysis failed');
        }

        const data = await response.json();
        currentAnalysis = data;

        // Display results
        displayResults(data);
        showSuccess('Analysis completed successfully!');

    } catch (error) {
        console.error('Analysis error:', error);
        showError(error.message || 'Failed to analyze issue. Please check your inputs and try again.');
        hideLoading();
    }
}

/**
 * Display analysis results
 */
function displayResults(data) {
    // Hide loading
    hideLoading();

    // Build results HTML
    const html = `
        <div class="result-item">
            <div class="result-label">Summary</div>
            <div class="result-value">${escapeHtml(data.summary)}</div>
        </div>
        
        <div class="result-item">
            <div class="result-label">Type</div>
            <div class="result-value">
                <span class="type-badge type-${data.type}">${formatType(data.type)}</span>
            </div>
        </div>
        
        <div class="result-item">
            <div class="result-label">Priority Score</div>
            <div class="result-value">
                <div class="priority-score">
                    <span class="score-number">${data.priority_score.charAt(0)}</span>
                    <span>${data.priority_score.substring(2)}</span>
                </div>
            </div>
        </div>
        
        <div class="result-item">
            <div class="result-label">Suggested Labels</div>
            <div class="result-value">
                <div class="labels-container">
                    ${data.suggested_labels.map(label =>
        `<span class="label-tag">${escapeHtml(label)}</span>`
    ).join('')}
                </div>
            </div>
        </div>
        
        <div class="result-item">
            <div class="result-label">Potential Impact</div>
            <div class="result-value">${escapeHtml(data.potential_impact)}</div>
        </div>
    `;

    resultsContent.innerHTML = html;

    // Build metadata HTML
    if (data.metadata) {
        const metadataHtml = `
            ${data.metadata.issue_url ? `
                <div class="metadata-item">
                    <strong>Issue URL:</strong>
                    <a href="${data.metadata.issue_url}" target="_blank" style="color: var(--accent-cyan); text-decoration: none;">
                        View on GitHub →
                    </a>
                </div>
            ` : ''}
            ${data.metadata.issue_state ? `
                <div class="metadata-item">
                    <strong>State:</strong>
                    <span>${data.metadata.issue_state}</span>
                </div>
            ` : ''}
            ${data.metadata.comments_count !== undefined ? `
                <div class="metadata-item">
                    <strong>Comments:</strong>
                    <span>${data.metadata.comments_count}</span>
                </div>
            ` : ''}
            ${data.metadata.cached ? `
                <div class="metadata-item">
                    <strong>⚡ Cached result</strong>
                </div>
            ` : ''}
        `;
        metadata.innerHTML = metadataHtml;
    }

    // Show results section with animation
    resultsSection.style.display = 'block';
    resultsSection.style.animation = 'fadeInUp 0.6s ease-out';
}

/**
 * Show loading state
 */
function showLoading() {
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'block';
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<span>Analyzing...</span>';
}

/**
 * Hide loading state
 */
function hideLoading() {
    loadingSection.style.display = 'none';
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = `
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Analyze Issue</span>
    `;
}

/**
 * Handle copy JSON button
 */
copyBtn.addEventListener('click', async () => {
    if (!currentAnalysis) return;

    // Create clean JSON object (without metadata)
    const jsonToCopy = {
        summary: currentAnalysis.summary,
        type: currentAnalysis.type,
        priority_score: currentAnalysis.priority_score,
        suggested_labels: currentAnalysis.suggested_labels,
        potential_impact: currentAnalysis.potential_impact
    };

    try {
        await navigator.clipboard.writeText(JSON.stringify(jsonToCopy, null, 2));

        // Visual feedback
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = `
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none">
                <path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Copied!
        `;
        copyBtn.style.background = 'rgba(79, 172, 254, 0.2)';

        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.style.background = '';
        }, 2000);

        showSuccess('JSON copied to clipboard!');
    } catch (error) {
        showError('Failed to copy to clipboard');
    }
});

/**
 * Show error notification
 */
function showError(message) {
    errorMessage.textContent = message;
    errorNotification.style.display = 'flex';

    // Auto-hide after 5 seconds
    setTimeout(() => {
        closeNotification();
    }, 5000);
}

/**
 * Show success notification
 */
function showSuccess(message) {
    successMessage.textContent = message;
    successNotification.style.display = 'flex';

    // Auto-hide after 3 seconds
    setTimeout(() => {
        closeNotification();
    }, 3000);
}

/**
 * Close notifications
 */
function closeNotification() {
    errorNotification.style.display = 'none';
    successNotification.style.display = 'none';
}

/**
 * Format issue type for display
 */
function formatType(type) {
    return type.replace(/_/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize the application
init();
