jQuery(document).ready(function($){  
	
  category = $('#category').attr('data-name');
  console.log("in overrides", category)
  if (category === "mobiles" || category === "tablets") {
  	console.log("in overrides", category)
  	$(".product-image-wrapper.listing").css({'max-height':'120px'});
  }
  else {
  	$(".product-image-wrapper.listing").css({'max-height':'80px});
  }
  
});