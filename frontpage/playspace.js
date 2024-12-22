//const convert = require('xml-js');
var downloadMode = false;

async function sendFile(downloadMode) {
    var input = document.getElementById('file-input');

    if ((input.files[0] == undefined)||(input.files[0].name.slice(-3) != "xml")) {
        document.getElementById("sendingButton").innerText = "wrong file type";
    }
    else {
        document.getElementById("sendingButton").innerText = "Sending...";
        actuallySend(input.files[0], );
        //need to parse and serialize the xml file into a string format to then stick onto a json
    }
}

function downloadXML(XMLData) {
    const a = document.createElement('a');
    const dataToSend = new Blob([XMLData], {type: "application/vnd.recordare.musicxml+xml"});
    const url = window.URL.createObjectURL(dataToSend);
    a.href = url;
    a.download = 'result.musicxml';
    document.body.append(a);
    a.style.display = "none";
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
}

async function actuallySend(FILE) {
    const reader = new FileReader();
    reader.onload = function () {
        fetch('http://127.0.0.1:8000/items/', {
            method: 'POST', // Specifying the method
            headers: { 
                'Content-Type': 'application/json' // Correct MIME type for JSON
            },
            body: JSON.stringify({name: 
                "xml to be harmonized", data: reader.result})
        })
        .then(response => response.text()) // Extract the response text
        .then(data => {
            document.getElementById("sendingButton").innerText = "Send File";
            //data = data.replace(/\n  /g, ''); this shit is not doing anything
            downloadXML(data);
        })
    }
    reader.readAsText(FILE);
}
