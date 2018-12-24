getRandom = function(min, max) {
    return Math.random() * (max - min) + min;
};

getRandomInt = function(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};

generateData = function() {
    var payload = getRandom(20,40); // random number between 20 and 40
    return payload;
};

$.addTimer("500ms",doTick);         //send new random number every 500ms

function doTick(ctx) {
    $.output(generateData());
}
