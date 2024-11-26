import * as Config from '/Users/matheusturra/Documents/dev-ops/young-grasshopper/src/config/config.js';
import * as Utils from './index.js';

// Create container to for mainScene to house intro scene
export const mainScene = new PIXI.Container();  // Container for all elements in the main scene

// Create the rocket sprite
const rocketTexture = await PIXI.Assets.load(Config.characterConfig.texturePath);
const rocketship = new PIXI.Sprite(rocketTexture);

// Apply dimensions to rocket
rocketship.width = Config.characterConfig.width;
rocketship.height = Config.characterConfig.height;

// Set rocket initial position and velocity
rocketship.x = Config.characterConfig.initialX(app.screen.width);
rocketship.y = Config.characterConfig.initialY;
rocketship.vx = Config.characterConfig.initialVel.vx;
rocketship.vy = Config.characterConfig.initialVel.vy;

// config for privateUniversity
const privateUniversity = Utils.createBox(
    Config.universityBoxConfig.private.x,
    Config.universityBoxConfig.private.y,
    Config.universityBoxConfig.private.width,
    Config.universityBoxConfig.private.height,
    Config.universityBoxConfig.private.color,
    Config.universityBoxConfig.private.text
);

// config for privateUniversity
const publicUniversity = Utils.createBox(
    Config.universityBoxConfig.public.x,
    Config.universityBoxConfig.public.y,
    Config.universityBoxConfig.public.width,
    Config.universityBoxConfig.public.height,
    Config.universityBoxConfig.public.color,
    Config.universityBoxConfig.public.text
);

// Add the rocketship and university entries to the mainScene
mainScene.addChild(rocketship);
mainScene.addChild(publicUniversity);
mainScene.addChild(privateUniversity);

const welcomeText = new PIXI.Text('Welcome to the University Game!', {
    fontFamily: 'Arial',
    fontSize: 24,
    fill: 0xffffff,
    align: 'center',
});

welcomeText.x = 100;
welcomeText.y = 20;
mainScene.addChild(welcomeText);