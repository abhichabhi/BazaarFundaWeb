
var product_map ={}
jQuery(document).ready(function($){  
  // $(".product-image-wrapper").css({'max-height':'80px','color':'red'});
   $("img").error(function(){
        $(this).attr('src', 'https://s3-ap-southeast-1.amazonaws.com/bazaarfunda/Website/static/ProductImage/No-Image-Available.jpg');
    });

	/*ComparePrices PopUp*/
	$("#compare_price").on("show", function () {
      $("body").addClass("modal-open");
    }).on("hidden", function () {
      $("body").removeClass("modal-open")
    });

    /*ComparePrices PopUp*/

     var category = $('#category').attr('data-name'); 
      if (category == 'None') { 
                bind_Category();
      }
      else {
        loadBrands();
      }

      $(".checkbox").click(function() {
        console.log("checked");
      });

	});


// Choose Product From Compare Page
  $('#chooseproduct').click(function(){
    model = $("#the_model").val()   
    $productID = product_map[model];
    addToCompare($productID)

  }); 
          
$(function() {
    $('#filter_search_3').fastLiveFilter('#filter_model');
    
    });

//------------ Bottom Compare List PopUp
$(document).scroll(function() {

  var y = $(this).scrollTop();
  if (y > 520) {
    $('.bottomMenu').animate({
                    'top': -10
                },  10, 'linear');
  } else {
    //$('.bottomMenu').fadeOut();
    $('.bottomMenu').animate({
                    'top': -400
                }, 10, 'linear');
  }
});

//------------ Bottom Compare List PopUp

// Easy AutoComplete
var category = $('#category').attr('data-name');
if (category == "") {
  console.log(category);
  category = "all";
}

var options = {
  url: function(phrase) {
    return "/product-search?category=" + category + "&qu=" + phrase
  },
    list: {
      onClickEvent: function() {
      search();
    },
    match: {
      enabled: true
    }
  },

  getValue: "name",

  template: {
    type: "iconRight",
    fields: {
      iconSrc: "icon"
    }
  },

};

var main_search_options = {
  
  url: function(phrase) {
    return "/product-search?category=" + category + "&qu=" + phrase
  },
  requestDelay: 1000,
  cssClasses: "main_search",
    list: {
      onClickEvent: function() {
      search();
    },
    match: {
      enabled: true
    }
  },

  getValue: "name",

  template: {
    type: "iconRight",
    fields: {
      iconSrc: "icon"
    }
  },

};
$("#form-search-spy-text").easyAutocomplete(options);

$("#allProductSearch").easyAutocomplete(main_search_options);


function bind_Category() {
  var category_options = {
    url: "/restfull/categories",
    cssClasses: "category",
    list: {
      onClickEvent: function() {
        category_value = $("#the_category").val()
        // $('#the_brand').attr('value');
    loadBrands();
     }    
    }   

  };
  $("#the_category").easyAutocomplete(category_options);
  $(".easy-autocomplete").css({"width":"100%"});
  $(".category .easy-autocomplete-container ul").css({"top":"-10px"});
}


function loadBrands() {
  category = $("#the_category").val()
  if (!category) {
    category = $('#category').attr('data-name');
  }
  domain = location.host
  theUrl = "http://" + domain + "/restfull/brands/" + category
  
  brandJson = httpGet(theUrl)
  var brand_jsonData = JSON.parse(brandJson);
  $('#the_brand').autocomplete({
                source: brand_jsonData,
                minLength: 0,
                scroll: true

            }).focus(function() {
                $(this).autocomplete("search", "");
            });
}

function loadModels(category, brand) {
  category = $("#the_category").val()
  if (!category) {
    category = $('#category').attr('data-name');
  }
  brand = $("#the_brand").val()
  domain = location.host
  theUrl = "http://" + domain + "/restfull/products/" + category + "/" + brand
  
  productJson = httpGet(theUrl)
  product_list = []
  product_map = JSON.parse(productJson);
  for (var key in product_map) {
  if (product_map.hasOwnProperty(key)) {
    product_list.push(key);
  }
  }
  $('#the_model').autocomplete({
                source: product_list,
                minLength: 0,
                scroll: true

            }).focus(function() {
                $(this).autocomplete("search", "");
            });
}

