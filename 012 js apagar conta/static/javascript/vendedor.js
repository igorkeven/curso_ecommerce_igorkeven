

const btnapagar_conta = document.querySelector(".apagar_conta");
const modal_apagarConta = document.querySelector("#modal_apagarConta");
const cancelarApagarConta = document.querySelector("#cancelarApagarConta");

btnapagar_conta.addEventListener("click", ()=>{
    modal_apagarConta.style.display = 'block';
})

cancelarApagarConta.addEventListener("click", ()=>{
    modal_apagarConta.style.display = 'none';
})
