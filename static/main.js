const userForm = document.getElementById("userForm");

let users = [];
let editing = false;
let userId = null;

window.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch("/api/users");
    const data = await response.json();
    users = data;
    renderUser(users);
});

// Crear usuario
userForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = userForm["username"].value;
    const email = userForm["email"].value;
    const password = userForm["password"].value;

    if (!editing) {
    // enviar usuario al backend
    const response = await fetch("/api/users", {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify({
        username,
        email,
        password,
        }),
    });

    const newUser = await response.json();
    users.unshift(newUser);
    renderUser(users);
    } else {
    const response = await fetch(`/api/users/${userId}`, {
        method: "PUT",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify({
        username,
        email,
        password,
        }),
    });
    const updatedUser = await response.json();

    users = users.map((user) =>
        user.id === updatedUser.id ? updatedUser : user
    );
    renderUser(users);

    editing = false;
    userId = null;
    }
    userForm.reset();
    });

    function renderUser(users) {
    const userList = document.querySelector("#userList");
    userList.innerHTML = "";
    users.forEach((user) => {
    const userItem = document.createElement("li");
    userItem.classList = "list-group-item list-group-item-dark my-2";
    userItem.innerHTML = `
            <header class="d-flex justify-content-between align-items-center">
            <h3>${user.username}</h3>
            <div>
                <button data-id="${user.id}" class="btn-delete btn btn-danger btn-sm">Delete</button>
                <button data-id="${user.id}" class="btn-edit btn btn-secondary btn-sm">Edit</button>
            </div>
            </header>
            <p>${user.email}</p>
            <p class="text-truncate">${user.password}</p>
        `;

    // botón de eliminar
    const btnDelete = userItem.querySelector(".btn-delete");

    btnDelete.addEventListener("click", async (e) => {
        const response = await fetch(`/api/users/${user.id}`, {
        method: "DELETE",
        });

        const data = await response.json();

        users = users.filter((user) => user.id !== data.id);
        renderUser(users);
    });

    userList.appendChild(userItem);

    // botón de edición
    const btnEdit = userItem.querySelector(".btn-edit");

    btnEdit.addEventListener("click", async (e) => {
        const response = await fetch(`/api/users/${user.id}`);
        const data = await response.json();

        userForm["username"].value = data.username;
        userForm["email"].value = data.email;

        editing = true;
        userId = user.id;
    });
    });
}