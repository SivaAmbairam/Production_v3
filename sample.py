def run_sequence_of_scripts(script_names):
    global stop_execution
    for script_name in script_names:
        if stop_execution:
            logging.info(f"Execution stopped before running {script_name}")
            break
        run_script(script_name)


def run_sequence_scripts():
    try:
        global stop_execution
        stop_execution = False
        data = request.get_json()
        scripts = data.get('scripts', [])
        if not scripts:
            return jsonify({'status': 'No scripts selected.'})

        additional_scripts = ['Run_comparison.py']
        scripts.extend(additional_scripts)

        # Run the sequence of scripts in a separate thread
        threading.Thread(target=run_sequence_of_scripts, args=(scripts,)).start()
        return jsonify({'status': 'Scripts are running in sequence.'})
    except Exception as e:
        logging.error(f"Error running scripts in sequence: {str(e)}")
        return jsonify({'status': f'Error running scripts in sequence: {str(e)}'}), 500





const baseUrl = 'http://192.168.0.91:5000';
    document.getElementById('stop-button').addEventListener('click', function() {
    fetch(`${baseUrl}/stop_scripts`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    }).then(response => response.json())
        .then(data => {
            console.log(data.status);
            document.getElementById('run-button').disabled = false;
            document.getElementById('stop-button').disabled = true;
            document.getElementById('schedule-button').disabled = false;
            document.getElementById('stop-schedule-button').disabled = true;
            updateButtonColors();
            document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                checkbox.disabled = false;
            });
            saveState();

        }).catch(error => {
            console.error('Error stopping scripts:', error);
        });

});

<!--    document.getElementById('run-button').addEventListener('click', function() {-->
<!--    let formData = new FormData(document.getElementById('script-form'));-->

<!--    fetch(`${baseUrl}/run_scripts`, {-->
<!--        method: 'POST',-->
<!--        body: new URLSearchParams(formData)-->
<!--    }).then(response => response.json())-->
<!--        .then(data => {-->
<!--            let selectedScripts = formData.getAll('scripts');-->
<!--            let consolesDiv = document.getElementById('consoles');-->
<!--            consolesDiv.innerHTML = '';-->
<!--            selectedScripts.forEach(script => {-->
<!--                let consoleDiv = document.createElement('div');-->
<!--                consoleDiv.id = `console-${script}`;-->
<!--                consoleDiv.className = 'console-box';-->
<!--                consoleDiv.innerHTML = `<h3>${script}</h3><p>Status: Running</p><p>URLs Scraped: 0</p>`;-->
<!--                consolesDiv.appendChild(consoleDiv);-->
<!--            });-->
<!--            updateStatus();-->
<!--            document.getElementById('run-button').disabled = true;-->
<!--            document.getElementById('stop-button').disabled = false;-->
<!--            document.getElementById('schedule-button').disabled = true;-->
<!--            document.getElementById('stop-schedule-button').disabled = true;-->
<!--            updateButtonColors();-->
<!--            document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {-->
<!--                checkbox.disabled = true;-->
<!--            });-->
<!--            saveState(); // Save state immediately after updating UI-->
<!--        });-->
<!--});-->

