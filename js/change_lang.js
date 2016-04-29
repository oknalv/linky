function change_lang(tags, langs, user_lang) {
    $.each(tags, function( key, value){
        if(value == "text"){
            $("#" + key).text(langs[user_lang][key]);
        }
        if(value == "placeholder"){
            $("#" + key).attr("placeholder", langs[user_lang][key]);
        }
    });
}