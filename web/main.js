const ctx = new AudioContext();
let audio1;

function generateRaga() {
	var fileInput =
		document.getElementById('audio');

	var filePath = fileInput.value;

	// Allowing file type
	var allowedExtensions = /(\.wav)$/i;

	if (!allowedExtensions.exec(filePath)) {
		alert('Invalid file type');
		fileInput.value = '';
		return false;
	}
	else {
		var audio = document.getElementById("audio")

		console.log("Here");
		console.log("Here");
		if (fileInput.files && fileInput.files[0]) {
			console.log("There")
			var reader = new FileReader();
			reader.onload = function (e) {
				console.log(e.target.result);
				fetch(e.target.result)
					.then(data => data.arrayBuffer())
					.then(arrayBuffer => ctx.decodeAudioData(arrayBuffer))
					.then(decodedAudio => {
						audio1 = decodedAudio;
						console.log(audio1)

						var myAudioArray = []

						for (var channel = 0; channel < 2; channel++) {
							// This gives us the actual array that contains the data
							myAudioArray = audio1.getChannelData(channel);
							console.log(myAudioArray)
							console.log(typeof myAudioArray)
						}


						eel.process_audio(myAudioArray)(displayRaga)
					});

			}
			reader.readAsDataURL(fileInput.files[0]);
			console.log("where")
		}
	}
}

function decodedDone(decoded) {

	var typedArray = new Object(decoded.length);

	typedArray=decoded.getChannelData(0);
	console.log("typedArray:");
	console.log(typedArray);

}

function displayRaga(raga) {
    var output = raga
    document.getElementById("raga").value = output
    console.log(output)
}
