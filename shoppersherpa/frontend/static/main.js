//init fn
$(function() {

    $('.submit').click(function() {
        $(this).closest('form').submit();
        return false;
    });

    $canvas = $('canvas#graphCanvas');

    alert(data);

    graph($canvas,
          data,
          10000,70,92,8);

});

/*
Point data is a list of points with size, price and id
*/
function graph($canvas, pointData,maxPrice,minPrice,maxSize,minSize) {
    var width = $canvas.width();
    var height = $canvas.height();

    $canvas[0].height = height;
    $canvas[0].width = width;

    $canvas.clearCanvas();

    var i;

    for(i=0;i<pointData.length;i++) {
        size = pointData[i].size_class;
        price = pointData[i].price;
        id = pointData[i].id;
        rating = pointData[i].ratings_avg;

        x = (size - minSize)/(maxSize-minSize) * width;
        y = (price - minPrice)/(maxPrice-minPrice) * height;

        $canvas.drawEllipse({
            x: x, y: y, width: 10, height: 10,
            fillStyle: "#000",
            fromCenter: true
        });
    }


}