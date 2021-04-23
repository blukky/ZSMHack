jQuery(function(){
var verif = true
while (verif){
    var result = prompt("Введите пароль","")
//    console.log(result)
    if (result === null){
    console.log(history.back());
    history.back()
    verif = false
    }
    if (result == $('#pswd').data('value')){
        verif = false
    }
};
});