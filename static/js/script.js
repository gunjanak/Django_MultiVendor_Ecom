$(document).ready(function(){
    console.log("hey you");
    // Store a copy of the original data
    var allDataOriginal = [];
    var allData = [];
    var loadedData = 0;
    var dataPerPage = 6;
    var isLoading = false;
    var loadTriggred = true;
    var currentUrl = '/products/';

    var minPrice = null;
    var maxPrice = null;

    //Function to update price range filters values
    function updatePriceRangeFilter(){
        console.log("calling updatePriceRangeFilter");
        minPrice = parseFloat($('#minPriceInput').val()) || null;
        maxPrice = parseFloat($('#maxPriceInput').val()) || null;

        //Trigger data loading with updated filter values
        loadedData = 0;
        $('#content-list').empty();
        loadTriggred = true;
        loadData();

    }

    //Function to reset price range filters
    function resetPriceRangeFilters(){
        $('#minPriceInput').val('');
        $('#maxPriceInput').val('');
        updatePriceRangeFilter();
    }

    //Add event listeners for price range inputs
    $('#minPriceInput,#maxPriceInput').on('input',updatePriceRangeFilter);

    //Add event listener for reset button
    $('#resetFiltersButton').click(function(){
        resetPriceRangeFilters();

    });

    function loadDataFromUrl(url){
        //simulate getting all products from Django backend and storing them in allProducts array
        $.ajax({
            url:currentUrl,
            type:'GET',
            success:function(data){
                allDataOriginal = data;
                allData = data;
                console.log(allData);
                loadData();
            }
        });
    }


    function loadData() {
        if (isLoading || !loadTriggred){
            return;
        }

        isLoading = true;

         //Filter data based on price range
         allData = allDataOriginal.filter(function(item) {
            if(minPrice !== null && item.price < minPrice){
                return false;
            }
            if (maxPrice !== null && item.price > maxPrice){
                return false;
            }
            return true;
        });

        //Get the next set of products based on the current offset
        var nextData = allData.slice(loadedData,loadedData+dataPerPage);
        // console.log("***inside loadData function ****");
        // console.log(loadedData);
        // console.log(nextData);

       


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
            console.log(dataUrl);
            var detailsLink = $('<a>').attr('href', dataUrl).addClass('btn btn-primary').text('Details');
            console.log(detailsLink);

            
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

        loadDataFromUrl(currentUrl);
        //Update button text
        updateButtonText();

    }

    

    function updateButtonText(){
        var buttonText = currentUrl === '/products/' ? 'Switch to Services': 'Switch to Products';
        $('#toggleButton').text(buttonText);

    }

    function performSearch(searchQuery){
        // console.log("**********at search query ***************");
        // console.log(searchQuery);
        //Filter the data based on the search query
        var filterData = allDataOriginal.filter(function (item) {
            //Customize this condition based on your data structure and search criteria
            return item.item_name.toLowerCase().includes(searchQuery.toLowerCase());


        });
        //Reset loaded data
        loadedData = 0;
         //Clear content list
         $('#content-list').empty();

         //Update allData with filtered data
        //  console.log("***********filterData************");
        //  console.log(filterData);
         allData = filterData;

         //trigger data loading
         loadTriggred = true;
          loadData();
    }
    

    loadDataFromUrl(currentUrl);

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

    //Add click event for the search button
    $('#searchButton').click(function(){
        var searchQuery = $('#searchInput').val();
        performSearch(searchQuery);

    });

    // Add keypress event for the search input
    $('#searchInput').on('keypress',function (e) {
        // console.log("enter pressed")
        if (e.which === 13) {
            // 13 is the key code for Enter
            var searchQuery = $('#searchInput').val();
            // console.log(searchQuery);
            performSearch(searchQuery);
            return false;
        }
    });


});