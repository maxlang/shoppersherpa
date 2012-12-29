
var filters = {};


//init fn
$(function() {


    $(".point").click(function() {

        $this = $(this);
        $("#product-info").load("/product",{"id":$this.data("id")},function() {
            $(".close").click(function() {
                $(this).parent().hide();
            });
        });


         //$.post('/tracker/add', trackerData, 'json').success(function () {
        //$.post('/product',{},'html').success(function () {

        //});
    });

    //TODO: when you hover over a point, highlight the relevant attributes in the side bar
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


    function prepareAttributeBar() {

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


        function deselect() {
            $checkbox = $(this).closest(".input").find(".checkbox");
            //apply filters
            addExclusionFilter($checkbox.data("attr"), $checkbox.data("value"));
            //reload the attributes
            var filterdata = [];
            for(attr in filters) {
                filterdata.push(filters[attr]);
            }

            var data = {"keywords":$("input[name='keywords']").val(), "attributes":["size"],
                 "filters":filterdata};

            var attr = $checkbox.data("attr");
            var value = $checkbox.data("value");
            $(".point[data-" + attr + "='" + value + "']").hide();

            $("#attributeTabs").load("/attributes", {"query":JSON.stringify(data)},prepareAttributeBar);



        }

        function select() {
            //apply filters
            addInclusionFilter($this.data("attr"), $this.data("value"));
            //reload the attributes

        }

        function only() {
            //apply filters
            addOnlyFilter($this.data("attr"), $this.data("value"));
            //reload the attributes

        }


        $(".deselect").click(deselect);

    };

    prepareAttributeBar();

});

//create filters
function addInclusionFilter(attribute, value) {
    if (attribute in filters) {
        if(filters[attribute]["type"]==="include") {
            filters[attribute]["value"].push(value);
        } else if (filters[attribute]["type"]==="exclude") {
            var idx;
            while((idx = filters[attribute]["value"].indexOf(value)) > -1) {
                filters[attribute]["value"].splice(idx,1);
            }
        }
    } else {
        // it's already included
        console.log("unexpected option");
    }
}

function addOnlyFilter(attribute, value) {
    filters[attribute] = {"attribute":attribute,"type":"include","value":[value]};
}

function addExclusionFilter(attribute, value) {
    if (attribute in filters) {
        if(filters[attribute]["type"]==="exclude") {
            filters[attribute]["value"].push(value);
        } else if (filters[attribute]["type"]==="include") {
            var idx;
            while((idx = filters[attribute]["value"].indexOf(value)) > -1) {
                filters[attribute]["value"].splice(idx,1);
            }
        }
    } else {
        filters[attribute] = {"attribute":attribute,"type":"exclude","value":[value]};
    }
}
