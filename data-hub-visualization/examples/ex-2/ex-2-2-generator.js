getRandom = function(min, max) {
    return Math.random() * (max - min) + min;
};

getRandomInt = function(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};

generateData = function() {
    var payload = getRandom(50,70);     // Generate random number between 50 and 70
    return payload;
};

$.addTimer("500ms",doTick);             // Generate new data every 500ms

function doTick(ctx) {
    $.output(generateData());
}
