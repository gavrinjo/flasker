$('#summernote').summernote({
    lang: "en-EN",
    dialogsInBody: true,
    height: 220,
    minHeight: null,
    maxHeight: null,
    shortCuts: false,
    fontSize: 14,
    disableDragAndDrop: false,
    toolbar: [
        ["style", ["bold", "italic", "underline", "clear"]],
        ["font", ["strikethrough", "superscript", "subscript"]],
        ["fontsize", ["fontsize"]],
        ["color", ["color"]],
        ["para", ["ul", "ol", "paragraph"]],
        ["height", ["height"]],
        ["Insert", ["picture"]],
        ["Other", ["fullscreen", "codeview"]]
    ],
    callbacks: {
        onImageUpload: function(image) {
            var sizeKB = image[0]['size'] / 1000;
            var tmp_pr = 0;
            if(sizeKB > 200){
                tmp_pr = 1;
                alert("pls, select less then 200kb image.");
            }
            if(image[0]['type'] != 'image/jpeg' && image[0]['type'] != 'image/png'){
                tmp_pr = 1;
                alert("pls, select png or jpg image.");
            }
            if(tmp_pr == 0){
                var file = image[0];
                var reader = new FileReader();
                reader.onloadend = function() {
                    var image = $('<img>').attr('src',  reader.result);
                    $('#editor').summernote("insertNode", image[0]);
                }
            reader.readAsDataURL(file);
            }
        }
    }
});