function updateHomeBanner(frmVariable) { 
	
	var sliderBanner=new Array();
	var arrIndex=0;
	var TBanner = ""
	var PBanner = ""
	var MediaBanner = ""
	for(var i=0;i<frmVariable.elements.length;i++){
		if (frmVariable.elements[i].name=='TBanner') {
			TBanner = frmVariable.elements[i].value
		}
		if (frmVariable.elements[i].name=='PBanner') {
			PBanner = frmVariable.elements[i].value
		}
		if (frmVariable.elements[i].name=='SBanner') {
			SBanner = frmVariable.elements[i].value
			if (SBanner != "" && SBanner != "new") {
				sliderBanner[arrIndex] = SBanner;
				arrIndex ++;
			}
		}

		if (frmVariable.elements[i].name=='MediaBanner') {
			MediaBanner = frmVariable.elements[i].value
		}
		if (frmVariable.elements[i].name=='MediaLink') {
			MediaLink = frmVariable.elements[i].value
		}
		
	}

	$domain = location.host
	$url = "http://"  + $domain + "/admin/banner/home/submit"
	$url = $url + "?TBanner=" + TBanner + "&PBanner=" + PBanner + "&sliderBanner=" + sliderBanner + "&MediaLink=" + MediaLink + "&MediaBanner=" + MediaBanner
	console.log(httpGet($url))

}

function updateListingBanner(frmVariable) { 
	TBannerLinkList = new Array();
	tBannerLinkIndex = 0
	TBannerLocList = new Array();
	tBannerLocIndex = 0
	category = location.search.split('category=')[1]?location.search.split('category=')[1]:"0";
	var killer_prods=new Array();
	var arrIndex=0;
	var most_rev=new Array();
	var arrIndex_rev=0;
	for(var i=0;i<frmVariable.elements.length;i++) {
		if (frmVariable.elements[i].name == 'newCategory') {
			category = frmVariable.elements[i].value
			break;
		}
	}
	for(var i=0;i<frmVariable.elements.length;i++){
		if (frmVariable.elements[i].name=='most_reviewed') {
			mst_rev = frmVariable.elements[i].value
			if (mst_rev != "" && mst_rev != "new") {
				most_rev[arrIndex_rev] = mst_rev;
				arrIndex_rev ++;
			}
		}
	}

	TBannerList = extractedValues('TBanner', frmVariable)
	console.log(TBannerList)
	hotbrandsList = extractedValues('hotbrands', frmVariable)
	compareItemsIDList = extractedValues('compareItemsID', frmVariable)
	economicbrandsList = extractedValues('economicbrands', frmVariable)
	right_vertical = extractedValues('right_vertical', frmVariable)
	killerList = extractedValues('killer', frmVariable)
	responseJson = {}
	responseJson['compareitems'] = compareItemsIDList
	responseJson['hotbrands'] = hotbrandsList
	responseJson['economicbrands'] = economicbrandsList
	responseJson['topbanner'] = TBannerList
	responseJson['killer'] = killerList
	responseJson['most_reviewed'] = most_rev
	responseJson['right_vertical_aff'] = right_vertical
	responseJson['custome_item_list'] = getCustomItemsList(frmVariable, 'custom_product')
	responseJson['custom_link_list'] = getCustomItemsList(frmVariable, 'custom_link')
	dataJSON = {}
	dataJSON['data'] = responseJson
	dataJSON['category'] = category

	$domain = location.host
	$url = "http://"  + $domain + "/admin/banner/listing/submit"
	httpAjaxPost($url, JSON.stringify(dataJSON))
	
	return false;
}

function priceOverride(frmVariable, product_id) {
	
	website_list = ['amazon', 'flipkart', 'snapdeal']
	price_override = {}
	for(var i=0;i<frmVariable.elements.length;i++) {
		websiteIndex = website_list.indexOf(frmVariable.elements[i].name)
		if ( websiteIndex > -1 ){
			price = frmVariable.elements[i].value
			if (isNaN(parseFloat(price)) == false) {
				website = website_list[websiteIndex]
				price_override[website] = parseFloat(price)
			}
			
		}
	}
	responseJson = {}
	responseJson['override_price'] = price_override	
	$domain = location.host
	$url = "http://"  + $domain + "/admin/priceoverride/" + product_id
	httpAjaxPost($url, JSON.stringify(responseJson))
	
}

