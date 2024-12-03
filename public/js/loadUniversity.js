// wait to render page until after HTML page has loaded
document.addEventListener("DOMContentLoaded", function () {
    // Fetch the JSON file using HTTP request
    fetch('../../dialog_scripts/dialogV1.json')
    // fetch('../dialog_scripts/entry_dialog.json')
        .then(response => response.json()) // convert raw text response to .json format
        .then(data => {
            // Review html body tag for all classes containing private-university
            const isPrivateUniversity = document.body.classList.contains("private-university");

            // When privateUniversity or publicUniversity is selected, populate universityData with that json data
            const universityData = isPrivateUniversity ? data.privateUniversity : data.publicUniversity;

            // Populate the welcome text with respective data from json file
            document.getElementById("welcomeText").innerText = universityData.welcomeText;

            // Cycle through all available degree tracks
            for (let i = 1; i <= 3; i++) {
                // create var for degree{i}
                const degree = universityData[`degree${i}`];

                // Extract and input necessary elements where necessary in HTML file
                if (degree) {
                    const degreeElement = document.getElementById(`degree${i}`);
                    degreeElement.querySelector(".degree-name").innerText = degree.name;
                    degreeElement.querySelector(".degree-description").innerText = degree.description;
                    degreeElement.querySelector(".degree-cost").innerText = `Cost: ${degree.cost}`;
                    
                    // Add event listener to the select button
                    const button = degreeElement.querySelector(".degree-choice-btn");
                    button.addEventListener("click", function () {
                        // Store selected degree details in sessionStorage
                        sessionStorage.setItem("selectedDegree", JSON.stringify(degree));

                        // Navigate to the degreeSelected page
                        window.location.href = "degreeSelected.html";
                    });
                }
            }
        })
        .catch(error => console.error("Error loading university data:", error));
});
