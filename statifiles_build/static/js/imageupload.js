function fun(input) {
    if (input.files && input.files[0]) {
        console.log(input.files)
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#image_upload').attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}