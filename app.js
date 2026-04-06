const URL = "http://127.0.0.1:5000/";

/* ================= TASKS ================= */

function loadTasks() {
    fetch(URL + "/tasks")
    .then(res => res.json())
    .then(data => {
        let list = document.getElementById("taskList");
        list.innerHTML = "";

        data.tasks.forEach(task => {
            let li = document.createElement("li");

            li.innerHTML = `
                ${task.content} ${task.done ? "✅" : ""}
                <button onclick="deleteTask(${task.id})">❌</button>
            `;

            list.appendChild(li);
        });
    });
}

function addTask() {
    let content = document.getElementById("taskInput").value;

    fetch(URL + "/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: content })
    })
    .then(() => {
        document.getElementById("taskInput").value = "";
        loadTasks();
    });
}

function completeTask(id) {
    fetch(URL + "/tasks/" + id + "/complete", {
        method: "PATCH"
    }).then(loadTasks);
}

function deleteTask(id) {
    fetch(URL + "/tasks/" + id, {
        method: "DELETE"
    }).then(loadTasks);
}

/* ================= USERS ================= */

function loadUsers() {
    fetch(URL + "/users")
    .then(res => res.json())
    .then(data => {
        let table = document.getElementById("userTable");
        table.innerHTML = "";

        data.users.forEach(user => {
            let row = document.createElement("tr");

            row.innerHTML = `
                <td>${user.name}</td>
                <td>${user.lastname}</td>
                <td>${user.address.city}</td>
                <td>${user.address.country}</td>
                <td>${user.address.code}</td>
                <td>
                    <button onclick="deleteUser(${user.id})">❌</button>
                </td>
            `;

            table.appendChild(row);
        });
    });
}

function addUser() {
    let user = {
        name: document.getElementById("name").value,
        lastname: document.getElementById("lastname").value,
        address: {
            city: document.getElementById("city").value,
            country: document.getElementById("country").value,
            code: document.getElementById("code").value
        }
    };

    fetch(URL + "/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user)
    })
    .then(() => loadUsers());
}

function deleteUser(id) {
    fetch(URL + "/users/" + id, {
        method: "DELETE"
    }).then(loadUsers);
}

/* ================= INIT ================= */
window.onload = function() {
    loadTasks();
    loadUsers();
};