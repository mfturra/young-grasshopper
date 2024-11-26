// Function to create box with specific configs
export function createBox(x, y, width, height, color, textContent) {
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