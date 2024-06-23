class ActivityLogController {
    constructor() {
        this.bindEvents();
    }

    bindEvents() {
        document.getElementById('addEntryBtn').addEventListener('click', () => this.addEntry());
        document.getElementById('logForm').addEventListener('submit', (e) => this.handleSubmit(e));
    }

    addEntry() {
        const entriesDiv = document.getElementById('entries');
        const newEntry = entriesDiv.children[0].cloneNode(true);
        newEntry.querySelector('.week').value = '';
        newEntry.querySelector('.activity').value = '';
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
            document.getElementById('result').textContent = `${data.message}: ${data.filename}`;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ActivityLogController();
});