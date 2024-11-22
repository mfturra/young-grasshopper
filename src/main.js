import * as Config from './config/config.js';
// import * as Utils from './utils/index.js';
import * as Scenes from './utils/scenes/scenes.js';
import { switchScene } from './utils/scenes/sceneSwitcher.js';
import mainScene from './utils/scenes/mainScene.js';
src/utils/scenes/mainScene.js

let entrydialogScript = {}

fetch('dialog_scripts/entry_dialog.json')
    .then(response => response.json())
    .then(data => {
        entrydialogScript = data;
    })
    .catch(error => console.error("Error loading dialog data:", error));

(async function() {
    // App config
    const app = new PIXI.Application(Config.appConfig);
    
    // Apply styles to the canvas
    Object.assign(app.view.style, Config.appStyles);

    // Append the canvas to the document body
    document.body.appendChild(app.view);

    // Add the main scene to the app stage (this makes it the starting scene)
    app.stage.addChild(mainScene);

    // // Create the rocket sprite
    // const rocketTexture = await PIXI.Assets.load(Config.characterConfig.texturePath);
    // const rocketship = new PIXI.Sprite(rocketTexture);
    
    // // Apply dimensions
    // rocketship.width = Config.characterConfig.width;
    // rocketship.height = Config.characterConfig.height;

    // // Set initial position
    // rocketship.x = Config.characterConfig.initialX(app.screen.width);
    // rocketship.y = Config.characterConfig.initialY;

    // // Set initial velocity
    // rocketship.vx = Config.characterConfig.initialVel.vx;
    // rocketship.vy = Config.characterConfig.initialVel.vy;

    // Add rocket to the stage
    app.stage.addChild(rocketship);

    // // config for privateUniversity
    // const privateUniversity = Utils.createBox(
    //     Config.universityBoxConfig.private.x,
    //     Config.universityBoxConfig.private.y,
    //     Config.universityBoxConfig.private.width,
    //     Config.universityBoxConfig.private.height,
    //     Config.universityBoxConfig.private.color,
    //     Config.universityBoxConfig.private.text
    // );

    // // config for privateUniversity
    // const publicUniversity = Utils.createBox(
    //     Config.universityBoxConfig.public.x,
    //     Config.universityBoxConfig.public.y,
    //     Config.universityBoxConfig.public.width,
    //     Config.universityBoxConfig.public.height,
    //     Config.universityBoxConfig.public.color,
    //     Config.universityBoxConfig.public.text
    // );

   // Create the main scene (default screen)
   Scenes.mainScene.addChild(privateUniversity);
   Scenes.mainScene.addChild(publicUniversity);

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
        // Reset velocity
        rocketship.vx = 0;
        rocketship.vy = 0;
    
        // Handle movement based on keys pressed
        if (keys["ArrowUp"] || keys["w"]) rocketship.vy = -5;
        if (keys["ArrowDown"] || keys["s"]) rocketship.vy = 5;
        if (keys["ArrowLeft"] || keys["a"]) rocketship.vx = -5;
        if (keys["ArrowRight"] || keys["d"]) rocketship.vx = 5;
    
        // Calculate new position
        const newX = rocketship.x + rocketship.vx;
        const newY = rocketship.y + rocketship.vy;
    
        // Check for collisions
        const collisionResult = checkCollisions(newX, newY, rocketship, boxes);
    
        if (collisionResult === "private") {
            console.log(Scenes.privateUniversityScene);
            switchScene(Scenes.privateUniversityScene);
        } else if (collisionResult === "public") {
            console.log(Scenes.publicUniversityScene);  // Log the scene
            switchScene(Scenes.publicUniversityScene);
        } else {
            // Move the rocketship if no collision happens
            rocketship.x = newX;
            rocketship.y = newY;
        }
        requestAnimationFrame(gameLoop);

        function checkCollisions(newX, newY, sprite, boxes) {
            for (let box of boxes) {
                if (Utils.checkCollision(newX, newY, sprite, box)) {
                    if (box === privateUniversity) return "private";
                    if (box === publicUniversity) return "public";
                }
            }
            return null; // No collision
        }
        
    }

    // collision func

    gameLoop();
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