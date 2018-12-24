getRandom = function(min, max) {
    return Math.random() * (max - min) + min;
};

getRandomInt = function(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};

generateData = function() {
    var payload = getRandom(50,70);     // Random number between 50 and 70. Scatter plot will contain dots between these values on y axis
    return payload;
};

$.addTimer("500ms",doTick);

function doTick(ctx) {
    $.output(generateData());
}
