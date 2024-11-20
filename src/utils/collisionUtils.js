export function checkCollision(x, y, sprite, box, buffer = 0) {
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