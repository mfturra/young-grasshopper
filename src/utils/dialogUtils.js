// Track if a collision is detected and handle each box separately
for (let i = 0; i < boxes.length; i++) {
    const box = boxes[i];           
    
    const isColliding = Utils.checkCollision(newX, newY, rocketship, box);                        

    // Collision detection and scene switching logic
    app.ticker.add(() => {
        // Check for collision with private & public university
        if (Utils.checkCollision(newX, newY, rocketship, privateUniversity)) {
            Utils.switchScene(privateUniversityScene);
        } else if (Utils.checkCollision(newX, newY, rocketship, publicUniversity)) {
            Utils.switchScene(publicUniversityScene);
        }
    });

    if (Utils.checkCollision(newX, newY, rocketship, privateUniversity)){
        Utils.switchScene(privateUniversityScene);
    } else if (Utils.checkCollision(newX, newY, rocketship, publicUniversity)){
        Utils.switchScene(publicUniversityScene);
    }
    // if (isColliding && !collisionStates[i] && !dialogOpen) {
    //     if (box === privateUniversity) {
    //         document.getElementById('dialog-text').textContent = entrydialogScript.privateUniversity.welcomeText;
    //         document.getElementById('career1-btn').textContent = entrydialogScript.privateUniversity.career1.name;
    //         document.getElementById('career2-btn').textContent = entrydialogScript.privateUniversity.career2.name;
    //         document.getElementById('career3-btn').textContent = entrydialogScript.privateUniversity.career3.name;
    //     } else if (box === publicUniversity) {
    //         document.getElementById('dialog-text').textContent = entrydialogScript.publicUniversity.welcomeText;
    //         document.getElementById('career1-btn').textContent = entrydialogScript.publicUniversity.career1.name;
    //         document.getElementById('career2-btn').textContent = entrydialogScript.publicUniversity.career2.name;
    //         document.getElementById('career3-btn').textContent = entrydialogScript.publicUniversity.career3.name;
    //     }
        
    //     // Show dialog box on collision
    //     questDialog.style.display = "block";
    //     dialogOpen = true;

    //     const activeBox = box;

    //     // cost of pursuing career1 track
    //     career1Button.onclick = () => {
    //         if (activeBox === privateUniversity) { //private college
    //             updateCounter(-40000);
    //         } else if (activeBox === publicUniversity) { // public college
    //             updateCounter(-30000);
    //         }
    //         closedialog();
    //     };

    //     // cost of pursuing career2 track
    //     career2Button.onclick = () => {
    //         if (activeBox === privateUniversity) {
    //             updateCounter(-40000);
    //         } else if (activeBox === publicUniversity) {
    //             updateCounter(-30000);
    //         }
    //         closedialog();
    //     };

    //     // cost of pursuing career3 track
    //     career3Button.onclick = () => {
    //         if (activeBox === privateUniversity) {
    //             updateCounter(40000);
    //         } else if (activeBox === publicUniversity) {
    //             updateCounter(30000);
    //         }
    //     };

    //     noButton.onclick = closedialog;

    //     collisionStates[i] = true;

    // } else if (!isColliding) {
    //     // Reset collision state when rocket exits collision
    //     collisionStates[i] = false;
    // }
};

// Function to close the dialog box
function closedialog() {
    questDialog.style.display = "none";
    dialogOpen = false;
}