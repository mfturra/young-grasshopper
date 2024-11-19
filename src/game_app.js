let entrydialogScript = {}

fetch('dialog_scripts/entry_dialog.json')
    .then(response => response.json())
    .then(data => {
        entrydialogScript = data;
    })
    .catch(error => console.error("Error loading dialog data:", error));

(async function() {
    const app = new PIXI.Application({
        width: 500,
        height: 500,
        backgroundColor: "#55a341",
        antialias: true
    });
    app.view.style.position = 'absolute';
    app.view.style.top = '50%';
    app.view.style.left = '50%';
    app.view.style.transform = 'translate(-50%, -50%)';
    document.body.appendChild(app.view);

    const rocketTexture = await PIXI.Assets.load('assets/sample_rocket.png');
    const rocketship = new PIXI.Sprite(rocketTexture);
    
    
    // set sprite size relative to original size
    // rocketship.scale.set(0.25, 0.25);
    rocketship.height = 100;
    rocketship.width = 100;
    
    rocketship.x = app.screen.width / 2 - rocketship.width / 2;
    rocketship.y = 150 - rocketship.height / 2;
    rocketship.vx = 0;
    rocketship.vy = 0;

    // Function to create box with specific configs
    function createBox(x, y, width, height, color, textContent) {
        const container = new PIXI.Container();
        
        // container should be located in specific location
        container.x = x;
        container.y = y;
        
        // box dimensions and color config
        const box = new PIXI.Graphics();
        box.beginFill(color);
        box.drawRect(0, 0, width, height);
        box.endFill();

        // box position
        box.x = 0;
        box.y = 0;

        const text = new PIXI.Text(textContent, {
            fontFamily: 'Arial',
            fontSize: 16,
            fill: 0xffffff, // White text
            align: 'center',
            wordWrap: true,
            wordWrapWidth: width - 10 // create slight padding inside box
        });

        // Position the text at the center of the box
        text.x = width / 2 - text.width / 2;
        text.y = height / 2 - text.height / 2;

        // Add both the box and the text to a container
        container.addChild(box);
        container.addChild(text);

        container.height = height;
        container.width = width;

        return container;
    }

    const privateUniversity = createBox (
        80,
        app.screen.height - 175,
        80,
        60,
        0x333333,
        "Private School"
    );

    const publicUniversity = createBox (
        app.screen.width - 180,
        app.screen.height - 220,
        60,
        60,
        0x333333,
        "Public School"
    );

    app.stage.addChild(rocketship);
    app.stage.addChild(privateUniversity);
    app.stage.addChild(publicUniversity);

    const boxes = [privateUniversity, publicUniversity];

    // Create a counter text element
    let counterValue = 0;
    const counterText = new PIXI.Text(`Debt Owed: ${counterValue}`, {
        fontFamily: 'Arial',
        fontSize: 24,
        fill: 0xffffff,
        align: 'right'
    });
    counterText.anchor.set(1, 0);
    counterText.x = app.screen.width - 10;
    counterText.y = 10;
    app.stage.addChild(counterText);

    
    // Function to update the counter value and display
    function updateCounter(value) {
        const incrementDuration = 1000;
        const startValue = counterValue;
        const endValue = counterValue + value;
        const startTime = performance.now();

        function animateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / incrementDuration, 1); // Cap at 1 (100%)
    
            // Interpolate the counter value
            const currentDisplayValue = Math.round(startValue + (endValue - startValue) * progress);
    
            // Update the counter text
            counterText.text = `Debt Owed: ${currentDisplayValue}`;
    
            // Continue animating if not yet complete
            if (progress < 1) {
                requestAnimationFrame(animateCounter);
            } else {
                // Finalize the counter value
                counterValue = endValue;
            }
        }
    
        requestAnimationFrame(animateCounter);
    }

    // Add references to the dialog box and buttons
    const questDialog = document.getElementById("quest-dialog");
    const career1Button = document.getElementById("career1-btn");
    const career2Button = document.getElementById("career2-btn");
    const career3Button = document.getElementById("career3-btn");
    const noButton = document.getElementById("no-btn");

    let dialogOpen = false;

    // Store collision states for each box to track if the rocket is currently colliding
    const collisionStates = boxes.map(() => false);

    const keys = {};
    window.addEventListener("keydown", (e) => { keys[e.key] = true; });
    window.addEventListener("keyup", (e) => { keys[e.key] = false; });

    function gameLoop() {
        rocketship.vx = 0;
        rocketship.vy = 0;

        if (keys["ArrowUp"] || keys["w"]) rocketship.vy = -5;
        if (keys["ArrowDown"] || keys["s"]) rocketship.vy = 5;
        if (keys["ArrowLeft"] || keys["a"]) rocketship.vx = -5;
        if (keys["ArrowRight"] || keys["d"]) rocketship.vx = 5;

        const newX = rocketship.x + rocketship.vx;
        const newY = rocketship.y + rocketship.vy;

        // console.log("Rocket:", rocketship.x, rocketship.y, rocketship);
        // console.log("Left Box:", boxes[0].x, boxes[0].y, boxes[0].width, boxes[0].height);
        // console.log("Right Box:", boxes[1].x, boxes[1].y, boxes[1].width, boxes[1].height);


        // Track if a collision is detected and handle each box separately
        for (let i = 0; i < boxes.length; i++) {
            const box = boxes[i];
            // console.log(`Checking collision with box ${i}`);

            
            
            const isColliding = checkCollision(newX, newY, rocketship, box);                        

            if (isColliding && !collisionStates[i] && !dialogOpen) {
                if (box === privateUniversity) {
                    document.getElementById('dialog-text').textContent = entrydialogScript.privateUniversity.welcomeText;
                    document.getElementById('career1-btn').textContent = entrydialogScript.privateUniversity.career1.name;
                    document.getElementById('career2-btn').textContent = entrydialogScript.privateUniversity.career2.name;
                    document.getElementById('career3-btn').textContent = entrydialogScript.privateUniversity.career3.name;
                } else if (box === publicUniversity) {
                    document.getElementById('dialog-text').textContent = entrydialogScript.publicUniversity.welcomeText;
                    document.getElementById('career1-btn').textContent = entrydialogScript.publicUniversity.career1.name;
                    document.getElementById('career2-btn').textContent = entrydialogScript.publicUniversity.career2.name;
                    document.getElementById('career3-btn').textContent = entrydialogScript.publicUniversity.career3.name;
                }
                
                // Show dialog box on collision
                questDialog.style.display = "block";
                dialogOpen = true;

                const activeBox = box;

                // cost of pursuing career1 track
                career1Button.onclick = () => {
                    if (activeBox === privateUniversity) { //private college
                        updateCounter(-40000);
                    } else if (activeBox === publicUniversity) { // public college
                        updateCounter(-30000);
                    }
                    closedialog();
                };

                // cost of pursuing career2 track
                career2Button.onclick = () => {
                    if (activeBox === privateUniversity) {
                        updateCounter(-40000);
                    } else if (activeBox === publicUniversity) {
                        updateCounter(-30000);
                    }
                    closedialog();
                };

                // cost of pursuing career3 track
                career3Button.onclick = () => {
                    if (activeBox === privateUniversity) {
                        updateCounter(40000);
                    } else if (activeBox === publicUniversity) {
                        updateCounter(30000);
                    }
                };

                noButton.onclick = closedialog;

                collisionStates[i] = true;

            } else if (!isColliding) {
                // Reset collision state when rocket exits collision
                collisionStates[i] = false;
            }
        };

        // Only update position if no collision detected
        rocketship.x = newX;
        rocketship.y = newY;

        requestAnimationFrame(gameLoop);
    }

    function checkCollision(x, y, sprite, box, buffer = 0) {
        const spriteBounds = {
            left: x + buffer,
            right: x + sprite.width - buffer,
            top: y + buffer,
            bottom: y + sprite.height - buffer
        };
        const boxBounds = {
            left: box.x + buffer,
            right: box.x + box.width - buffer,
            top: box.y + buffer,
            bottom: box.y + box.height - buffer
        };

        return (
            spriteBounds.right > boxBounds.left &&
            spriteBounds.left < boxBounds.right &&
            spriteBounds.bottom > boxBounds.top &&
            spriteBounds.top < boxBounds.bottom
        );
        
        
    }

    gameLoop();

    // Function to close the dialog box
    function closedialog() {
        questDialog.style.display = "none";
        dialogOpen = false;
    }
})();



