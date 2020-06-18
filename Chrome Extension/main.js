//This chrome extension allows you to interface with the radiooooo.com website with your keyboard.
//This extension was developped for the Rotary Radio project : https://create.arduino.cc/projecthub/carolinebuttet/rotary-musical-phone-14fd79
//You need to have this extension enabled and active when you visit the website https://radiooooo.com/

// The keycodes are as follow. Feel free to edit them or add new ones!
// 0  = click on decade 1900
// 1  = click on decale 1910
// 2  = click on decade 1920
// 3  = click on decale 1930
// 4  = click on decade 1940
// 5  = click on decale 1950
// 6  = click on decade 1960
// 7  = click on decale 1970
// 8  = click on decale 1980
// 9  = click on decade 1990
// q  = click on decale 2000
// w  = click on decale 2010
// e  = click on decale 2020

// If you wish to add your own countries, make sure you use the right ISO format:
// https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
// r  = click on country USA (United Stated)
// t  = click on country COL (Colombia)
// z  = click on country GBR (Great Britain)
// u  = click on country FRA (France)
// i  = click on country TUR (Turkey)
// o  = click on country MLI (Mali)
// p  = click on country MDG (Madagascar)
// a  = click on country RUS (Russia)
// s  = click on country JPN (Japan)
// d  = click on country NZL (New Zealand)



console.log("Radio extension go!!")


document.addEventListener("click", event => {
    console.log("onclick! ", event.target)
});


document.addEventListener("keydown", event => {
    console.log(event)
    switch (event.key) {
        case "0":
            click('.decade[data-decade="1900"]')
            break;
        case "1":
            click('.decade[data-decade="1910"]')
            break;
        case "2":
            click('.decade[data-decade="1920"]')
            break;
        case "3":
            click('.decade[data-decade="1930"]')
            break;
        case "4":
            click('.decade[data-decade="1940"]')
            break;
        case "5":
            click('.decade[data-decade="1950"]')
            break;
        case "6":
            click('.decade[data-decade="1960"]')
            break;
        case "7":
            click('.decade[data-decade="1970"]')
            break;
        case "8":
            click('.decade[data-decade="1980"]')
            break;
        case "9":
            click('.decade[data-decade="1990"]')
            break;
        case "q":
            click('.decade[data-decade="2000"]')
            break;
        case "w":
            click('.decade[data-decade="2010"]')
            break;
        case "e":
            click('.decade[data-decade="2020"]')
            break;
        case "r":
            mouseUpDpwn('g[data-isocode="USA"] path')
            break;
        case "t":
            mouseUpDpwn('g[data-isocode="COL"] path')
            break;
        case "z":
            mouseUpDpwn('g[data-isocode="GBR"] path')
            break;
        case "u":
            mouseUpDpwn('g[data-isocode="FRA"] path')
            break;
        case "i":
            mouseUpDpwn('g[data-isocode="TUR"] path')
            break;
        case "o":
            mouseUpDpwn('g[data-isocode="MLI"] path')
            break;
        case "p":
            mouseUpDpwn('g[data-isocode="MDG"] path')
            break;
        case "a":
            mouseUpDpwn('g[data-isocode="RUS"] path')
            break;
        case "s":
            mouseUpDpwn('g[data-isocode="JPN"] path')
            break;
        case "d":
            mouseUpDpwn('g[data-isocode="NZL"] path')
            break;
        default:
    }
});


function click(element) {
    document.querySelector(element).click();
}

function mouseUpDpwn(element) {
    document.querySelector(element).dispatchEvent(new MouseEvent("mousedown", {
        bubbles: true,
        cancelable: true
    }));
    window.setTimeout(() => {
        console.log("timeout")
        document.querySelector(element).dispatchEvent(new MouseEvent("mouseup", {
            bubbles: true,
            cancelable: true
        }));
    }, 20);
}