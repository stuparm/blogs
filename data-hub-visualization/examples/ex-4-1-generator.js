getRandom = function(min, max) {
    return Math.random() * (max - min) + min;
};

getRandomInt = function(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};

generateData = function() {
    var payload = getRandom(10,70)+","+getRandom(80,90);    // Generate csv formatted string: float,float. Values showed from this generator will be visible from 10 to 70 on x axis and from 30 to 90 on y axis
    return payload;
};

$.addTimer("500ms",doTick);         // Generate new data every 500ms

function doTick(ctx) {
    $.output(generateData());
}
