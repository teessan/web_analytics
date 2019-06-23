var _void = function () { return; };
var now = new Date();
var url = window.location;
var ref = document.referrer;
url = encodeURI(url);
ref = encodeURI(ref);
if (ref == "") {
  ref = 'N/A'
}

if (url == "") {
  url = 'N/A'
}

function ckSave(){
    var date = new Date();
    term = parseInt(90);
    val = now.getTime()+Math.floor(Math.random()*10000);
    date.setTime(date.getTime()+term*24*60*60*1000);
    document.cookie = "_ck="+escape(val)+";expires="+date.toGMTString();

}
function ckLoad(){
    var r = document.cookie.split(';');
    //console.log(r);
    for(var i = 0; i < r.length; i++){
        content=r[i].split("=");
        if(content[0]==="_ck"){
            console.log(content);
            return content[1];
        }else{
            //return 0;
        }
    }
}
var result = document.cookie.indexOf('_ck');
if(result === -1){
    ckSave();
}
var cookie = ckLoad();
console.log(location.hostname);
