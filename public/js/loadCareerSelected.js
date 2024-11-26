document.addEventListener("DOMContentLoaded", function () {
    const selectedCareer = JSON.parse(sessionStorage.getItem("selectedCareer"));

    if (selectedCareer) {
        // Populate the career details on the page
        document.getElementById("careerName").innerText = selectedCareer.name;
        document.getElementById("careerDescription").innerText = selectedCareer.description;
        document.getElementById("careerCost").innerText = `Cost: ${selectedCareer.cost}`;
    } else {
        // If no career was selected, display a message or redirect
        document.getElementById("selectedCareerDetails").innerText = "No career selected. Please go back and select a career.";
    }
})