function getCustomItemsList(frmVariable, custome_list) {
	custome_item_list = {}
	for(var i=0;i<frmVariable.elements.length;i++){
		if (frmVariable.elements[i].name == custome_list + '_name'){
			if (frmVariable.elements[i].value != "new" && frmVariable.elements[i].value != "") {
				custom_list_name_val = frmVariable.elements[i].value
				custome_item_list[custom_list_name_val] = new Array()
				for(var j=0;j<frmVariable.elements.length;j++){
					console.log(custome_list + "_" + custom_list_name_val)
					if (frmVariable.elements[j].name == custome_list + "_" + custom_list_name_val){
						if (frmVariable.elements[j].value != "new" && frmVariable.elements[j].value != "") {
							custome_item_list[custom_list_name_val].push(frmVariable.elements[j].value)
						}				
					}
				}
			}
		}
		if (frmVariable.elements[i].name == 'new_' + custome_list + '_name'){
			
			if (frmVariable.elements[i].value != "new" && frmVariable.elements[i].value != "") {
				console.log(frmVariable.elements[i].value, "###")
				custome_item_list[frmVariable.elements[i].value] = new Array()
				for(var j=0;j<frmVariable.elements.length;j++){
					if (frmVariable.elements[j].name == 'new_' + custome_list + '_entry'){

						if (frmVariable.elements[j].value != "new" && frmVariable.elements[j].value != "") {
							console.log(frmVariable.elements[j].value, "###")
							custome_item_list[frmVariable.elements[i].value].push(frmVariable.elements[j].value)
						}				
					}
				}
			}
		}	
	}
	console.log(custome_item_list)
	return custome_item_list
}
function extractedValues(name, frmVariable) {
	link = name + "Link"
	loc = name + "Location"
	newLink = link + "New"
	newLocation = loc + "New"
	TBannerLinkList = new Array();
	tBannerLinkIndex = 0
	TBannerLocList = new Array();
	tBannerLocIndex = 0

	for(var i=0;i<frmVariable.elements.length;i++){

		if (frmVariable.elements[i].name == link){

			if (frmVariable.elements[i].value != '' && frmVariable.elements[i].value != "new") {
				
				TBannerLinkList[tBannerLinkIndex] = frmVariable.elements[i].value
			tBannerLinkIndex ++;
			}
		}
		if (frmVariable.elements[i].name == loc){
			if (frmVariable.elements[i].value !='' && frmVariable.elements[i].value != "new") {
				
				TBannerLocList[tBannerLocIndex] = frmVariable.elements[i].value
			tBannerLocIndex ++;
			}
		}
		if (frmVariable.elements[i].name == newLink){
			if (frmVariable.elements[i].value != '' && frmVariable.elements[i].value != "new") {
				TBannerLinkList[tBannerLinkIndex] = frmVariable.elements[i].value
			tBannerLinkIndex ++;
			}			
		}
		if (frmVariable.elements[i].name == newLocation){
			if (frmVariable.elements[i].value != '' && frmVariable.elements[i].value != "new") {
				TBannerLocList[tBannerLocIndex] = frmVariable.elements[i].value
			tBannerLocIndex ++;
			}
		}		
	}
	dictList = new Array();
	for (i=0;i< tBannerLocIndex; i++){
		dict = {}
		dict['link'] = TBannerLinkList[i]
		dict['location'] = TBannerLocList[i]
		
		dictList[i] = dict
	}
	return dictList
}


function httpGet(theUrl)
        {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", theUrl, false );
            xmlHttp.send( null );
            return xmlHttp.responseText;
        }
function httpAjaxPost(urlAddress, jsonData) {
	jQuery.ajax({
            url: urlAddress,
            type: 'PUT',
            headers: {
		        "Content-Type": "application/json"
		    },
            data: jsonData,
            success: function() { alert('Entry Successfully'); }
        });
}