document.getElementById('run-button').addEventListener('click', function() {
    let formData = new FormData(document.getElementById('script-form'));

    fetch(`${baseUrl}/run_scripts`, {
        method: 'POST',
        body: new URLSearchParams(formData)
    }).then(response => response.json())
        .then(data => {
            let selectedScripts = formData.getAll('scripts');
            let consolesDiv = document.getElementById('consoles');
            consolesDiv.innerHTML = '';
            selectedScripts.forEach(script => {
                let consoleDiv = document.createElement('div');
                consoleDiv.id = `console-${script}`;
                consoleDiv.className = 'console-box';

                let consoleHTML = `<h3>${script}</h3><p>Status: Running</p>`;

                if (script !== 'Run_comparison.py') {
                    consoleHTML += `<p>URLs Scraped: 0</p>`;
                }

                consoleDiv.innerHTML = consoleHTML;
                consolesDiv.appendChild(consoleDiv);
            });
            updateStatus();
            document.getElementById('run-button').disabled = true;
            document.getElementById('stop-button').disabled = false;
            document.getElementById('schedule-button').disabled = true;
            document.getElementById('stop-schedule-button').disabled = true;
            updateButtonColors();
            document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                checkbox.disabled = true;
            });
            saveState(); // Save state immediately after updating UI
        });
});

    document.getElementById('schedule-button').addEventListener('click', function() {
    let formData = new FormData(document.getElementById('script-form'));
    let checkedScripts = document.querySelectorAll('input[name="scripts"]:checked');

    if (checkedScripts.length > 0) {
        checkedScripts.forEach(script => {
            formData.append('scripts', script.value);
        });
        const startDate = document.getElementById('start-date').value;
        const startTime = document.getElementById('start-time').value;
        const recurrenceType = document.getElementById('recurrence-type').value;

        formData.append('start-date', startDate);
        formData.append('start-time', startTime);
        formData.append('recurrence-type', recurrenceType);

        fetch(`${baseUrl}/schedule_scripts`, {
            method: 'POST',
            body: formData
        }).then(response => response.json())
        .then(data => {
            if (data.status.startsWith('Scheduled')) {
                displayScheduledTask(data.status);
                document.getElementById('run-button').disabled = true;
                document.getElementById('run-button').style.backgroundColor = 'grey';
                document.getElementById('stop-button').disabled = true;
                document.getElementById('schedule-button').disabled = true;
                document.getElementById('stop-schedule-button').disabled = false;
                document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                checkbox.disabled = true;
            });
                updateButtonColors();
                saveState();
                window.stop_execution = false;
            } else {
                console.error('Scheduling error:', data.status);
                alert('Error scheduling script: ' + data.status);
            }
        }).catch(error => {
            console.error('Error scheduling script:', error);
            alert('An error occurred while scheduling the script. Please try again.');
        });
    } else {
        alert('Please select a script to schedule.');
    }
    saveState();
});

    document.getElementById('toggle-schedule-button').addEventListener('click', function() {
    const scheduleSection = document.getElementById('schedule-section');
    const toggleButton = document.getElementById('toggle-schedule-button');

    if (scheduleSection.style.display === 'none') {
        scheduleSection.style.display = 'block';
        toggleButton.textContent = 'Hide Schedule Options';
        toggleButton.classList.remove('collapsed');
    } else {
        scheduleSection.style.display = 'none';
        toggleButton.textContent = 'Show Schedule Options';
        toggleButton.classList.add('collapsed');
    }
});



    function displayScheduledTask(status) {
        let scheduledTaskInfo = document.getElementById('scheduled-task-info');
        scheduledTaskInfo.textContent = `Scheduled Task: ${status}`;
        document.getElementById('scheduled-task-display').style.display = 'block';
        document.getElementById('run-button').disabled = true;
    }

    function updateStatus() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            Object.keys(data).forEach(scriptName => {
                let statusText = data[scriptName];
                let urlCount = 0;
                let match = statusText.match(/URLs scraped: (\d+)/);
                if (match) {
                    urlCount = parseInt(match[1]);
                }
                let status = statusText.split('(')[0].trim();

                createOrUpdateConsoleDiv(scriptName, status, urlCount);
            });
            saveState();
            setTimeout(updateStatus, 1000);
        });
}


    updateStatus();

    document.getElementById('stop-schedule-button').addEventListener('click', function() {
    fetch(`${baseUrl}/stop_all`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.status);
        document.getElementById('scheduled-task-info').textContent = '';
        document.getElementById('scheduled-task-display').style.display = 'none';
<!--        document.getElementById('run-button').disabled = false;-->
<!--        document.getElementById('stop-button').disabled = true;-->
<!--        document.getElementById('schedule-button').disabled = false;-->
<!--        document.getElementById('stop-schedule-button').disabled = true;-->
            pollStatus();
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.disabled = false;
        });
        updateButtonColors();
        saveState();
        alert('All scheduled tasks and running scripts have been stopped.');
    })
    .catch(error => {
        console.error('Error stopping all tasks and scripts:', error);
        alert('An error occurred while stopping tasks and scripts. Please try again.');
    });
});

