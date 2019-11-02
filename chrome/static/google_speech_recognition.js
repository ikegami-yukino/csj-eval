// Speech Recognition
let recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.lang = "ja-JP";

let request = new XMLHttpRequest();
let URL = "http://localhost:5000/chrome/"

recognition.onspeechstart = function(event) {
    console.log("[INFO] Recognition Start");
    document.getElementById("info").style.color="white";
    document.getElementById("info").innerText = "Please speak...";
};

function write(final_transcript){
    request.open("GET", URL + final_transcript);
    request.onreadystatechange = function () {
        if (request.readyState != 4) {
            document.getElementById("info").innerText = "Sending result...";
        } else if (request.status != 200) {
            document.getElementById("info").innerText = "ERROR!";
            console.log("[ERROR] Request status: " + request.status);
        } else {
            let result = request.responseText;
            document.getElementById("info").innerText = "Finished!";
            document.getElementById("google").innerText = result;
        }
    };
    request.send(null);
}

recognition.onresult = function(event) {
    var final_transcript = "";
    for (let i = event.resultIndex; i < event.results.length; i++){
        let transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal || i == event.results.length){
            final_transcript += transcript;
        }
        if (final_transcript){
            console.log(final_transcript);
            document.getElementById("google").innerText = final_transcript;
            fetch(URL + final_transcript, {method: "GET"});
            //write(final_transcript);
        }
    }
};

recognition.onerror = function(event) {
    console.log("[ERROR] " + event.error);
    document.getElementById("info").style.color="red";
    document.getElementById("info").innerText = "[ERROR] " + event.error;
};

recognition.onend = function(event) {
    console.log("[INFO] END");
    setTimeout(function(){recognition.start()}, 5);
};

window.onload = function() {
    recognition.start();
};
