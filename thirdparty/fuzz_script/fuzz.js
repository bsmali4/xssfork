/**
 * Created by bsmali4 on 17/6/14.
 * 用法 ./phantomjs fuzz.js "http://127.0.0.1/xsstest/demo3.php?id=%3Cimg%20src=1%20onerror=alert(1)%3E" "user=admin;pass=123"
 */
var url;
var post_data;
var cookie;
var referer;
var timeout;
var http_method;
var system = require("system");
var page = require("webpage").create();
var EVENT_LIST;
function isContains(str, substr) {
    return str.indexOf(substr) >= 0;
}
function onInitialized(){
    page.onInitialized = function () {
        _addEventListener = Element.prototype.addEventListener;
        Element.prototype.addEventListener = function(a,b,c) {
            EVENT_LIST.push({"event": event, "element": this});
            _addEventListener.apply(this, arguments);
        };
    };
}
function initArgs(){
    url = system.args[1];
    post_data = system.args[3];
    cookie = system.args[2] ? system.args[2] : "";
    referer = system.args[4];
    timeout = system.args[5];
    http_method = post_data ? "POST": "GET";
    initWebkit();
}
function initWebkit() {
    page.settings.loadImages = false;
    page.settings.resourceTimeout = timeout ? timeout * 1000 : 5 * 1000;
    headers = {};
    headers['Cookie'] = cookie;
    headers['Referer'] = referer;
    page.customHeaders = headers;
    page.viewportSize = {
        width: 1024,
        height: 768
    }
}
function hookAlert(){
    page.onAlert = function (msg) {
        console.log("===alert===" + msg + "===alert===");
        phantom.exit();
    };
}
function evalOnEvent(nodes){
    for (var i = 0; i < nodes.length; i++){
        var attrs = nodes[i].attributes;
        for (var j = 0; j < attrs.length; j++){
            attr_name = attrs[j].nodeName;
            attr_value = attrs[j].nodeValue;
            if (attr_name.substr(0, 2) == "on") {
                try{
                    eval(attr_value.replace(/return.*;/g,''));
                } catch (e){
                    console.log(e);
                }
            }
            if (attr_name in {"src": 1, "href": 1} && attrs[j].nodeValue.substr(0, 11) == "javascript:"){
                try{
                    eval(attr_value.substr(11));
                } catch (e){
                    console.log(e);
                }
            }
        }
    }
}
function dispatchEvent(){
    for(var i in EVENT_LIST){
        var evt = document.createEvent('CustomEvent');
        evt.initCustomEvent(EVENT_LIST[i]["event"], true, true, null);
        EVENT_LIST[i]["element"].dispatchEvent(evt);
    }
}
function evaluate(EVENT_LIST) {
    page.evaluate(function (EVENT_LIST) {
        function dispatchEvent(EVENT_LIST){
            for(var i in EVENT_LIST){
                var evt = document.createEvent('CustomEvent');
                evt.initCustomEvent(EVENT_LIST[i]["event"], true, true, null);
                EVENT_LIST[i]["element"].dispatchEvent(evt);
            }
        }
        function evalOnEvent(nodes){
            for (var i = 0; i < nodes.length; i++){
                var attrs = nodes[i].attributes;
                for (var j = 0; j < attrs.length; j++){
                    attr_name = attrs[j].nodeName;
                    attr_value = attrs[j].nodeValue;
                    var onevents = {'onerror': 1, 'onload': 1, 'onmouseover': 1, 'onfocus': 1, 'onclick': 1};
                    //attr_name.substr(0, 2) == "on"
                    if (attr_name in onevents) {
                        try{
                            eval(attr_value.replace(/return.*;/g,''));
                        } catch (e){
                            console.log(e);
                        }
                    }
                    if (attr_name in {"src": 1, "href": 1} && attrs[j].nodeValue.substr(0, 11) == "javascript:"){
                        try{
                            eval(attr_value.substr(11));
                        } catch (e){
                            console.log(e);
                        }
                    }
                }
            }
        }
        dispatchEvent();
        evalOnEvent(document.all);
    });
}


if (!system.args[1]) {
    var notice = "Usage: " + system.args[0] + " <url> <cookie> <post_data> <referer> <timeout>";
    console.log(notice);
    phantom.exit();
} else {
    onInitialized();
    initArgs();
    hookAlert();
    page.open(url, {operation: http_method, data: post_data,}, function (status) {
        if (status !== "success"){
            console.log('Unable to connect' + url);
        }
        else {
            try{
                evaluate(EVENT_LIST);
            } catch (e){
                console.log(e);
            }
        }
        phantom.exit();
    });
}