function pollStatus() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            const anyRunning = Object.values(data).some(status => status === 'Running' || status === 'Stopping');
            if (!anyRunning) {
                document.getElementById('run-button').disabled = false;
                document.getElementById('stop-button').disabled = true;
                document.getElementById('schedule-button').disabled = false;
                document.getElementById('stop-schedule-button').disabled = true;
                updateButtonColors();
                document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                    checkbox.disabled = false;
                });
                saveState();
            } else {
                // Continue polling if any scripts are still running
                setTimeout(pollStatus, 1000);
            }
        })
        .catch(error => {
            console.error('Error polling status:', error);
        });
}
<!--    function saveState() {-->
<!--    const checkboxes = document.querySelectorAll('input[type="checkbox"]');-->
<!--    const state = {-->
<!--        checkboxes: Array.from(checkboxes).map(cb => ({ id: cb.id, checked: cb.checked })),-->
<!--        runButtonDisabled: document.getElementById('run-button').disabled,-->
<!--        stopButtonDisabled: document.getElementById('stop-button').disabled,-->
<!--        startDate: document.getElementById('start-date').value,-->
<!--        startTime: document.getElementById('start-time').value,-->
<!--        recurrenceType: document.getElementById('recurrence-type').value-->
<!--    };-->
<!--    localStorage.setItem('pageState', JSON.stringify(state));-->
<!--}-->

function saveState() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const state = {
        checkboxes: Array.from(document.querySelectorAll('input[type="checkbox"]')).map(cb => ({ id: cb.id, checked: cb.checked, disabled: cb.disabled })),
        runButtonDisabled: document.getElementById('run-button').disabled,
        stopButtonDisabled: document.getElementById('stop-button').disabled,
        scheduleButtonDisabled: document.getElementById('schedule-button').disabled,
        stopScheduleButtonDisabled: document.getElementById('stop-schedule-button').disabled,
        startDate: document.getElementById('start-date').value,
        startTime: document.getElementById('start-time').value,
        recurrenceType: document.getElementById('recurrence-type').value,
        scheduledTaskDisplay: document.getElementById('scheduled-task-display').style.display,
        scheduledTaskInfo: document.getElementById('scheduled-task-info').textContent

    };
    localStorage.setItem('pageState', JSON.stringify(state));
}

<!--function loadState() {-->
<!--    const savedState = localStorage.getItem('pageState');-->
<!--    if (savedState) {-->
<!--        const state = JSON.parse(savedState);-->

<!--        // Restore checkboxes-->
<!--        state.checkboxes.forEach(cb => {-->
<!--            const checkbox = document.getElementById(cb.id);-->
<!--            if (checkbox) checkbox.checked = cb.checked;-->
<!--        });-->

<!--        // Restore button states-->
<!--        document.getElementById('run-button').disabled = state.runButtonDisabled;-->
<!--        document.getElementById('stop-button').disabled = state.stopButtonDisabled;-->

<!--        // Restore scheduled task display-->
<!--        document.getElementById('scheduled-task-display').style.display = state.scheduledTaskDisplay;-->
<!--        document.getElementById('scheduled-task-info').textContent = state.scheduledTaskInfo;-->

<!--        // Restore schedule inputs-->
<!--        document.getElementById('start-date').value = state.startDate;-->
<!--        document.getElementById('start-time').value = state.startTime;-->
<!--        document.getElementById('recurrence-type').value = state.recurrenceType;-->

<!--        // Update button colors-->
<!--        updateButtonColors();-->
<!--    }-->
<!--}-->

<!--function loadState() {-->
<!--    return new Promise((resolve, reject) => {-->
<!--        const savedState = localStorage.getItem('pageState');-->
<!--        if (savedState) {-->
<!--            const state = JSON.parse(savedState);-->

<!--            // Restore checkboxes-->
<!--            state.checkboxes.forEach(cb => {-->
<!--                const checkbox = document.getElementById(cb.id);-->
<!--                if (checkbox) checkbox.checked = cb.checked;-->
<!--            });-->

<!--            // Restore schedule inputs-->
<!--            document.getElementById('start-date').value = state.startDate;-->
<!--            document.getElementById('start-time').value = state.startTime;-->
<!--            document.getElementById('recurrence-type').value = state.recurrenceType;-->
<!--        }-->

<!--        // Fetch current scheduling status from server-->
<!--        fetch('/get_scheduling_status')-->
<!--            .then(response => response.json())-->
<!--            .then(data => {-->
<!--                if (data.status === 'Scheduled') {-->
<!--                    let tasksInfo = data.tasks.map(task =>-->
<!--                        `${task.script_name} scheduled for ${task.run_date} at ${task.run_time} (${task.status})`-->
<!--                    ).join(', ');-->
<!--                    document.getElementById('scheduled-task-info').textContent = tasksInfo;-->
<!--                    document.getElementById('scheduled-task-display').style.display = 'block';-->
<!--                    document.getElementById('run-button').disabled = data.any_running;-->
<!--                    document.getElementById('stop-button').disabled = !data.any_running;-->
<!--                } else {-->
<!--                    document.getElementById('scheduled-task-display').style.display = 'none';-->
<!--                    document.getElementById('run-button').disabled = false;-->
<!--                    document.getElementById('stop-button').disabled = true;-->
<!--                }-->
<!--                updateButtonColors();-->
<!--                resolve();-->
<!--            })-->
<!--            .catch(error => {-->
<!--                console.error('Error fetching scheduling status:', error);-->
<!--                // If there's an error, assume no tasks are scheduled-->
<!--                document.getElementById('scheduled-task-display').style.display = 'none';-->
<!--                document.getElementById('run-button').disabled = false;-->
<!--                document.getElementById('stop-button').disabled = true;-->
<!--                updateButtonColors();-->
<!--                reject(error);-->
<!--            });-->
<!--    });-->
<!--}-->

