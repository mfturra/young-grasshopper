// wait to render page until after HTML page has loaded
document.addEventListener("DOMContentLoaded", function () {
    // Fetch the JSON file using HTTP request
    fetch('../dialog_scripts/entry_dialog.json')
        .then(response => response.json()) // convert raw text response to .json format
        .then(data => {
            // Review html body tag for all classes containing private-university
            const isPrivateUniversity = document.body.classList.contains("private-university");

            // When privateUniversity or publicUniversity is selected, populate universityData with that json data
            const universityData = isPrivateUniversity ? data.privateUniversity : data.publicUniversity;

            // Populate the welcome text with respective data from json file
            document.getElementById("welcomeText").innerText = universityData.welcomeText;

            // Cycle through all available career tracks
            for (let i = 1; i <= 3; i++) {
                // create var for career{i}
                const career = universityData[`career${i}`];

                // Extract and input necessary elements where necessary in HTML file
                if (career) {
                    const careerElement = document.getElementById(`career${i}`);
                    careerElement.querySelector(".career-name").innerText = career.name;
                    careerElement.querySelector(".career-description").innerText = career.description;
                    careerElement.querySelector(".career-cost").innerText = `Cost: ${career.cost}`;
                }
            }
        })
        .catch(error => console.error("Error loading university data:", error));
});
