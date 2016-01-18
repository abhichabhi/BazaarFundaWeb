var start = 0
jQuery(document).ready(function($){ 
	current_URl =  window.location.href
	current_URl = current_URl.replace('browse','listing')
	loadFirstData(current_URl) 
	});

function loadFirstData(current_URl) {	
	$.ajax({url:current_URl ,
      dataType: 'json',
      success: function(data, status) {
      		window.start = data.start + 20
      		listing_div = ".small_with_description"
            html_str = createListingHTMLWithJSON(data.productList, data.category)
            jQuery(listing_div).html(html_str)
          },          
        });
}

$(document).on("click", ".listingLoadProducts", function() {
    current_URl =  window.location.href
	current_URl = current_URl.replace('browse','listing')
	if (current_URl.indexOf('?') > -1)
		current_URl = current_URl + "&start=" + String(window.start)
	else
		current_URl = current_URl + "?start=" + String(window.start)
	listingLoadProducts(current_URl) 
});

function listingLoadProducts(url) {
	$.ajax({url:current_URl ,
      dataType: 'json',
      success: function(data, status) {
      		window.start = data.start + 20
      		listing_div = ".small_with_description"
            html_str = createListingHTMLWithJSON(data.productList, data.category)
            jQuery(listing_div).html(html_str)
          },          
        });
}

function createListingHTMLWithJSON(productList, category, rank=0) {
	html_str = ''
	for (iter = 0; iter < productList.length; iter++) { 
		product = productList[iter]
		if (typeof product.master != 'undefined') {
			rank ++;
			product_id = product.master.product_id
			product_name = product.master.product_name
			product_url = product.master.productUrl
			priceList = product.priceList.priceList
			//Compare Prices Pop-Up
			html_str += '<!-- {#Compare Prices PoUp #} -->'
			html_str += '<div class="modal fade price" id="compare_price_' + product_id + '">'
			html_str += '<div class="modal-dialog">'
			html_str += '<div class="modal-content">'
			html_str += '<div class="modal-header">'
			html_str += '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>'
			html_str += '<h4 class="modal-title"><center>Compare Prices for ' + product_name.substring(0,20) + '...</center></h4>'
			html_str += '</div>'
			html_str += '<div class="modal-body">'
			html_str += '<table class="table">'
			html_str += '<colgroup>'
			html_str += '<col class="colfixw25"><col class="colfixw25"><col class="colfixw20"><col class="colfixw10"><col class="colfixw20"></colgroup>'
			html_str += '<thead>'
			html_str += '<tr>'
			html_str += '<td scope="col" class="aligncenter backgrey font_table_fix">Seller</td>'
			html_str += '<td scope="col" class="aligncenter backgrey font_table_fix">Discount</td><td scope="col" class="aligncenter backgrey font_table_fix">Price</td><td scope="col" class="aligncenter backgrey font_table_fix">Buy Option</td></tr></thead><tbody>'
			for (price_itr =0; price_itr < priceList.length; price_itr++ ) {
				if (priceList[price_itr].price != 0) {
					html_str += '<tr>'
					html_str += '<td class="aligncenter 0_margin"><img src="https://s3-ap-southeast-1.amazonaws.com/bazaarfunda/Website/static/logo/' + priceList[price_itr].website + '.jpg"  alt="filpkart" height="25px" width="100px"></td>'
					html_str += '<td class="aligncenter 0_margin"><h5>' + priceList[price_itr].discount + ' %</h5></td>'
					html_str += '<td class="aligncenter 0_margin"><h5>' + priceList[price_itr].price + '</h5></td>'
					html_str += '<td class="aligncenter 0_margin"><a href=' + priceList[price_itr].productUrl + ' target="_blank" class="btn btn-mini">BUY</a></td>'
					html_str += '</tr>'
				}
			}
			html_str += '</tbody></table></div>'
			html_str += '<!--{# Price Alert #}-->'
			html_str += '<h3 class="register-title">Set Price Alert</h3>'
			html_str += '<form class="register" onsubmit="emailMeWhenAvailable(&#39;' + product_id + '&#39;);">'
			html_str += '<input type="text" class="register-input" placeholder="Your Desired Price" id= "' + product_id + '"_price >'
			html_str += '<input type="email" class="register-input" placeholder="Your Email Address" id= "' + product_id + '_email">'
			html_str += '<input type="submit" value="Submit" class="register-button">'
			html_str += '</form>'
			html_str += '<div id="submitsuccess_' + product_id + '">'
			html_str += '</div>'
			html_str += '{# Price Alert #}'
			html_str += ' </div> </div> </div>'
			html_str += '<!-- {# Compare Prices #} -->'
			//Compare Prices Pop-Up

			html_str += '<div class="span2 product hover carousel_item">'
			html_str += '<div class="label_new_top_left">Rank:' + rank + '</div>'
			html_str += '<div class="product-image-wrapper listing ' + category + '" >'
			html_str += '<a href="/pdp/' + product_id + '" >'
			html_str += '<img src="https://s3-ap-southeast-1.amazonaws.com/bazaarfunda/Website/static/ProductImage/' + product_id + '.jpg">'
			html_str += '</a></div>'

			html_str += '<div class="wrapper-hover"><div class="product-name aligncenter" style="height:33px"><a href="/pdp/' + product_id + '">' + product_name.substring(0,20) + '...</a></div>'
			html_str += '<div class="wrapper"><span class="sort-rating hidden">4</span><div class="product-price aligncenter" style = "padding-bottom:10px">';
			if (product.min_priceDict['price'] == 0 || typeof product.min_priceDict === "undefined") {
				html_str += '<a class="aligncenter price-not-available"  href="#">"Price Not Available"</a>'
			}
			else {
				html_str += '<a class="aligncenter price-available"  href="' + product_url + '">₹&nbsp ' + product.min_priceDict.price + '</a>'
			}
			html_str += '</div> </div>'
			html_str += '<div class="skillbar clearfix " data-percent=' + product.finalrating + '%>'
			html_str += '<div class="skillbar-title" style=" width:' + product.finalrating + '%;"><span style="color: #FFFFFF">' + product.finalrating + '</span></div>'
			html_str += '<div class="skillbar-bar" style="background: #8b9dc3;"></div>'
			html_str += '<div class="skill-bar-percent"></div></div>'
			html_str += '<div class="add-to-links">'
			html_str += '<ul>'
			html_str += '<li style = "padding-bottom:10px;"><a href="#compare_price_all" class="small_icon_color" data-toggle="modal"><i class="icon-shop"></i></a><a class="small_icon_color" data-toggle="modal" onclick="location.href=#;" href="#compare_price_' + product_id + '">Compare Prices</a></li>'
			html_str += '<li> <a href="#" class="small_icon_color" onclick="addToCompare(&#39;' + product_id + '&#39;);"><i class="icon-chart-bar"></i>Add to Compare</a> </li>'
			html_str += '</ul>'
			html_str += '</div>'
			html_str += '</div>'
			html_str += '</div>'
			}
	}
	return html_str
}

