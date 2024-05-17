$(function () {
    $('#username, #password').on('keypress', function (e) {
        if (e.which === 13) {
            e.preventDefault(); // Prevent default form submission behavior
            var username = $('#username').val();
            var password = $('#password').val();
            if (username && password) { 
                var query = username + '+' + password; // Concatenate username and password
                window.location.href = `/search?query=${encodeURIComponent(query)}`;
            }
        }
    });
});
