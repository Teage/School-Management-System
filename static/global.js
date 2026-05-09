// Global JavaScript for the application

//I have not use this script. Instead i used the flask method url_for to redirect the user to the dashboard page when the cancel button is clicked. But i have kept this script here in case i need to use it in the future.
addEventListener('DOMContentLoaded', function() {
    const btncancel = document.getElementById('cancel');
    if (btncancel) {
        btncancel.addEventListener('click', function() {
            window.location.href = '/dashboard';
        })}});


function loadPage(url) {
    fetch(url)
        .then(response => response.text())
        .then(html => {
            document.getElementById('content-area').innerHTML = html;
        });
}

document.querySelectorAll('.nav-link')
.forEach(link => {

    link.addEventListener('click', function(e){

        e.preventDefault();

        const url = this.getAttribute('href');

        loadPage(url);

    });

});

// function showSection(sectionId) {

//     let sections = document.querySelectorAll('.student-table');

//     sections.forEach(section => {
//         section.style.display = 'none';
//     });

//     document.getElementById(sectionId).style.display = 'block';
// }

// let links = document.querySelectorAll(".sidebar a");
// links.forEach(link =>{
//     link.addEventListener('click', () =>{
//         let section = link.getAttribute('data-section');
//         showSection(section); 
//     });
// });

// fetch('/api/students')
// .then(response => response.json())
// .then(data => {
//     let table = document.getElementById('student-table');
//     let tbody = table.querySelector('tbody');
//     data.forEach(student => {
//         let row = document.createElement('tr');
//         row.innerHTML = `
//             <td>${student.id}</td>
//             <td>${student.roll_number}</td>
//             <td>${student.first_name}</td>
//             <td>${student.last_name}</td>
//             <td>${student.phone}</td>
//             <td>${student.email}</td>
//             <td>${student.grade}</td>
//             <td>${student.date_of_birth}</td>
//             <td>${student.gender}</td>
//             <td>${student.address}</td>
//             <td>${student.enrollment_date}</td>
//             <td>${student.parent_name}</td>
//             <td>
//                 <button class="edit-button">Edit</button>
//                 <button class="delete-button">Delete</button>
//             </td>
//         `;
//         tbody.appendChild(row);
//     });
// })