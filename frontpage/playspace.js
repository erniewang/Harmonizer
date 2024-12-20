function sendFile() {
    var input = document.getElementById('file-input');
    if ((input.files[0] == undefined)||(input.files[0].name.slice(-3) != "xml")) {
        document.getElementById("sendingButton").innerText = "wrong file type";
    }
    else {
        console.log(input.files[0].toString());
        document.getElementById("sendingButton").innerText = "Sending...";

        //need to parse and serialize the xml file into a string format to then stick onto a json

        fetch('http://127.0.0.1:8000/items/', {
            method: 'POST', // Specifying the method
            headers: {
                'Content-Type': 'application/json' // Correct MIME type for JSON
            },
            body: JSON.stringify({name: input.files[0].name, data: input.files[0].toString()})
        })
        .then(response => response.text()) // Parsing the response as text
        .then(data => console.log(data)) // Logging the response to the console
    }
}

