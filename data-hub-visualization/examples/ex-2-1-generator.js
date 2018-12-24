getRandom = function(min, max) {
    return Math.random() * (max - min) + min;
};

getRandomInt = function(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};

generateData = function() {
    var payload = getRandom(20,60);     // Random value between 20 and 60 
    return payload;
};

$.addTimer("500ms",doTick);             // Generate random value every 500ms

function doTick(ctx) {
    $.output(generateData());
}
