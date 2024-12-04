document.addEventListener("DOMContentLoaded", function () {
    const selectedDegree = JSON.parse(sessionStorage.getItem("selectedDegree"));

    if (selectedDegree) {

        fetch('../../dialog_scripts/dialogV1.json')
        .then(response => response.json())
        .then(data => {
            // Review html body tag for all classes containing private-university
            const isPrivateUniversity = document.body.classList.contains("private-university");

            // When privateUniversity or publicUniversity is selected, populate universityData with that json data
            const universityData = isPrivateUniversity ? data.privateUniversity : data.publicUniversity;

            // Find the selected degree details
            const degree = Object.values(universityData).find(c => c?.name?.toLowerCase() === selectedDegree?.name?.toLowerCase());

            if (degree && degree.curriculum) {
                document.getElementById("degree-name").innerText = degree.name;
                document.getElementById("degree-description").innerText = degree.description;
                document.getElementById("degree-cost").innerText = degree.cost;

                // Render core courses
                const coreCoursesList = document.getElementById("core-courses");
                if (degree.curriculum.coreCourses) {
                    degree.curriculum.coreCourses.forEach(course => {
                        const listItem = document.createElement("li");
                        listItem.innerText = course;
                        coreCoursesList.appendChild(listItem);
                    });
                }

                // Render elective courses
                const electivesList = document.getElementById("elective-courses");
                if (degree.curriculum.electives) {
                    degree.curriculum.electives.forEach(course => {
                        const listItem = document.createElement("li");
                        listItem.innerText = course;
                        electivesList.appendChild(listItem);
                    });
                }
            } else {
                console.error("No curriculum found for the selected degree.");
                document.getElementById("selectedDegreeDetails").innerText =
                    "No curriculum data available for this degree.";
            }
        })
        .catch(error => console.error("Error loading curriculum data:", error));
    } else {
        // If no degree was selected, display a message or redirect
        document.getElementById("selectedDegreeDetails").innerText = "No degree selected. Please go back and select a degree.";
    }
});