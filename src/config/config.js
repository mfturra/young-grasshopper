export const appConfig = {
    width: 500,
    height: 500,
    backgroundColor: 0x55a341, // Use hexadecimal for PIXI background color
    antialias: true,
};

export const appStyles = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    border: "3px solid black",
    boxSizing: "border-box",
    borderRadius: "5px",
    padding: "8px",
    backgroundColor: '#FFBF00'
}

export const characterConfig = {
    texturePath: 'assets/sample_rocket.png',
    width: 100,
    height: 100,
    initialX: (screenWidth) => screenWidth / 2 - 50,
    initialY: 150 - 50,
    initialVel: { vx: 0, vy: 0 },
}

export const universityBoxConfig = {
    private: {
        // x: 80,
        // y: (screenWidth) => -175,
        x: 80,
        y: 300,
        width: 80,
        height: 60,
        color: 0x333333,
        text: "Private School"
    },
    public: {
        // x: (screenWidth) => -180,
        // y: (screenHeight) => 220,
        x: 340,
        y: 280,
        width: 60,
        height: 60,
        color: 0x333333,
        text: "Public School"
    }
}

// privateUniversity = createBox (
//     80,
//     app.screen.height - 175,
//     80,
//     60,
//     ,
    
// );

// const publicUniversity = createBox (
//     app.screen.width - 180,
//     app.screen.height - 220,
//     60,
//     60,
//     ,
    
// );