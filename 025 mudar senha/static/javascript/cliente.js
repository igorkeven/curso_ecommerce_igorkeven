



const btnapagar_conta = document.querySelector(".apagar_conta");
const modal_apagarConta = document.querySelector("#modal_apagarConta");
const cancelarApagarConta = document.querySelector("#cancelarApagarConta");
const btnEscolha_formulario_senha = document.querySelector("#escolha_formulario_senha");
const produtos = document.querySelector("#produtos");
const formulario_senha = document.querySelector("#formulario_senha");
const titulo = document.querySelector("#titulo");
const btnHistorico = document.querySelector("#btnHistorico");
const paginaInicial = document.querySelector("#paginaInicial");
const Meus_pedidos = document.querySelector("#Meus_pedidos");
const historico = document.querySelector("#historico");

btnapagar_conta.addEventListener("click", ()=>{
    modal_apagarConta.style.display = 'block';
})

cancelarApagarConta.addEventListener("click", ()=>{
    modal_apagarConta.style.display = 'none';
})


btnHistorico.addEventListener('click', ()=>{
    historico.style.display = 'block';
    produtos.style.display = 'none';
    formulario_senha.style.display = 'none';
    titulo.textContent = "Meu Historico de Compras";

})



btnEscolha_formulario_senha.addEventListener("click", ()=>{
    produtos.style.display = 'none';
    formulario_senha.style.display = 'flex';
    historico.style.display = 'none';
    titulo.textContent = "Mudar Senha";

})


paginaInicial.addEventListener('click', ()=>{
    window.location.href = 'http://127.0.0.1:5500/templates/home.html';
})

Meus_pedidos.addEventListener("click", ()=>{
    produtos.style.display = 'flex';
    formulario_senha.style.display = 'none';
    historico.style.display = 'none';
    titulo.textContent = "Meu Carrinho";

})



const formNovasenha = document.querySelector("#formMudarSenha");
const novasenha = document.querySelector("#novaSenha");
const repertir = document.querySelector("#repetirNovaSenha");
const msgerro = document.querySelector("#errosenha");

formNovasenha.addEventListener("submit", (e) =>{
    if(novasenha.value !== repertir.value){
        msgerro.textContent = "As senhas não são iguais";
        e.preventDefault();
        return false;
    }
})