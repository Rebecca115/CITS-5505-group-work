<script>
    document.getElementById("search-button").addEventListener("click", function() {
        var query = document.getElementById("search-input").value;
        // Call a function to send query to backend API
        searchBackend(query);
    });

    function searchBackend(query) {
        // Use AJAX or fetch to send a request to your backend API with the query
        // Example using fetch:
        fetch('/search?query=' + query)
            .then(response => response.json())
            .then(data => {
                // Process the data returned from backend and update the UI accordingly
            })
            .catch(error => console.error('Error:', error));
    }
</script>
