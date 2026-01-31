document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('command-input');
    const outputDiv = document.getElementById('output');
    const terminalContainer = document.getElementById('terminal-container');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Focus input on click anywhere
    document.addEventListener('click', () => {
        input.focus();
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const command = input.value;
            
            // 1. Display the command the user typed
            const commandLine = document.createElement('div');
            commandLine.className = 'output-line command-history';
            commandLine.innerHTML = `<span class="prompt">guest</span><span class="path">~/bodomain.de</span><span>$</span> ${escapeHtml(command)}`;
            outputDiv.appendChild(commandLine);

            input.value = '';

            // 2. Handle 'clear' command client-side
            if (command.trim().toLowerCase() === 'clear') {
                outputDiv.innerHTML = '';
                return;
            }

            // 3. Send to backend
            fetch('/api/command/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ 'command': command })
            })
            .then(response => response.json())
            .then(data => {
                if (data.output) {
                    const responseLine = document.createElement('div');
                    responseLine.className = 'output-line';
                    responseLine.textContent = data.output; // Text content safely escapes
                    outputDiv.appendChild(responseLine);
                } else if (data.error) {
                    const errorLine = document.createElement('div');
                    errorLine.className = 'output-line';
                    errorLine.style.color = 'red';
                    errorLine.textContent = 'Error: ' + data.error;
                    outputDiv.appendChild(errorLine);
                }
                scrollToBottom();
            })
            .catch(error => {
                const errorLine = document.createElement('div');
                errorLine.className = 'output-line';
                errorLine.style.color = 'red';
                errorLine.textContent = 'Network Error';
                outputDiv.appendChild(errorLine);
                scrollToBottom();
            });
            
            scrollToBottom();
        }
    });

    function scrollToBottom() {
        terminalContainer.scrollTop = terminalContainer.scrollHeight;
    }

    function escapeHtml(text) {
        if (!text) return text;
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});
