export const publicUniversityScene = new PIXI.Container();

const text = new PIXI.Text('Welcome to Public University!', {
    fontFamily: 'Arial',
    fontSize: 24,
    fill: 0xffffff,
    align: 'center',
});

text.x = 50;
text.y = 50;

publicUniversityScene.addChild(text);

export default publicUniversityScene