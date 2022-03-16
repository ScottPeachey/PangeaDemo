let viewRotation = 0.0;
let viewDistance = 2.0;
let viewFocalLength = 50.0;
let pointData;

let leftTurn = document.getElementById("left-turn");
leftTurn.onclick = (event) => {
    viewRotation-=0.1;
    setText('rotation', viewRotation);
    renderImage().then();
    event.preventDefault();
};

let rightTurn = document.getElementById("right-turn");
rightTurn.onclick = (event) => {
    viewRotation+=0.1;
    setText('rotation', viewRotation);
    renderImage().then();
    event.preventDefault();
};

let viewParams = document.querySelectorAll('.view');
viewParams.forEach(el => {
    el.onchange = () => renderImage();
});

async function renderImage() {
    viewRotation = Number(document.getElementById('rotation').value);
    viewDistance = Number(document.getElementById('distance').value);
    viewFocalLength = Number(document.getElementById('focal_length').value);
}

function getUrl(path) {
    let host = document.URL;
    if (host.endsWith('/')) path = path.substring(1);
    return host + path
}

function setText(id, value) {
    let el = document.getElementById(id);
    el.value = value;
}

async function loadData() {
    setText('rotation', viewRotation);
    setText('distance', viewDistance);
    setText('focal_length', viewFocalLength);
}