// // canvas properties
// await app.init({ 
//     // resizeTo: window,
    
    
//     // antialias: true 
    

//     // width: 512,
//     // height: 512, 
//     // backgroundColor: 0x1099bb  

// app.canvas.style.position = 'absolute'
// document.body.appendChild(app.canvas);

// // build title for game
// const text = new Text({
//     text: 'Welcome Young Grasshopper',
//     style: {
//         // `fill` is the same as the `color` property
//         // in CSS.
//         fill: '#ffffff',
//         // Make sure you have the font is installed
//         // before you use it.
//         fontFamily: 'Press Start 2P',
//         fontSize: 20,
//         // fontStyle: 'italic',
//         fontWeight: 'bold',
//         stroke: { color: '#4a1850', width: 5 },
//         dropShadow: {
//             color: '#4a1850',
//             blur: 4,
//             angle: Math.PI / 6,
//             distance: 6,
//         },
//     }
// });


// // establish global location of specific elements
// const posX = -50 + app.screen.width / 2;
// const posY = -50 + app.screen.height / 2;

// // const rectangle = new Graphics()
// //     .rect(200, 200, 200, 180)
// //     .fill({
// //         color: 0x1099bb,
// //         alpha: 0.5
// //     })
// //     .stroke({
// //         width: 8,
// //         color: 0x00ff00
// //     });

