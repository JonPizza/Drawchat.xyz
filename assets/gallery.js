function clearDivArray() {
    for (var i = 0; i < 100; i++) {
        for (var j = 0; j < 100; j++) {
            var d = document.getElementById(i + "-" + j)
            d.style.backgroundColor = "white";
        }
    }
}

function loadImage(date) {
    clearDivArray();
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/v1/getImgByDate/?date=" + date, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            var j = JSON.parse(xhr.responseText);
            
            for (i in j.pixels) {
                var cell = document.getElementById(j.pixels[i][0]);
                console.log(j.pixels[i][0]);
                cell.style.backgroundColor = j.pixels[i][1];
            }
        }
    }
    xhr.send();
}

function createDivArray() {
    var canvas = document.getElementById("drawing-box");
    for (var i = 0; i < 100; i++) {
        for (var j = 0; j < 100; j++) {
            var d = document.createElement("div");
            d.setAttribute("class", "cell-nohover");
            d.setAttribute("id", i + "-" + j);
            canvas.appendChild(d);
        }
    }
}

createDivArray();
