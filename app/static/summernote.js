$('#summernote').summernote({
    placeholder: 'Write here',
    tabsize: 2,
    height: 500,
    callbacks: {
        onImageUpload: function (image) {
            uploadImage(image[0]);
        }
    }
});

function uploadImage(image) {
    var data = new FormData();
    data.append("image", image);
    $.ajax({
        url: "/upload",
        cache: false,
        contentType: false,
        processData: false,
        data: data,
        type: "POST",
        success: function (filename) {
            var image = $('<img>').attr('src', '/uploads/' + filename).addClass("img-fluid");
            $('#summernote').summernote("insertNode", image[0]);
        },
        error: function (data) {
            console.log(data);
        }
    });
}