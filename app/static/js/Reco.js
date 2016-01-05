
var click=0;
var count=1;
var flag=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
var category;
var all_cat_detailJS = {}
HttpAjax('/restfull/categorydetails');

jQuery(document).ready(function($){ 
	$('.price_checkbox').click(function(){
		console.log("clicked");
	});
});


function remove_flag()
{
for(i=1;i<=40;i++)
flag[i]=0;
count=1;
}

function reco_slider_children(category, thisLink, catAppend) {
	var name = thisLink.id
	//the current children id
	//alert(name);
	var current = jQuery("#" + name).parent().attr("id");	//the parent div id
	jQuery("#"+current).html('<br><br> <h1>Choose Product Categories</h1>')
	console.log(name, current)
	children = all_cat_detailJS[category]['children']
	category_parent = all_cat_detailJS[category]['parent'][0]
	console.log(thisLink)
	cat_Str = ""
	for (child of children) {
		childDetails = all_cat_detailJS[child]
		child_of_child = all_cat_detailJS[child]['children']
		console.log(child_of_child)
		if (child_of_child.length > 0) {
			jQuery("#"+current).append('<div id=' + '"reco_' + child.replace(" ", "_") + '" class="pop_box" onclick="reco_slider_children(&#39;' + child + '&#39;,this,&#39;' + catAppend +'&#39;);">' + 
				'<img src=https://s3-ap-southeast-1.amazonaws.com/bazaarfunda/Website/static/logo/home_' + child + '.png alt="' + child + '"></div>');
		
		}

		else {
			if (catAppend) {

				jQuery("#"+current).append('<div id=' + '"reco_' + child.replace(" ", "_") + '" class="pop_box" onclick="start_recommendationSlider(&#39;' + child + '&#39;,this,&#39;' + catAppend.replace(' ', '_') +'&#39;);">' + 
				'<img src=https://s3-ap-southeast-1.amazonaws.com/bazaarfunda/Website/static/logo/home_' + child + '.png alt="' + child + '"></div>');
			}
			else {
				jQuery("#"+current).append('<div id=' + '"reco_' + child.replace(" ", "_") + '" class="pop_box" onclick="start_recommendationSlider(&#39;' + child + '&#39;,this,&#39;&#39;);">' + 
				'<img src=https://s3-ap-southeast-1.amazonaws.com/bazaarfunda/Website/static/logo/home_' + child + '.png alt="' + child + '"></div>');
			}	
		
		}
	}

	if (catAppend != category.replace(' ','_')) {
		if (category_parent) {
		jQuery("#"+current).append('<br><span id="slide_2_back" class="btn back" onclick="reco_slider_children(&#39;' + category_parent + '&#39;,this,&#39;' + catAppend.replace(' ', '_') + '&#39;)">BACK</span>');
		}
		else {		
			jQuery("#"+current).append('<br><span id="slide_2_back" class="btn back" onclick="reco_slider_AllParentCat(&#39;' + category_parent + '&#39;,this,&#39;' + catAppend.replace(' ', '_') + '&#39;)">BACK</span>');
		}
	}
	
      
}

