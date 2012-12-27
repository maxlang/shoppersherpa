


//init fn
$(function() {

    var filters = [];

    $('.submit').click(function() {
        $(this).closest('form').submit();
        return false;
    });

    $(".input").hover(function() {
        var $this = $(this);
        var $check = $this.find(".checkbox");
        var $actions = $this.find(".actions");
        $actions.show();
        var attr = $check.data("attr");
        var value = $check.data("value");
        $(".point[data-" + attr + "='" + value + "']")
            .css("background-color","#919191")
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

    function more() {
        $(this).nextAll().show();
        $(this).removeClass("more").addClass("less");
        $(this).text("Less");
        $(this).click(less);
    }

    function less() {
        $(this).nextAll().hide();
        $(this).removeClass("less").addClass("more");
        $(this).text("More");
        $(this).click(more);
    }

    $(".link.more").click(more);

    $(".point").hover(function() {
        $this = $(this);
        var size = $this.data("size_class");
        var price = $this.data("price");
        var priceperinch = price/size;
        $this.css("background-color","#919191");
        $("#point-info").html(size+"\"" + " at $" + Math.round(priceperinch,2) + "/inch, " + "total $" + price);
    },
    function() {
        $this = $(this);
        $this.css("background-color","black");
        $("#point-info").html("");
    });

 //$.post('/tracker/add', trackerData, 'json').success(function () {

    $(".point").click(function() {

        $this = $(this);
        $("#product-info").load("/product",{"id":$this.data("id")},function() {
            $(".close").click(function() {
                $(this).parent().hide();
            });
        });
        //$.post('/product',{},'html').success(function () {

        //});
    });

    $(".deselect").click(function() {
        //grey out and switch to a "select" button

        //move to the bottom of the list

        //pull up another filter from below the fold

        //

    });

});


//view product info
function viewProduct() {


}

//view point info
function pointInfo() {


}