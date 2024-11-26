document.addEventListener("DOMContentLoaded", function () {
    const selectedCareer = JSON.parse(sessionStorage.getItem("selectedCareer"));

    if (selectedCareer) {

        fetch('../dialog_scripts/entry_dialog.json')
        .then(response => response.json())
        .then(data => {
            // Review html body tag for all classes containing private-university
            const isPrivateUniversity = document.body.classList.contains("private-university");

            // When privateUniversity or publicUniversity is selected, populate universityData with that json data
            const universityData = isPrivateUniversity ? data.privateUniversity : data.publicUniversity;

            // Find the selected career details
            const career = Object.values(universityData).find(c => c?.name?.toLowerCase() === selectedCareer?.name?.toLowerCase());

            if (career && career.curriculum) {
                document.getElementById("career-name").innerText = career.name;
                document.getElementById("career-description").innerText = career.description;
                document.getElementById("career-cost").innerText = career.cost;

                // Render core courses
                const coreCoursesList = document.getElementById("core-courses");
                if (career.curriculum.coreCourses) {
                    career.curriculum.coreCourses.forEach(course => {
                        const listItem = document.createElement("li");
                        listItem.innerText = course;
                        coreCoursesList.appendChild(listItem);
                    });
                }

                // Render elective courses
                const electivesList = document.getElementById("elective-courses");
                if (career.curriculum.electives) {
                    career.curriculum.electives.forEach(course => {
                        const listItem = document.createElement("li");
                        listItem.innerText = course;
                        electivesList.appendChild(listItem);
                    });
                }
            } else {
                console.error("No curriculum found for the selected career.");
                document.getElementById("selectedCareerDetails").innerText =
                    "No curriculum data available for this career.";
            }
        })
        .catch(error => console.error("Error loading curriculum data:", error));
    } else {
        // If no career was selected, display a message or redirect
        document.getElementById("selectedCareerDetails").innerText = "No career selected. Please go back and select a career.";
    }
});


    //             if (career) {
    //                 const careerElement = document.getElementById(`career${i}`);
    //                 careerElement.querySelector(".career-name").innerText = career.name;
    //                 careerElement.querySelector(".career-description").innerText = career.description;
    //                 careerElement.querySelector(".career-cost").innerText = career.cost;
    //                 careerElement.querySelector(".core-courses").innerText = career.curriculum.coreCourses;
    //                 careerElement.querySelector(".elective-courses").innerText = career.curriculum.electives;
    //             }
    //         }
    //     })
    // } else {
    //     // If no career was selected, display a message or redirect
    //     document.getElementById("selectedCareerDetails").innerText = "No career selected. Please go back and select a career.";