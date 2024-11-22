import { scenes } from './scenes.js';

export function switchScene(targetScene) {
    if (!targetScene) {
        console.error("Invalid targetScene passed to switchScene");
        return;  // Early return if targetScene is invalid
    }

    // Hide all scenes
    scenes.children.forEach(scene => {
        scene.visible = false;
    });

    // Show the target scene
    targetScene.visible = true;
}