function loadState() {
    return new Promise((resolve, reject) => {
        const savedState = localStorage.getItem('pageState');
        if (savedState) {
            const state = JSON.parse(savedState);

            // Restore checkboxes and other inputs
            state.checkboxes.forEach(cb => {
                const checkbox = document.getElementById(cb.id);
                if (checkbox) {
                    checkbox.checked = cb.checked;
                    checkbox.disabled = cb.disabled;
                }
            });
            document.getElementById('start-date').value = state.startDate;
            document.getElementById('start-time').value = state.startTime;
            document.getElementById('recurrence-type').value = state.recurrenceType;

            // Restore button states
            document.getElementById('run-button').disabled = state.runButtonDisabled;
            document.getElementById('stop-button').disabled = state.stopButtonDisabled;
            document.getElementById('schedule-button').disabled = state.scheduleButtonDisabled;
            document.getElementById('stop-schedule-button').disabled = state.stopScheduleButtonDisabled;


            // Restore scheduled task display
            document.getElementById('scheduled-task-display').style.display = state.scheduledTaskDisplay;
            document.getElementById('scheduled-task-info').textContent = state.scheduledTaskInfo;
        }

        // Check server status to ensure UI is in sync
        fetch('/check_running_scripts')
            .then(response => response.json())
            .then(runningData => {
                if (runningData.any_running) {
                    document.getElementById('run-button').disabled = true;
                    document.getElementById('stop-button').disabled = false;
                    document.getElementById('schedule-button').disabled = true;
                    document.getElementById('stop-schedule-button').disabled = true;
                } else {
                    return fetch('/get_scheduling_status');
                }
            })
            .then(response => response ? response.json() : null)
            .then(data => {
                if (data && data.any_scheduled) {
                    let tasksInfo = data.tasks.map(task =>
                        `${task.script_name} scheduled for ${task.run_date} at ${task.run_time} (${task.status})`
                    ).join(', ');
                    document.getElementById('scheduled-task-info').textContent = tasksInfo;
                    document.getElementById('scheduled-task-display').style.display = 'block';
                    document.getElementById('run-button').disabled = true;
                    document.getElementById('stop-button').disabled = true;
                    document.getElementById('schedule-button').disabled = true;
                    document.getElementById('stop-schedule-button').disabled = false;
                }
                updateButtonColors();
                resolve();
            })
            .catch(error => {
                console.error('Error checking script status:', error);
                reject(error);
            });
    });
}



<!--function updateButtonColors() {-->
<!--    const runButton = document.getElementById('run-button');-->
<!--    const stopButton = document.getElementById('stop-button');-->

<!--    runButton.style.backgroundColor = runButton.disabled ? 'grey' : '#28a745';-->
<!--    stopButton.style.backgroundColor = stopButton.disabled ? 'grey' : '#dc3545';-->
<!--}-->

function updateButtonColors() {
    const buttons = ['run-button', 'stop-button', 'schedule-button', 'stop-schedule-button'];
    buttons.forEach(buttonId => {
        const button = document.getElementById(buttonId);
        button.style.backgroundColor = button.disabled ? 'grey' : '#15a65e';
    });
}

    function setDefaultDateTime() {
        const now = new Date();

        // Set default date
        const year = now.getFullYear();
        const month = (now.getMonth() + 1).toString().padStart(2, '0');
        const day = now.getDate().toString().padStart(2, '0');
        document.getElementById('start-date').value = `${year}-${month}-${day}`;

        // Set default time
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        document.getElementById('start-time').value = `${hours}:${minutes}`;
    }