/*
Compare Page Auto Completes
*/

//Cart Box Display
function cartMouseHover() {
  
  $(".shopping_cart_mini").css({'display':'block'});
}
function cartMouseOut() {
  
  $(".shopping_cart_mini").css({'display':'None'});
}
function coupleCompare(id1,id2) {
  $domain = location.host
  $removeAll = "http://" + $domain + "/cart/clear"
  $addUrl =  "http://" + $domain + "/cart/add/";
  $compareURL = "http://" +  $domain +  "/compare";
  httpGet($removeAll);
  httpGet($addUrl + id1);
  httpGet($addUrl + id2);

  window.location = $compareURL

}

function addToCompare(productId) {
  console.log(productId)

  $domain = location.host
  $url =  "http://" + $domain + "/cart/add/" + productId;
  $compareURL = "http://" +  $domain +  "/compare";

  
  $.ajax({url:$url ,
  dataType: 'json',
  success: function(data, status){
    console.log(data)
      if (data.status == 200) {
          $( "span.badge" ).empty();
          $( "span.badge" ).append(data.productId.length);
        location.href = $compareURL;
      }

      else if (data.status == 256) {
        $( "span.badge" ).empty();
        $( "span.badge" ).append(data.productId.length);
        location.href = $compareURL;
      }

      else if (data.status == 512) {
          $("div.alert").css("display", "");
      }

  },
});
  console.log(productId)
}

function filterOptions(inputElement) {
  urlParams = getURLParameters()
  if (urlParams['start'] != undefined) {
    delete urlParams['start']
  }
  if (urlParams['reco'] != undefined) {
    delete urlParams['reco']
  }  
  newFilterName = inputElement.getAttribute('name') 
  console.log(urlParams)
  if (newFilterName == "price") {
    newFilterValue = [inputElement.getAttribute('valuei').toString() + '_' + inputElement.getAttribute('valuej').toString()]  
    console.log(newFilterValue)
  }
  else {
    newFilterValue = [inputElement.getAttribute('value')]
  }

  if (urlParams[newFilterName]) {
    var index = urlParams[newFilterName].indexOf(newFilterValue[0]);
    if (index > -1) {
      urlParams[newFilterName] = removeElemetFromList(newFilterValue[0], urlParams[newFilterName])
      if (urlParams[newFilterName].length == 0) {
        delete urlParams[newFilterName]
      }
    }
    else {
      urlParams[newFilterName].push.apply(urlParams[newFilterName], newFilterValue)
    }
  }
  else {
    urlParams[newFilterName] = newFilterValue
  }

  listingURl = window.location.pathname + '?' + makeURLFromParameters(urlParams)  
  window.location = listingURl
}
/* Listing filter*/
/*Listing Load More*/
function listingLoadMore(start) {
  urlParams = getURLParameters()
  urlParams['start'] = start + 20 
  newSearchURL = window.location.pathname + '?' + makeURLFromParameters(urlParams)
  console.log(newSearchURL)
  window.location = newSearchURL
}
/*Listing Load More*/

function httpGet(path) {
  var host = window.location.origin
  theUrl = host + path
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", theUrl, false );
  xmlHttp.send( null );
  console.log(xmlHttp.responseText)
  return xmlHttp.responseText;
}

function removeElemetFromList(element, List) {
  var index = List.indexOf(element);
      if (index > -1) {
        List.splice(index, 1);
      }
  return List
}

function getURLParameters() {
  var urlParams;
    (window.onpopstate = function () {
        var match,
            pl     = /\+/g,  // Regex for replacing addition symbol with a space
            search = /([^&=]+)=?([^&]*)/g,
            decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
            query  = window.location.search.substring(1);
        urlParams = {};
        while (match = search.exec(query))
           urlParams[decode(match[1])] = decode(match[2]);
    })();
    for (params in urlParams) {
      value = urlParams[params].split(",")
      urlParams[params] = value         
    }
    return urlParams;
}