function reco_slider_AllParentCat(category, thisLink, catAppend) {
	console.log(thisLink)
	var name = thisLink.id
	//the current children id
	//alert(name);

	var current = jQuery("#" + name).parent().attr("id");	//the parent div id
	
	jQuery("#"+current).html('<br><br> <h1>Choose Product Categories</h1>')
	for (cat in all_cat_detailJS) { 
		cat_parent = all_cat_detailJS[cat]['parent']
		if (typeof cat_parent === 'undefined') {
				if (all_cat_detailJS[cat]['children']) {
					jQuery("#"+current).append('<div id="reco_' + cat.replace(" ", "_") + '" class="pop_box" onclick="reco_slider_children(&#39;' + cat + '&#39;,this,&#39;&#39;' + "" +');">' + 
						'<img src=https://s3-ap-southeast-1.amazonaws.com/bazaarfunda/Website/static/logo/home_' + cat + '.png alt="' + cat + '"></div>');
				}
				else {
					jQuery("#"+current).append('<div id="reco_' + cat.replace(" ", "_") + '" class="pop_box" onclick="start_recommendationSlider(&#39;' + cat + '&#39;,this,&#39;&#39;' + catAppend +');">' + 
						'<img src=https://s3-ap-southeast-1.amazonaws.com/bazaarfunda/Website/static/logo/home_' + cat + '.png alt="' + cat + '"></div>');
				}
		}
		else {
			if (cat_parent.length == 0) {
				if (all_cat_detailJS[cat]['children']) {
					jQuery("#"+current).append('<div id="reco_' + cat.replace(" ", "_") + '" class="pop_box" onclick="reco_slider_children(&#39;' + cat + '&#39;,this,&#39;&#39;' + "" +');">' + 
						'<img src=https://s3-ap-southeast-1.amazonaws.com/bazaarfunda/Website/static/logo/home_' + cat + '.png alt="' + cat + '"></div>');
				}
				else {
					jQuery("#"+current).append('<div id="reco_' + cat.replace(" ", "_") + '" class="pop_box" onclick="start_recommendationSlider(&#39;' + cat + '&#39;,this,&#39;&#39;' + catAppend +');">' + 
						'<img src=https://s3-ap-southeast-1.amazonaws.com/bazaarfunda/Website/static/logo/home_' + cat + '.png alt="' + cat + '"></div>');
				}
				}
		}
	}
	if (catAppend !='') {
		console.log(catAppend)
		jQuery("#"+current).append('&nbsp;&nbsp; <br><br><span id="slide_2_back" class="btn back" onclick="reco_slider_prev(this,&#39;' + catAppend.replace(' ','_') + '&#39;)">BACK</span>')
	}

}

function reco_slider_next(thislink, catAppend) {
		
	var max = 4;		
	if (catAppend) {
		var str= catAppend + "reco_slide_";	
	}

	else {
		var str="reco_slide_";
	}
	var name=thislink.id

	var current=jQuery("#"+name).parent().attr("id");	//the parent div id
	
	//alert(current);
	var inr = current.slice(-1);				//getting id number (last)	
	if(inr == max)
		inr=1;									//boundary check maintaining cycle
	else
		inr = Number(inr)+1;					//increment by 1													
	var next = str.concat(inr);	

	jQuery("#"+current).animate({left: '-1000px'},"slow").hide(50);	//animating sequences 1
	jQuery("#"+next).animate({left: '1000px'},"slow");				//2
	jQuery("#"+next).show(50).animate({left: '0px'},"slow");		//3
}

function reco_slider_prev(thislink, catAppend) {
	console.log(thislink)
	var max=4;									//depend on no of slide
	if (catAppend) {
		var str= catAppend + "reco_slide_";	
	}			
	else {
		var str="reco_slide_";	
	}				//depend on no of slide				//id name to concat
	console.log(str, catAppend)
	//alert(thislink);	
	var name = thislink.id						//the current children id
	//alert(name);
	var current = jQuery("#"+name).parent().attr("id");	//the current id
	//alert(current);
	var inr = current.slice(-1);				//getting id number
	if(inr==1)
		inr=max;								//boundary maintaining cycle
	else
		inr = Number(inr)-1;					//decrement by 1
	if (catAppend) {
		if (inr == 1 ) {
			inr = 2
		}
	}
		
	var next = str.concat(inr);					//concat to get id of next div
	jQuery("#"+current).animate({left: '1000px'},"slow").hide(50);	//animating sequences 1
	jQuery("#"+next).animate({left: '-1000px'},"slow");				//2
	jQuery("#"+next).show(50).animate({left: '0px'},"slow");		//3
}


