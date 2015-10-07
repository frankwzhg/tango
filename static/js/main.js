
var myImage = document.querySelector('img');

myImage.onclick = function(){
    var mySrc = myImage.getAttribute('src');
    if (mySrc === "/static/images/about.JPG"){
        myImage.setAttribute('src', "/static/images/pic.JPG");
    } else{
        myImage.setAttribute('src', "/static/images/about.JPG");
    }
};
var myButton = document.querySelector('button');
var myHeading = document.querySelector('h1');

function setUserName(){
    var myName = prompt('please enter your name');
    localStorage.setItem('name', myName);
    myHeading.innerHTML = 'Mozilla is cool, ' + myName;
}

if (!localStorage.getItem('name')){
        setUserName();
    }else{
        var storedName = localStorage.getItem('name');
        myHeading.innerHTML = 'Mozilla is cool, ' + storedName;
    }

myButton.onclick = function(){
    setUserName()
}