getRandom = function(min, max) {
    return Math.random() * (max - min) + min;
};

getRandomInt = function(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};

generateData = function() {
    var payload = getRandom(20,30)+","+getRandom(30,60); //  Generate csv formatted string: float,float. Values showed from this generator will be visible from 20 to 30 on x axis and from 30 to 60 on y axis
    return payload;
};

$.addTimer("500ms",doTick);

function doTick(ctx) {
    $.output(generateData());
}
