import { privateUniversityScene } from './privateUniversityScene.js';
import { publicUniversityScene } from './publicUniversityScene.js';

// Create a container for all app scenes
export const scenes = new PIXI.Container();

// Create individual scenes
export const mainScene = new PIXI.Container();

// Add all scenes to the parent container
scenes.addChild(mainScene);
scenes.addChild(privateUniversityScene);
scenes.addChild(publicUniversityScene);

privateUniversityScene.visible = false; // Initially hide private university scene
publicUniversityScene.visible = false; // Initially hide p

// Set visibility: mainScene visible by default, others hidden
// scenes.children.forEach(scene => (scene.visible = false));
// mainScene.visible = true;
