$(document).ready(function(){
    console.log("hey you");

    //Store a copy of the original
    var allDataOriginal = []
    var allData = [];
    var loadedData = 0;
    var dataPerPage = 6;
    var isLoading = false;
    var loadTriggred = true;
    var currentUrl = '/products/';
    var minPrice = null;
    var maxPrice = null;

 

    //Function to load data from the API with filters and search
    function loadDataFromApi(){
        $.ajax({
            url:currentUrl,
            type:'GET',
            data:{
                min_price:minPrice,
                max_price:maxPrice,
                search:$('#searchInput').val(),
            },

            success: function(data){
                allDataOriginal = data;
                allData = data;
                loadedData = 0;
                $('#content-list').empty();
                loadData();
                console.log(allDataOriginal);
            }

        });
    }






    function loadData() {
        if (isLoading || !loadTriggred){
            return;
        }

        isLoading = true;

       


        //Loop through the next set of products and them to the list
        for(var i=0; i<nextData.length; i++){
            //Create a bootstrap card for each product
            var dataCard = $('<div>').addClass('col-md-4 mb-4');
            dataCard.append('<div class="card">');
            
            //Create an image element and set its source to product's image URL
            if(nextData[i].image){
                var image = $('<img>').addClass('card-img-top').attr('src',''+nextData[i].image);

            }else {
                
                
                 var image = $('<img>').addClass('card-img-top').attr('src',imageSrc);
            }

            // console.log(imageSrc);
           
            var dataId = nextData[i].id;
            // console.log(typeof dataId);

            if(currentUrl === '/products/'){
                var dataUrl = "product/1/"

            }else {
                var dataUrl = "service/1/"
            }
            
            dataUrl = dataUrl.replace('1',dataId);
            //console.log(dataUrl);
            var detailsLink = $('<a>').attr('href', dataUrl).addClass('btn btn-primary').text('Details');
            //console.log(detailsLink);

            
            //Create a card body
            var cardBody = $('<div>').addClass('card-body');
            cardBody.append('<h5 class="card-title">'+nextData[i].item_name+'</h5>');
            cardBody.append(detailsLink);

            
            //Append the image and card body to the card
            dataCard.append(image);
            dataCard.append(cardBody);

            //Append the productcard to the list 
            $('#content-list').append(dataCard);
            loadedData++;

        }
        // loadedData += nextData.length;

        

        //Hide loading message if no more products
        if(loadedData >= allData.length){
            $('#loading-message').text("No more products to load");
        } else {
            $("#loading-message").text("loading");
        }

        isLoading = false;
        loadTriggred = false;

        //     // Add filters for price range
        // $('#content-list').before('<div class="row mb-3"><div class="col-md-6"><label for="minPriceInput">Min Price:</label><input type="number" class="form-control" id="minPriceInput" placeholder="Min Price"></div><div class="col-md-6"><label for="maxPriceInput">Max Price:</label><input type="number" class="form-control" id="maxPriceInput" placeholder="Max Price"></div></div>');

        // // Add reset button for filters
        // $('#content-list').before('<button class="btn btn-secondary" id="resetFiltersButton">Reset Filters</button>');



    }

   
    function switchUrl(){
        if(currentUrl === '/products/'){
            currentUrl = '/services/';
        }
        else {
            currentUrl = '/products/';
        }

        //Reset loaded data
        loadedData = 0;

        //Clear contetn list
        $('#content-list').empty();

        //Trigger data loading
        loadTriggred = true;

        loadDataFromApi(currentUrl);
        //Update button text
        updateButtonText();

    }

    

    function updateButtonText(){
        var buttonText = currentUrl === '/products/' ? 'Switch to Services': 'Switch to Products';
        $('#toggleButton').text(buttonText);

    }

    
    

    loadDataFromApi();

    //Load more products as the user scrolls down
    $(window).scroll(function () {
        if($(window).scrollTop() + $(window).height() >= $(document).height() - 200 && !isLoading) {
            loadTriggred = true;
            setTimeout(loadData,2000);
        }
    });

    //Add click event for the toggle button
    $('#toggleButton').click(function (){
        switchUrl();
    });

   
   


})