chrome.runtime.onMessage.addListener(function (message, sender) {
  if (message.from === "content" && message.subject === "getTabId") {
    chrome.pageAction.show(sender.tab.id);

  }
});
chrome.storage.local.get('prediction', function(result){
  var value=result
  // console.log("prediction",result)
 return value
    });

    chrome.storage.local.get('url', function(result){
  var url=result
  // console.log("prediction",result)
 return url
    });

