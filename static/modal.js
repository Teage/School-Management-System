// function openAddStudentModalForm() {
//        fetch('/add_student')
//         .then(response => response.text())
//         .then(html => {
//             document.getElementById('modal-body').innerHTML = html;
//             document.getElementById("studentModal").style.display = "block";
//         });

//     }

//function to fetch the url of the given form 
function open_modal_box(url){
    fetch(url)
        .then(response => response.text())
        .then(html => {
            document.getElementById('modal-body').innerHTML = html;
            document.getElementById("dialog_box").style.display = "block";
        });
}
    

    document.getElementById('closeModal').addEventListener('click', function() {
        document.getElementById("dialog_box").style.display = "none";
    });

    document.addEventListener('click', function(event) {
        if (event.target.id === 'openModalBtn') {
            open_modal_box(url);
        }
        if (event.target.id === 'btn-add-teacher') {
            open_modal_box(url);
        }
        if (event.target.classList.contains('edit-student')) {
            const url = event.target.getAttribute('href');
            event.preventDefault();
            open_modal_box(url);
        }

        if(event.target.classList.contains('edit-teacher')){
            const url = event.target.getAttribute('href');
            event.preventDefault();
            open_modal_box(url);
        }
    })