<!--function initializeConsoleDivs(scripts) {-->
<!--    let consolesDiv = document.getElementById('consoles');-->
<!--    consolesDiv.innerHTML = ''; // Clear existing content-->
<!--    scripts.forEach(scriptName => {-->
<!--        let consoleDiv = document.createElement('div');-->
<!--        consoleDiv.id = `console-${scriptName}`;-->
<!--        consoleDiv.className = 'console-box';-->
<!--        consoleDiv.innerHTML = `-->
<!--            <h3>${scriptName}</h3>-->
<!--            <p>Status: Not started</p>-->
<!--            <p>URLs Scraped: <span class="url-count">0</span></p>-->
<!--        `;-->
<!--        consolesDiv.appendChild(consoleDiv);-->
<!--    });-->
<!--}-->

function initializeConsoleDivs(scripts) {
    let consolesDiv = document.getElementById('consoles');
    consolesDiv.innerHTML = ''; // Clear existing content

    scripts.forEach(scriptName => {
        let consoleDiv = document.createElement('div');
        consoleDiv.id = `console-${scriptName}`;
        consoleDiv.className = 'console-box';

        let consoleHTML = `
            <h3>${scriptName}</h3>
            <p>Status: Not started</p>
        `;

        if (scriptName !== 'Run_comparison.py') {
            consoleHTML += `<p>URLs Scraped: <span class="url-count">0</span></p>`;
        }

        consoleDiv.innerHTML = consoleHTML;
        consolesDiv.appendChild(consoleDiv);
    });
}


<!--function createOrUpdateConsoleDiv(scriptName, status, urlCount) {-->
<!--    let consolesDiv = document.getElementById('consoles');-->
<!--    let consoleDiv = document.getElementById(`console-${scriptName}`);-->

<!--    if (!consoleDiv) {-->
<!--        consoleDiv = document.createElement('div');-->
<!--        consoleDiv.id = `console-${scriptName}`;-->
<!--        consoleDiv.className = 'console-box';-->
<!--        consolesDiv.appendChild(consoleDiv);-->
<!--    }-->

<!--    let oldUrlCount = parseInt(consoleDiv.querySelector('.url-count')?.textContent || '0');-->

<!--    consoleDiv.innerHTML = `-->
<!--        <h3>${scriptName}</h3>-->
<!--        <p>Status: ${status}</p>-->
<!--        <p>URLs Scraped: <span class="url-count ${urlCount > oldUrlCount ? 'updated' : ''}">${urlCount}</span></p>-->
<!--    `;-->

<!--    if (urlCount > oldUrlCount) {-->
<!--        setTimeout(() => {-->
<!--            consoleDiv.querySelector('.url-count').classList.remove('updated');-->
<!--        }, 1000);-->
<!--    }-->
<!--}-->

function updateConsoleDiv(scriptName, status, urlCount) {
    let consoleDiv = document.getElementById(`console-${scriptName}`);

    if (!consoleDiv) {
        console.error(`Console div for script "${scriptName}" not found.`);
        return;
    }

    let oldUrlCount = parseInt(consoleDiv.querySelector('.url-count')?.textContent || '0');

    consoleDiv.innerHTML = `
        <h3>${scriptName}</h3>
        <p>Status: ${status}</p>
        ${scriptName !== 'Run_comparison.py' ? `<p>URLs Scraped: <span class="url-count ${urlCount > oldUrlCount ? 'updated' : ''}">${urlCount}</span></p>` : ''}
    `;

    if (urlCount > oldUrlCount) {
        setTimeout(() => {
            consoleDiv.querySelector('.url-count').classList.remove('updated');
        }, 1000);
    }
}

window.addEventListener('DOMContentLoaded', function() {
    loadState().then(() => {
        const scheduleSection = document.getElementById('schedule-section');
        const toggleButton = document.getElementById('toggle-schedule-button');

        scheduleSection.style.display = 'none';
        toggleButton.textContent = 'Show Schedule Options';
        toggleButton.classList.add('collapsed');

        // Initialize console divs
        let scripts = Array.from(document.querySelectorAll('#script-form input[type="checkbox"]')).map(cb => cb.value);
        initializeConsoleDivs(scripts);

        // Start updating status
        updateStatus();
    }).catch(error => {
        console.error('Error loading state:', error);
    });
});

    // Call the function when the page loads
<!--    window.addEventListener('DOMContentLoaded', setDefaultDateTime);-->
