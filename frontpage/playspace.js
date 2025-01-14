//global variables
var songName = null;
var sendingStatus = false;

//HTML specific functions
let user_style = document.getElementById("dropdown").value;
const updateUserStyle = (event) => {
    if (event.target.value == "Custom") {
        fetch('https://api.ipify.org/?format=json')
        .then(results => results.json()) // Get JSON response from the IP API
        .then(data => {
            user_style = data.ip;
            // Send the updated payload to the server
        })
    }
    user_style = event.target.value;
};
document.getElementById("dropdown").addEventListener("change", updateUserStyle);

//making sure the file is valid before sending
async function sendFile() {
    if (sendingStatus == true) {
        document.getElementById("sendingButton").innerText = "Patience...";
        return;
    }

    var input = document.getElementById('file-input');
    if (input.files[0] == undefined) {
        document.getElementById("sendingButton").innerText = "Needs File";
        return;
    }

    songName = input.files[0].name.slice(0,-9);

    if ((input.files[0] == undefined)||(input.files[0].name.slice(-3) != "xml")) {
        document.getElementById("sendingButton").innerText = "wrong file type";
    }
    else {
        document.getElementById("sendingButton").innerText = "Sending...";
        sendingStatus = true;
        actuallySend(input.files[0], );
    }
}

//make the client download the file
function downloadXML(XMLData) {
    const a = document.createElement('a');
    const dataToSend = new Blob([XMLData], {type: "application/vnd.recordare.musicxml+xml"});
    const url = window.URL.createObjectURL(dataToSend);
    a.href = url;
    a.download = songName + '_Harmonized.musicxml';
    document.body.append(a);
    a.style.display = "none";
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
}

//function to actually send the file
async function actuallySend(FILE) {
    const reader = new FileReader();
    reader.onload = function () {
        fetch('http://127.0.0.1:8000/items/', {
            method: 'POST', // Specifying the method
            headers: { 
                'Content-Type': 'application/json' // Correct MIME type for JSON
            },
            body: JSON.stringify({name: 
                "xml to be harmonized", style: user_style, data: reader.result})
        })
        .then(response => response.text()) // Extract the response text
        .then(data => {
            document.getElementById("sendingButton").innerText = "Send File";
            //data = data.replace(/\n  /g, ''); this shit is not doing anything
            downloadXML(data);
            sendingStatus = false;
        })
    }
    reader.readAsText(FILE);
}