// //     app.stage.addChild(rectangle);

// // Create container
// const gameContainer = new Container();
// app.stage.addChild(gameContainer)

// // load the sample image textures
// const rocketTexture = await Assets.load('assets/sample_rocket.png');
// const rocketship = Sprite.from(rocketTexture);

// // const bunnyTexture = await Assets.load('https://pixijs.com/assets/bunny.png');
// // const bunny = Sprite.from(bunnyTexture);
// // const sprite = Sprite.from(bunnyTexture);

// // game container build
// const container = new Container();

// container.position.set(200,200)
// const backgroundRec = new Graphics();
// backgroundRec.rect(200,200,200, 180);

// app.stage.addChild(container);
// container.addChild(backgroundRec);
// container.addChild(sprite);
// container.addChild(text)

// const x = sprite.getGlobalPosition().x;
// const y = sprite.getGlobalPosition().y;

// // log position
// console.log(`x: ${sprite.x}, y:${sprite.y}`);
// console.log(`x: ${x}, y:${y}`);
// // add to stage
// // app.stage.addChild(rocketship);
// // app.stage.addChild(bunny);

// // add to container
// gameContainer.addChild(rocketship)
// gameContainer.addChild(bunny)



// // set sprite size relative to original size
// rocketship.scale.set(0.25, 0.25);

// // translate sprite to specific location
// bunny.position.set(250, 250)


// 
// translate the sprite to a specific location


// sprite.position.set(250, 250)

// rotate the sprite
// modify anchor point
// sprite.pivot.set(0.5,0.5)

// sprite.rotation = Math.PI / 4;

    
// })();
// // const Application = PIXI.Application;

// (async () =>
// {
//     // initialize the application

//     
//     // create a new Sprite from an image path
//     // const rocketship = new Sprite(texture);

//     
// })




// const app = new PIXI.Application();
// await app.init({width: 640, height: 360 });

// // document.body.appendChild(app.view);