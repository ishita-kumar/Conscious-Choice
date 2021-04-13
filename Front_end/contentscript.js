chrome.runtime.sendMessage(
{
	from: 'content',
	subject: 'getTabId'
});


//Get Price

var productDescription = (function (){
	if(document.getElementById('productDescription')){
		
		var section = document.getElementById('productDescription');
		var descrp = section.getElementsByTagName('p')[0].innerText;
		
	return descrp; 
} 
else if (document.getElementById('unqualified')){
	var section = document.getElementById('unqualified');
	var availableFrom = section.getElementsByClassName('a-color-price')[0].innerText;
	return availableFrom;

} else if (document.getElementById('outOfStock')) {
	return "Out Of Stock";

} else if (document.getElementById('unqualifiedBuyBox')){
	return "See Buying Options";

} else if (document.getElementById('priceblock_saleprice')){
	var price = document.getElementById('priceblock_saleprice').innerText;
	
	return price;
} else
  return 'N/A'

})();


var asinNo = (function(){
	if(document.getElementById('detail-bullets')){
var section = document.getElementById('detail-bullets');
var list = section.getElementsByTagName('li');
for (var i = 0; i < list.length; i++){
	if (list[i].innerText.indexOf("ASIN") > -1){
		 var asinFull = list[i].innerText;
		 asinNum = asinFull.substring(asinFull.indexOf(' '));
	}
  }
  return asinNum;
} else if (document.getElementById('productDetails_detailBullets_sections1')){
	var section = document.getElementById('productDetails_detailBullets_sections1');
	var list = section.getElementsByTagName('td');
	for (var i = 0; i < list.length; i++){
	if (list[i].innerText.indexOf("B0") > -1){
		 var asinFull = list[i].innerText;
		 return asinFull;
	}
  }
} else if (document.getElementById('prodDetails')){
	var section = document.getElementById('prodDetails');
	var list = section.getElementsByTagName('td');
	for (var i = 0; i < list.length; i++){
	if (list[i].innerText.indexOf("B0") > -1){
		 var asinFull = list[i].innerText;
		 return asinFull;
	}
  }
} else if (document.getElementById('detail_bullets_id')){
	var section = document.getElementById('detail_bullets_id');
var list = section.getElementsByTagName('li');
for (var i = 0; i < list.length; i++){
	if (list[i].innerText.indexOf("ASIN") > -1){
		 var asinFull = list[i].innerText;
		 asinNum = asinFull.substring(asinFull.indexOf(' '));
		 return asinNum;
	}
  }
} else


  return 'N/A'

})();


chrome.runtime.onMessage.addListener(function(message, sender, response){
	if((message.from === 'popup') && (message.subject === 'getData')){
		var objson = {
		title:	document.getElementById("productTitle").innerText,
		asin: asinNo,

		};
		response(objson);	
	};
	
});





