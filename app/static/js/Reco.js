

//declaring global variable
var click=0;
var count=1;
var flag=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
var category;
var all_cat_detailJS = {}

//--end of declaration
//used in is_selected()
//jQuery('#the-element').click(function () { /* perform action here */ });

jQuery(document).ready(function($){ 
	$('.price_checkbox').click(function(){
		console.log("clicked");
	});
});

function reco_slider_next(thislink, catAppend)
{	
	var max=4;		
	if (catAppend) {
		var str= catAppend + "reco_slide_";	
	}			
	else {
		var str="reco_slide_";	
	}				//depend on no of slide
						//id name to concat
	//alert(thislink);	
	var name=thislink.id
						//the current children id
	//alert(name);
	var current=jQuery("#"+name).parent().attr("id");	//the parent div id
	
	//alert(current);
	var inr = current.slice(-1);				//getting id number (last)	
	if(inr == max)
		inr=1;									//boundary check maintaining cycle
	else
		inr = Number(inr)+1;					//increment by 1													
	var next = str.concat(inr);	
	console.log(next, "next");				//concat to get id of next div
	jQuery("#"+current).animate({left: '-1000px'},"slow").hide(50);	//animating sequences 1
	jQuery("#"+next).animate({left: '1000px'},"slow");				//2
	jQuery("#"+next).show(50).animate({left: '0px'},"slow");		//3
}

function reco_slider_prev(thislink, catAppend)
{

	var max=4;									//depend on no of slide
	if (catAppend) {
		var str= catAppend + "reco_slide_";	
	}			
	else {
		var str="reco_slide_";	
	}				//depend on no of slide				//id name to concat
	console.log(str, catAppend)
	//alert(thislink);	
	var name=thislink.id						//the current children id
	//alert(name);
	var current=jQuery("#"+name).parent().attr("id");	//the current id
	//alert(current);
	var inr = current.slice(-1);				//getting id number
	if(inr==1)
		inr=max;								//boundary maintaining cycle
	else
		inr = Number(inr)-1;					//decrement by 1
		
	var next = str.concat(inr);					//concat to get id of next div
	jQuery("#"+current).animate({left: '1000px'},"slow").hide(50);	//animating sequences 1
	jQuery("#"+next).animate({left: '-1000px'},"slow");				//2
	jQuery("#"+next).show(50).animate({left: '0px'},"slow");		//3
}


function is_selected(thislink)
{	
	console.log("in is_selected")
	var max=5;
	var str_class="show";
	var str_id="mob_key_"
	var add_class;
	var remove_class;
	var id;
	var current = thislink.id;
	var inr = current.slice(-2);
	var index=Number(inr);
	console.log(current, inr, index, flag[index], count)
	
	if(flag[index]==0 && count<=max)
	{
		// console.log('in is selected1')
		flag[index]=count;
		//alert(flag[index]);
		//alert(count);
		if(index>=10){
			id=str_id.concat(index);
		}
			
		else
		{
			id=str_id.concat("0");
			id=id.concat(index);
		}
		
		add_class=str_class.concat(count);
		// console.log(add_class, id)
		jQuery("#"+id).addClass(add_class);
		count++;	
		
	}

	else if(flag[index]!=0)
	{
		// console.log('in is selected2')
		if(index>=10)
			id=str_id.concat(index);
		else
		{
			id=str_id.concat("0");
			id=id.concat(index);
		}
		
		remove_class=str_class.concat(flag[index]);
		jQuery("#"+id).removeClass(remove_class);
		
		var temp=flag[index];
		flag[index]=0;
		for(i=1;i<=40;i++)
		{
			if(flag[i]>temp)
			{
				remove_class=str_class.concat(flag[i]);
				if(i>=10)
					id=str_id.concat(i);
				else
				{
					id=str_id.concat("0");
					id=id.concat(i);
				}
					
				jQuery("#"+id).removeClass(remove_class);
				flag[i]--;
				add_class=str_class.concat(flag[i]);
				jQuery("#"+id).addClass(add_class);
			}			
		}
		//alert(flag[index]);
		count--;
		//alert(count);
	}
	else {
		alert("Max Preference Selected")
	}
}

function start_recommendationSlider(category, thisLink,catAppend) {
	if (category == 'all' ) {
		category = catAppend
	}
	// console.log("In reco Slider", category, catAppend)
	window.category = category
	reco_slider_next(thisLink, catAppend);
	path = '/restfull/categorydetails'
	all_cat_detailJS = jQuery.parseJSON(httpGet(path));
	all_key_details = all_cat_detailJS[category]['allKeyWordsIcon']
	window.all_cat_detailJS = all_cat_detailJS
	reco_slider_str = '#' + catAppend + 'reco_slide_3'
	// console.log(reco_slider_str, "in start_recommendationSlider")
	catr_str_reco = category
	if (category.slice(-1) === 's') { 
		catr_str_reco = category.slice(0, -1);
	}

	jQuery(reco_slider_str).html('<h1>My New ' + ((category.slice(-1) === 's') ? catr_str_reco = category.slice(0, -1) : category ) + ' is for</h1><h5>Just click according to your priorities with a maximum of 5 Top most priority should be clicked 1st</h5>');
	iter_val = 1
	for (var kye_iter in all_key_details) {

		jQuery(reco_slider_str).append('<div data = "' + kye_iter + '" id="mob_key_' +  ("0" + iter_val.toString()).slice(-2) + '" class="pop_box" onclick="is_selected(this)"><i class="fa ' + all_key_details[kye_iter] + ' fa-5x "></i><div class="product-name aligncenter" style="height:33px">' + kye_iter + '</div></div>&nbsp;&nbsp;');
	iter_val ++;
		} 
	jQuery(reco_slider_str).append("<br><span id='slide_3_back' class='btn back' onclick='reco_slider_prev(this, &#39;" + catAppend + "&#39;)'>BACK</span>");
	jQuery(reco_slider_str).append("<span id='reco_pref_done' class= 'btn forward' onclick='Done(this, &#39;" + catAppend + "&#39;);'>DONE</span>");
                    
}

