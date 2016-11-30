// redirect to rel-canonical, if there is one
var children = document.head.children;
Array.prototype.map.call(document.head.children, function (element) {
    if (element.tagName.toLowerCase() === 'link' && element.rel === 'canonical') {
        window.location = element.href;
    }
})
