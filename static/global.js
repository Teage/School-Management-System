// Global JavaScript for the application

//I have not use this script. Instead i used the flask method url_for to redirect the user to the dashboard page when the cancel button is clicked. But i have kept this script here in case i need to use it in the future.
addEventListener('DOMContentLoaded', function() {
    const btncancel = document.getElementById('cancel');
    if (btncancel) {
        btncancel.addEventListener('click', function() {
            window.location.href = '/dashboard';
        })}});