function Done(thisLink, catAppend) {
				//alert(thislink.id);
	reco_slider_next(thisLink, catAppend);		
	var i;				
	// console.log(catAppend)
	theUrl = "/restfull/brands/" + category
	var reco_4_str = '#reco_slide_4'
  	if (catAppend) {
  		reco_4_str = '#' + catAppend + 'reco_slide_4'
  	}
  	// console.log(reco_4_str)
	brandJson = httpGet(theUrl)
	var brand_jsonData = JSON.parse(brandJson);
    //now json variable contains data in json format
    //let's display a few items
	var str='';
	str+='<h3>Choose if you Prefer a Price range or a specific Brand</h3>';
	var selectStr = 'Search by Brand'
	var blankStr = '';
	str+='<div clas="row"><div class="span4">';
	str+='<center><h5>Select Price Range</h5>';
	str+='<div class="inner-addon right-addon"><i class="glyphicon icon-search-2 icon-small"></i><input name="filter_search_price" type="text" id="filter_search_price" /></div>';
	str+='<div class="listing-height"><ul id="filter_price">';
	for (price = all_cat_detailJS[category]['priceRange'][0]; price <= all_cat_detailJS[category]['priceRange'][1];  price = price + all_cat_detailJS[category]['price_interval'] )
	{		
		str+=' <li ><input type="checkbox" onclick = "check_checkbox(this);" class="price_checkbox" id = "' + price + '" + valuei="'+price+'" + valuej="'+ (price +all_cat_detailJS[category]['price_interval']).toString() +'"   /><label for="' + price + '"> RS ' + price.toString() + " - Rs " + (price +all_cat_detailJS[category]['price_interval']).toString()  + '</label></li>';
	}
	str+='</ul></div></div></center></div>';
	str+='<div class="span4">';
	str+='<center><h5>Select Brand</h5>';
    str+='<div class="inner-addon right-addon"><i class="glyphicon icon-search-2 icon-small"></i><input name="filter_search_brand" type="text" id="filter_search_brand" /></div>';
	str+='<center><div class="listing-height"><ul id="filter_brand">';
	for(i=0;i<=brand_jsonData.length;i++)
	{
		str+=' <li><input onclick = "check_checkbox(this);" type="checkbox"  class="brand_checkbox" id = "' + brand_jsonData[i] + '" value="'+ brand_jsonData[i]+'" /><label for="' + brand_jsonData[i] + '"> '+brand_jsonData[i]+'</label></li>';	
	}
	str+='</ul></div></center></div></center></div></div>';
	str+="<br><span id='slide_4_back' class='btn back' onclick='reco_slider_prev(this, &#39;" + catAppend + "&#39;)''>BACK</span>";
	str+="<span id='recommend' class='btn forward' onclick='recommend()'>Recommend</span>";
	jQuery(reco_4_str).html(str);
	
	$('#filter_search_brand').fastLiveFilter('#filter_brand');
	$('#filter_search_price').fastLiveFilter('#filter_price');
	
	}


function check_checkbox(thisObj) {
	if ($(thisObj).attr('status') == 'checked') {
		$(thisObj).removeAttr('status');
	}
	else {
		$(thisObj).attr('status','checked');
	}
	
	// console.log("checkbox checked", thisObj);
}

function recommend()
{
	urlObj = {}
	urlObj['reco'] = 1
	priceRange = [];
	iter = 0;
	$('.price_checkbox').each(function(index) {
		if ( $( this ).attr('status') == 'checked') {
			priceRange.push(parseInt($( this ).attr('valuei')));
			priceRange.push(parseInt($( this ).attr('valuej')));
		}
		// console.log( index + ": " + $( this ).attr('valuei'), $( this ).attr('valuej'));
	});
	priceRange.sort()
	if (priceRange.length > 0) {
		priceRange = [priceRange[0], priceRange[priceRange.length -1]]	
	}
	
	// console.log(priceRange);
	
	var brandList = []
	$('.brand_checkbox').each(function(index) {
		if ( $( this ).attr('status') == 'checked') {
			brandList.push($( this ).attr('value'));			
		}
		// console.log( index + ": " + $( this ).attr('valuei'), $( this ).attr('valuej'));
	});

	// console.log(brandList);	
	keywordList = []
	for (iter = 0; iter<5; iter++) {
		pop_text = "pop_box.show" + (iter + 1).toString();
		if ($('.' + pop_text).attr('data')) {
			keywordList.push($('.' + pop_text).attr('data'));
		}		
	}

	if (brandList.length > 0) {
		
		urlObj['Brand'] = brandList
	}

	if (priceRange.length > 0) {
		
		urlObj['price'] = priceRange
	}

	if (keywordList.length > 0) { 
		weightList = []
		for(iter=1; iter <= keywordList.length; iter++) {
			weightList.push(iter)
		}
		urlObj['weights'] = weightList
		urlObj['keywords'] = keywordList
	}

	host = location.host + "/browse/" + category + "?"
	listingURl = "http://" + host + makeURLFromParameters(urlObj)
	
	window.location = listingURl		
}

