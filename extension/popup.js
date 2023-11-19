chrome.tabs.query({
    active: true,               // Select active tabs
    lastFocusedWindow: true     // In the current window
}, function(array_of_Tabs) {
    var tab = array_of_Tabs[0];
    var current_url = tab.url;
    var url_response = httpGet("http://localhost:8000/?url="+current_url)
    var ingredients_json = JSON.parse(url_response);
    // document.getElementById("ingredient").innerHTML = url_response
    
    // sleep time expects milliseconds
    function sleep (time) {
        return new Promise((resolve) => setTimeout(resolve, time));
    }
    
    // Usage!
    sleep(3000).then(() => {
        document.getElementById("ingredient").innerHTML = ingredients_json.harsh_chemicals_present
        document.getElementById('popup_loading').style.display = 'none';
    });
    
});

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}