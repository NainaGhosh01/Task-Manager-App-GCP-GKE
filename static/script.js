const API = "/tasks";

function loadTasks() {
    fetch(API)
        .then(res => res.json())
        .then(tasks => {
            const list = document.getElementById("taskList");
            list.innerHTML = "";
            tasks.forEach(task => {
                const li = document.createElement("li");
                li.innerHTML = `
                    ${task.title} [${task.status}]
                    <button onclick="completeTask(${task.id})">✔</button>
                    <button onclick="deleteTask(${task.id})">❌</button>
                `;
                list.appendChild(li);
            });
        });
}

function addTask() {
    const title = document.getElementById("title").value;
    fetch(API, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title})
    }).then(() => {
        document.getElementById("title").value = "";
        loadTasks();
    });
}

function completeTask(id) {
    fetch(`${API}/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({status: "completed"})
    }).then(loadTasks);
}

function deleteTask(id) {
    fetch(`${API}/${id}`, {method: "DELETE"})
        .then(loadTasks);
}

loadTasks();

