export const privateUniversityScene = new PIXI.Container();

const text = new PIXI.Text('Welcome to Private University!', {
    fontFamily: 'Arial',
    fontSize: 24,
    fill: 0xffffff,
    align: 'center',
});

text.x = 50;
text.y = 50;

privateUniversityScene.addChild(text);

export default privateUniversityScene;