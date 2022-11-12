
window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition

function voiceSearch(){
    if ('SpeechRecognition' in window) {
        console.log("SpeechRecognition is Working");
    } else {
        console.log("SpeechRecognition is Not Working");
    }

    var inputSearchQuery = document.getElementById("search_query");
    const recognition = new window.SpeechRecognition();
    //recognition.continuous = true;

    micButton = document.getElementById("mic_search");

    if (micButton.innerHTML == "mic") {
        recognition.start();
    } else if (micButton.innerHTML == "mic_off"){
        recognition.stop();
    }

    recognition.addEventListener("start", function() {
        micButton.innerHTML = "mic_off";
        console.log("Recording.....");
    });

    recognition.addEventListener("end", function() {
        console.log("Stopping recording.");
        micButton.innerHTML = "mic";
    });

    recognition.addEventListener("result", resultOfSpeechRecognition);
    function resultOfSpeechRecognition(event) {
        const current = event.resultIndex;
        transcript = event.results[current][0].transcript;
        inputSearchQuery.value = transcript;
        console.log("transcript : ", transcript)
    }
}




function textSearch() {
    var searchText = document.getElementById('search_query');
    if (!searchText.value) {
        alert('Please enter a valid text or voice input!');
    } else {
        searchText = searchText.value.trim().toLowerCase();
        console.log('Searching Photos....');
        searchPhotos(searchText);
    }

}

function searchPhotos(searchText) {

    console.log(searchText);
    document.getElementById('search_query').value = searchText;
    document.getElementById('photos_search_results').innerHTML = "<h4 style=\"text-align:center\">";

    var params = {
        'q' : searchText,
        'x-api-key': "fyzXzq8Toh7BIrGHRTItaaABS1Z2BDNu4s9qiYh1"
    };

    var additionalParams = {

    };
    var apigClient = apigClientFactory.newClient(
      apiKey: 'fyzXzq8Toh7BIrGHRTItaaABS1Z2BDNu4s9qiYh1'
    );
    //call search api
    apigClient.searchGet(params, {}, {})
        .then(function(result) {
            //console.log(JSON.parse(result));
            image_paths = result["data"];
            console.log("image_paths : ", image_paths);
            var photosDiv = document.getElementById("photos_search_results");
            photosDiv.innerHTML = "";

            if (Array.isArray(image_paths)){
              var n;
              for (n = 0; n < image_paths.length; n++) {
                  images_list = image_paths[n].split('/');
                  imageName = images_list[images_list.length - 1];

                  photosDiv.innerHTML += '<figure><img src="' + image_paths[n] + '" style="width:25%"><figcaption>' + imageName + '</figcaption></figure>';
              }

            }
            else{
              photosDiv.innerHTML = 'No resutls found!';
            }
        }).catch(function(result) {
            console.log(result);
        });
}

function uploadPhoto() {
    var apigClient = apigClientFactory.newClient(
      apiKey: 'fyzXzq8Toh7BIrGHRTItaaABS1Z2BDNu4s9qiYh1'
    );
    var filePath = (document.getElementById('uploaded_file').value).split("\\");
    var fileName = filePath[filePath.length - 1];

    if (!document.getElementById('custom_labels').innerText == "") {
        var customLabels = document.getElementById('custom_labels');
    }
    console.log(fileName);

    console.log(custom_labels.value);

    // var reader = new FileReader();
    var file = document.getElementById('uploaded_file').files[0];
    file.constructor = () => file;

    console.log('File : ', file);
    //document.getElementById('uploaded_file').value = "";

    if ((filePath == "") || (!['png', 'jpg', 'jpeg'].includes(fileName.split(".")[1]))) {
        alert("Please upload a valid .png/.jpg/.jpeg file!");
    } else {

        var params = {
          "folder":"lixuanyanghw2",
          "item": file.name,
          "Content-Type":file.type,
          'x-amz-meta-customLabels':custom_labels.value,
          'x-api-key': "fyzXzq8Toh7BIrGHRTItaaABS1Z2BDNu4s9qiYh1"
          //'Access-Control-Allow-Origin':"*"
        };
        console.log("Content-Type:",file.type)
        var additionalParams = {
        };

        apigClient.uploadFolderItemPut(params, file, additionalParams)

        // reader.onload = function (event) {
        //     //bodybtoa = btoa(event.target.result);
        //     var src = event.target.result;
        //     var newImage = document.createElement("img");
        //     newImage.src = src;
        //     encoded = newImage.outerHTML;
        //
        //     last_index_quote = encoded.lastIndexOf('"');
        //     encodedStr = encoded.substring(33, last_index_quote);
        //     /*
        //     if (fileExt == 'jpg' || fileExt == 'jpeg' || fileExt == 'png') {
        //       encodedStr = encoded.substring(33, last_index_quote);
        //     }
        //     else {
        //       encodedStr = encoded.substring(32, last_index_quote);
        //     }*/
        //
        //     //body = encodeURIComponent(event.target.result);
        //     console.log('Image sent to s3: ', encodedStr);
        //     return apigClient.uploadFolderItemPut(params, encodedStr, additionalParams)
        //     .then(function(result) {
        //         console.log(result);
        //     })
        //     .catch(function(error) {
        //         console.log(error);
        //     })
        // }
        // reader.readAsDataURL(file);
    }
}
