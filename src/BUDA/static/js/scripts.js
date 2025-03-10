    // Function to confirm deletion

    let holdTimeout = {};

    function startHoldDelete(objectId,objectType) {
        let button = document.getElementById(`deleteBtn-${objectId}`);
        
        // Start shaking animation
        button.classList.add("shake");

        // Set timeout for 2 seconds before deleting
        holdTimeout[objectId] = setTimeout(() => {
            fetch(`/${objectType}/delete/${objectId}`, { method: "POST" })
                .then(data => showModalMessage("Narrative deleted successfully!"))
                .then(() => new Promise(resolve => setTimeout(resolve, 3000)))
                .then(data => { window.location.reload(); })
                .catch(error => alert("Error deleting object: " + error));
        }, 2000); // ✅ Delete only if held for 2 seconds
    }

    function cancelHoldDelete(objectId) {
        let button = document.getElementById(`deleteBtn-${objectId}`);

        // Stop shaking animation
        button.classList.remove("shake");

        // Clear timeout to prevent deletion if released early
        if (holdTimeout[objectId]) {
            clearTimeout(holdTimeout[objectId]);
        }
    }