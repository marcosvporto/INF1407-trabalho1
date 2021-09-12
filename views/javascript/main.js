/**
 * 
 * 
 * 
 */


/*
console.log("Alô mundo Javascript");


var nome;
nome = prompt("Qual o seu nome?");
console.log("O nome do usuário é " + nome);

alert("Olá "+ nome);

*/
/**
 * Esse evento onload vai ser disparado quando a página html for totalmente 
 * carregada, incluindo as imagens e os CSSs
 */

 onload = function() {
    
    var btnOpera = document.getElementById('idOpera');
    btnOpera.addEventListener('click', funcaoSoma);

}

function funcaoSoma() {
    //alert("Olá");
    var num1 = document.getElementById('idPrimeiroNumero').value;
    var num2 = document.getElementById('idSegundoNumero').value;
    var txtResultado = document.getElementById('idTextResultado');
    txtResultado.value = (parseInt(num1) + parseInt(num2)).toString()
}



