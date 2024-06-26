class ActivityLogController {
    constructor() {
        this.bindEvents();
        this.submitBtn = document.getElementById('submitBtn');
        this.resultDiv = document.getElementById('result');
    }

    bindEvents() {
        document.getElementById('addEntryBtn').addEventListener('click', () => this.addEntry());
        document.getElementById('logForm').addEventListener('submit', (e) => this.handleSubmit(e));
    }

    addEntry() {
        const entriesDiv = document.getElementById('entries');
        const newEntry = entriesDiv.children[0].cloneNode(true);
        newEntry.querySelector('.week').value = '';
        const newActivity = newEntry.querySelector('.activity');
        newActivity.value = '';
        newActivity.style.height = '2.5rem'; // Reset height to default
        newEntry.querySelector('.remove-entry').addEventListener('click', (e) => this.removeEntry(e.target));
        entriesDiv.appendChild(newEntry);
    }

    removeEntry(button) {
        if (document.querySelectorAll('.entry').length > 1) {
            button.closest('.entry').remove();
        }
    }

    getMondayOfWeek(weekString) {
        const [year, week] = weekString.split('-W');
        const simple = new Date(year, 0, 1 + (week - 1) * 7);
        const dayOfWeek = simple.getDay();
        const difference = simple.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
        return new Date(simple.setDate(difference));
    }

    formatDateUK(date) {
        return date.toLocaleDateString('en-GB', { day: '2-digit', month: '2-digit', year: 'numeric' });
    }

    handleSubmit(e) {
        e.preventDefault();
        this.setProcessingState(true);
        // this.resultDiv.textContent = 'Processing your request...';

        const entries = [];
        document.querySelectorAll('.entry').forEach(entry => {
            const weekValue = entry.querySelector('.week').value;
            const monday = this.getMondayOfWeek(weekValue);
            entries.push({
                week: this.formatDateUK(monday),
                description: entry.querySelector('.activity').value
            });
        });

        fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({entries: entries}),
        })
        .then(response => response.json())
        .then(data => {
            let resultsHtml = `<p>${data.message}</p>`;
            if (data.filenames && data.filenames.length > 0) {
                resultsHtml += '<ul>';
                data.filenames.forEach(filename => {
                    resultsHtml += `<li>${filename}</li>`;
                });
                resultsHtml += '</ul>';
            }
            this.resultDiv.innerHTML = resultsHtml;
        })
        .catch((error) => {
            console.error('Error:', error);
            this.resultDiv.textContent = 'An error occurred while processing your request.';
        })
        .finally(() => {
            this.setProcessingState(false);
        });
    }

    setProcessingState(isProcessing) {
        const defaultText = this.submitBtn.querySelector('.default-text');
        const processingText = this.submitBtn.querySelector('.processing-text');
        const spinner = this.submitBtn.querySelector('svg');

        if (isProcessing) {
            this.submitBtn.disabled = true;
            this.submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
            defaultText.classList.add('hidden');
            processingText.classList.remove('hidden');
            spinner.classList.remove('hidden');
        } else {
            this.submitBtn.disabled = false;
            this.submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            defaultText.classList.remove('hidden');
            processingText.classList.add('hidden');
            spinner.classList.add('hidden');
        }
    }
}
document.addEventListener('DOMContentLoaded', () => {
    new ActivityLogController();
});