function makeURLFromParameters(obj) {
  var str = [];
  console.log(obj)
  for(var p in obj)
    if (obj.hasOwnProperty(p)) {
      str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
    }
  return str.join("&");
}

function searchFilter(category, start) {
  urlParams = getURLParameters()
  if (category != '' && start == 0) {
    urlParams['category'] = category
    delete urlParams.start
  }
  if (start != 0 && category == '') {
    urlParams['start'] = start
  }
  newSearchURL = window.location.pathname + '?' + makeURLFromParameters(urlParams)
  console.log(newSearchURL)
  window.location = newSearchURL
}

function search() {
  formObj = document.getElementById('form-search-spy-text')
  searchText = formObj.value
  if (searchText == 'search entire store...') {
    formObj = document.getElementById('allProductSearch')
  }
  
  newSearchURL = '/search?q=' + formObj.value
  window.location = newSearchURL
}

function remove_product_from_compare(theLink, id) {
    var data=theLink.className.split(' ')[0];
    // console.log(data);
    //var data = ev.dataTransfer.getData("text");
    //ev.target.appendChild(document.getElementById(data));
      //document.getElementById("demo").innerHTML = res;
      removeByClass(data);
      var last = data.slice(-1);
      var str ="hide";
      var res = str.concat(last);
      $("."+res).show();
      $currentURL = window.location.href;
      $currentURL = $currentURL.replace("#","");
      $currentURL = $currentURL + "/";
      $path = window.location.pathname + "/";
      $removeURL = $currentURL.replace($path, "/cart/remove/" + id);
      console.log($removeURL)
      $("#item_" + id).remove()
      $.ajax({url:$removeURL ,
      dataType: 'json',
      success: function(data, status){
              if (data.status == 200) {
                $( "span.badge" ).empty();
                $( "span.badge" ).append(data.productId.length);                
              }
              else if (data.status == 512) {
                $("div.alert").css("display", "");
              }

          },
          
        });
} 

function removeByClass(className) {
   $("."+className).remove();
}

function httpGet(theUrl)
        {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", theUrl, false );
            xmlHttp.send( null );
            return xmlHttp.responseText;
        }


//Email me when Available

function emailMeWhenAvailable(id) { 
  //http://127.0.0.1:8080/users/subscribePrice?email=dude.abhi.chat@gmail.com&productName=productName&productId=productId&priceCutOff=priceCutOff
  console.log('emailMeWhenAvailable');
  productId = id;
  priceId = id + "_price"
  emailId = id + "_email"
  priceCutOff = $('#' + priceId)[0].value
  email = $('#' + emailId)[0].value
  console.log(priceCutOff, email)
  // emaiReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  // priceReg = /^[0-9]*$/;
  subscribeURL = "/users/subscribePrice?" + "email=" + email + "&productId=" + id + "&priceCutOff=" + priceCutOff
  subscribeURL = window.location.origin + subscribeURL
  
  jQuery.ajax({
         url: subscribeURL,
         success: function(result) {
                      if (result == false) {
                        console.log("**We already have this request from you.")
                        $("#submitsuccess_" + productId).text("**We already have this request from you. You can place numerous price alerts.").css({"display":"block", "font-size":"150%","color":"#610B0B"})
                        return false;
                      }
                      else {
                        console.log("**We don't have this request from you")
                        $("#submitsuccess_" + productId).text("**Allright!! You will hear from us. You can place numerous price alerts.").css({"display":"block", "font-size":"150%","color":"#610B0B"})
                        return true;
                      }
                  },
         async:   false
    });  
   $("#compare_price_" + productId).hide();
// $("#submitsuccess").textContent.replace("**Allright You will hear from us").css({"display":"block", "font-size":"50%","color":"#610B0B"})
  return true;
}
//Email me when Available    