document.addEventListener('DOMContentLoaded', function() {
    // Завантаження проектів з localStorage або встановлення порожнього масиву, якщо нічого немає
    let projects = JSON.parse(localStorage.getItem('projects')) || [];

    function saveProjects() {
        localStorage.setItem('projects', JSON.stringify(projects));
    }

    function displayProjects() {
        const container = document.getElementById('projectContainer');
        container.innerHTML = '';

        projects.forEach((project, index) => {
            const projectCard = document.createElement('div');
            projectCard.className = 'project-card';
            projectCard.innerHTML = `
                <h3 class="project-title">${project.title}</h3>
                <p class="project-description">${project.description}</p>
                <p class="project-status">Status: ${project.status}</p>
                <button onclick="deleteProject(${index})">Видалити проект</button>
                <button onclick="editProject(${index})">Редагувати</button>
            `;
            container.appendChild(projectCard);
        });
    }

    window.deleteProject = function(index) {
        projects.splice(index, 1);
        saveProjects();
        displayProjects();
    };

    window.editProject = function(index) {
        const project = projects[index];
        document.getElementById('projectTitle').value = project.title;
        document.getElementById('projectDescription').value = project.description;
        document.getElementById('projectStatus').value = project.status;
        document.getElementById('projectModal').style.display = 'block';
        document.getElementById('saveProjectBtn').onclick = function() {
            saveEditedProject(index);
        }
    };

    function saveEditedProject(index) {
        const title = document.getElementById('projectTitle').value;
        const description = document.getElementById('projectDescription').value;
        const status = document.getElementById('projectStatus').value;

        if (title && description && status) {
            projects[index] = {
                id: projects[index].id,
                title: title,
                description: description,
                status: status
            };
            saveProjects();
            displayProjects();
            document.getElementById('projectModal').style.display = 'none';
        } else {
            alert('Будь ласка, заповніть всі поля.');
        }
    }

    document.getElementById('openModalBtn').addEventListener('click', function() {
        document.getElementById('projectModal').style.display = 'block';
        clearForm();  // Очистка форми при відкритті модального вікна для нового проекту
        document.getElementById('saveProjectBtn').onclick = function() {
            const newProject = {
                id: projects.length + 1,
                title: document.getElementById('projectTitle').value,
                description: document.getElementById('projectDescription').value,
                status: document.getElementById('projectStatus').value
            };
    
            if (newProject.title && newProject.description && newProject.status) {
                projects.push(newProject);
                saveProjects();
                displayProjects();
                document.getElementById('projectModal').style.display = 'none';
                clearForm();  // Додавання виклику clearForm тут
            } else {
                alert('ID проекту обов\'язковий.');
            }
        };
    });
    
    function clearForm() {
        document.getElementById('projectTitle').value = '';
        document.getElementById('projectDescription').value = '';
        document.getElementById('projectStatus').value = 'Not Started';
    }
    

    document.getElementById('cancelProjectBtn').addEventListener('click', function() {
        document.getElementById('projectModal').style.display = 'none';
    });

    displayProjects();
});
function clearForm() {
    document.getElementById("projectForm").reset();
}

// Приклад виклику clearForm після успішного створення проекту
function createProject() {
    const projectData = gatherProjectData(); // Збір даних з форми
    fetch('/api/projects', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(projectData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            clearForm(); // Очищення форми після успішного відправлення
            alert('Проект успішно створено!');
        } else {
            alert('Помилка при створенні проекту: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Помилка:', error);
    });
}
