


//init fn
$(function() {

    $('.submit').click(function() {
        $(this).closest('form').submit();
        return false;
    });

    $('.point').each(function(i,e) {
        var $e = $(e);
        $e.css("bottom",$e.data("bottom"));
        $e.css("left",$e.data("left"));
    });

    $(".input").hover(function() {
        var $this = $(this);
        var $check = $this.find(".checkbox");
        var $actions = $this.find(".actions");
        $actions.show();
        var attr = $check.data("attr");
        var value = $check.data("value");
        $(".point[data-" + attr + "='" + value + "']")
            .css("background-color","yellow")
            .css("z-index",1);
    },
    function() {
        var $this = $(this);
        var $check = $this.find(".checkbox");
        var $actions = $this.find(".actions");
        $actions.hide();
        var attr = $check.data("attr");
        var value = $check.data("value");
        $(".point[data-" + attr + "='" + value + "']")
        .css("background-color","black")
        .css("z-index",0);;
    });

    $(".link.more").click(function() {
        $(this).nextAll().show();
        $(this).removeClass("more").addClass("less");
        $(this).text("less");

    })

//    $canvas = $('canvas#graphCanvas');

//    alert(data);

//    graph($canvas,
//          data,
//          10000,70,92,8);

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