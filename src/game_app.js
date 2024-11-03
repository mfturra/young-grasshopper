// import { 
//     Application,
//     Assets,
//     Container,
//     Text,
//     Graphics,
//     Sprite } from "pixi.js";

(async function() {

const app = new PIXI.Application({
    width: 500,
    height: 500,
    backgroundColor: "rgb(249, 238, 217)",
    antialias: true
});

// Center app into view
app.view.style.position = 'absolute';
app.view.style.top = '50%';
app.view.style.left = '50%';
app.view.style.transform = 'translate(-50%, -50%)';
document.body.appendChild(app.view);

// counter text element
let counterValue = 0; //initialize counter
const counterText = new PIXI.Text(`Counter: ${counterValue}`, {
    fontFamily: 'Arial',
    fontSize: 24,
    fill: 0xffffff,
    align: 'right'
});

counterText.anchor.set(1, 0); // anchor text to top-right corner of canvas
counterText.x = app.screen.width - 10;
counterText.y = 10;

app.stage.addChild(counterText);


// Load rocket
const rocketTexture = await PIXI.Assets.load('assets/sample_rocket.png');
const rocketship = PIXI.Sprite.from(rocketTexture);

// set sprite size relative to original size
rocketship.scale.set(0.25, 0.25);

// Set rocket position
rocketship.x = app.screen.width/2 - rocketship.width/2;
rocketship.y = app.screen.height/2 - rocketship.height/2;
rocketship.vx = 0;
rocketship.vy = 0;


// const text = new PIXI.Text('Welcome to App', {
//     fontFamily: 'Arial',
//     fontSize: 24,
//     fill: 0x333333,
//     align: 'center'
// });

// text.anchor.set(0.5);
// text.x = app.screen.width / 2;
// text.y = app.screen.height / 2;

// Add canvas to HTML doc
// app.stage.addChild(text);

// bottom left rectangle configs
const bottomLeftRect = new PIXI.Graphics();
bottomLeftRect.beginFill(0x333333);
bottomLeftRect.drawRect(0, 0, 80, 60);
bottomLeftRect.endFill();
bottomLeftRect.x = 80;
bottomLeftRect.y = app.screen.height - 200;

// bottom right rectangle configs
const bottomRightRect = new PIXI.Graphics();
bottomRightRect.beginFill(0x333333);
bottomRightRect.drawRect(0, 0, 60, 60);
bottomRightRect.endFill();
bottomRightRect.x = app.screen.width - 120;
bottomRightRect.y = app.screen.height - 200;

// stage the assets for canvas
app.stage.addChild(rocketship);
app.stage.addChild(bottomLeftRect);
app.stage.addChild(bottomRightRect);

const boxes = [bottomLeftRect, bottomRightRect];

// key event handlers
const keys = {};

window.addEventListener("keydown", (e) => { keys[e.key] = true; });
window.addEventListener("keyup", (e) => { keys[e.key] = false; });

// game functions
function updateCounter(value) {
    counterValue =+ value; // update counter value
    counterText.text = `Counter: ${counterValue}`;
}

function gameLoop() {
    // reset velocity
    rocketship.vx = 0;
    rocketship.vy = 0;

    // check for key inputs
    if (keys["ArrowUp"] || keys["w"]) rocketship.vy = -5;
    if (keys["ArrowDown"] || keys["s"]) rocketship.vy = 5;
    if (keys["ArrowLeft"] || keys["a"]) rocketship.vx = -5;
    if (keys["ArrowRight"] || keys["d"]) rocketship.vx = 5;

    const newX = rocketship.x + rocketship.vx;
    const newY = rocketship.y + rocketship.vy;

    // Check for collisions with boxes
    let collisionDetected = false;
    for (const box of boxes) {
        if (checkCollision(newX, newY, rocketship, box, 5)){
            collisionDetected = true;
            updateCounter(50);
            break;
        }
    }

    if (!collisionDetected) {
        rocketship.x = newX;
        rocketship.y = newY;
    }

    // Request next frame
    requestAnimationFrame(gameLoop);
}

// collision detection function
function checkCollision(x, y, sprite, box, buffer) {
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
        bottom: box.y + box.height - buffer,
    };

    //Check for overlap between rocket and boxes
    return (
        spriteBounds.right > boxBounds.left &&
        spriteBounds.left < boxBounds.right &&
        spriteBounds.bottom > boxBounds.top &&
        spriteBounds.top < boxBounds.bottom 
    );
}

// start game loop
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