function is_selected(thislink)
{	
	var d = new Date();
	var t0 = performance.now();
	//console.log("in is_selected")
	//console.log(d.getMilliseconds())
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
		var t3 = performance.now();
		console.log("Call to is selected ADD took " + (t3 - t0) + " milliseconds.")	
		
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
		var t2 = performance.now();
		console.log("Call to is selected REMOVE took " + (t2 - t0) + " milliseconds.")
	}
	else {
		alert("Max Preference Selected")
	}
	var t1 = performance.now();
	console.log("Call to is selected END took " + (t1 - t0) + " milliseconds.")
	//console.log(d.getMilliseconds())
}


function start_recommendationSlider(category, thisLink, catAppend) {
	if (category == 'all' ) {
		category = catAppend
	}
	
	window.category = category
	reco_slider_next(thisLink, catAppend);
	
	all_key_details = window.all_cat_detailJS[category]['allKeyWordsIcon']
	all_key_text = window.all_cat_detailJS[category]['allKeywordsRecoText']
	reco_slider_str = '#' + catAppend + 'reco_slide_3'
	

	catr_str_reco = category
	if (category.slice(-1) === 's') { 
		catr_str_reco = category.slice(0, -1);
	}

	jQuery(reco_slider_str).html('<h1>My New ' + ((category.slice(-1) === 's') ? catr_str_reco = category.slice(0, -1) : category ) + ' is for</h1><h5>Just click according to your priorities with a maximum of 5.<br> Top most priority should be clicked 1st</h5>');
	iter_val = 1
	for (var kye_iter in all_key_details) {
		jQuery(reco_slider_str).append('<div data = "' + kye_iter + '" id="mob_key_' +  ("0" + iter_val.toString()).slice(-2) + '" class="pop_box" onclick="is_selected(this)"><i class="fa ' + all_key_details[kye_iter] + ' fa-5x "></i><div class="product-name aligncenter" style="height:33px">' + all_key_text[kye_iter] + '</div></div>&nbsp;&nbsp;');
	iter_val ++;
		} 
	jQuery(reco_slider_str).append("<br><span id='slide_3_back' class='btn back' onclick='reco_slider_prev(this, &#39;" + catAppend + "&#39;); remove_flag()'>BACK</span>");
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
	try {
		for (price = all_cat_detailJS[category]['priceRange'][0]; price <= all_cat_detailJS[category]['priceRange'][1];  price = price + all_cat_detailJS[category]['price_interval'] )
		{		
		str+=' <li ><input type="checkbox" onclick = "check_checkbox(this);" class="price_checkbox" id = "' + price + '" + valuei="'+price+'" + valuej="'+ (price +all_cat_detailJS[category]['price_interval']).toString() +'"   /><label for="' + price + '"> RS ' + price.toString() + " - Rs " + (price +all_cat_detailJS[category]['price_interval']).toString()  + '</label></li>';
		}
	}
	catch(err) {
		console.log(err)
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

function HttpAjax(path) {
	console.log("In That Ajax")
    var result;
    var host = window.location.origin
  	theUrl = host + path

    $.ajax({
        url: theUrl,
        success: function(response) {
            window.all_cat_detailJS = response;
            console.log(window.all_cat_detailJS)
            // return response; // <- I tried that one as well
        }
    });
}

// preload images

function preloadImages(array) {
    if (!preloadImages.list) {
        preloadImages.list = [];
    }
    var list = preloadImages.list;
    for (var i = 0; i < array.length; i++) {
        var img = new Image();
        img.onload = function() {
            var index = list.indexOf(this);
            if (index !== -1) {
                // remove image from the array once it's loaded
                // for memory consumption reasons
                list.splice(index, 1);
            }
        }
        list.push(img);
        img.src = array[i];
    }
}

preloadImages(["static/css/Count/count_1.png", "static/css/Count/count_2.png", "static/css/Count/count_3.png","static/css/Count/count_4.png","static/css/Count/count_5.png"]);
