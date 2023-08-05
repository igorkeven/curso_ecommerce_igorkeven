


const tipoCadastro = document.querySelector("#tipoCadastro");
const tituloVendedor = document.querySelector("#tituloVendedor");
const tituloCliente = document.querySelector("#tituloCliente");
const vendedorCadastro = document.querySelector("#vendedorCadastro");
const clienteCadastro = document.querySelector("#clienteCadastro");

tipoCadastro.addEventListener('submit', (event) => {
    event.preventDefault();
    const selecionarTipoCadastro = document.querySelector("#selecionarTipoCadastro").value;
    if (selecionarTipoCadastro === 'vendedor') {
        tituloVendedor.style.display = 'block';
        vendedorCadastro.style.display = 'block';
        tituloCliente.style.display = 'none';
        clienteCadastro.style.display = 'none';
        vendedorCadastro.scrollIntoView({behavior: 'smooth'})
    }else{
        tituloVendedor.style.display = 'none';
        vendedorCadastro.style.display = 'none';
        tituloCliente.style.display = 'block';
        clienteCadastro.style.display = 'block';
        clienteCadastro.scrollIntoView({behavior: 'smooth'})
    }
} )

clienteCadastro.addEventListener('submit', (event) =>{
    event.preventDefault();
    let senha = document.querySelector("#senhacliente");
    let repetirSenha = document.querySelector("#repetirSenhacliente");
    let msgErro = document.querySelector("#msgErroCliente");

    if (senha.value !== repetirSenha.value) {
        msgErro.style.display = 'block';
        repetirSenha.style.background = 'red';
        senha.style.background = 'red';
        return false;
    }else{
        msgErro.style.display = 'none';
        repetirSenha.style.background = 'white';
        senha.style.background = 'white';
        clienteCadastro.submit();
        return true;
    }
})

vendedorCadastro.addEventListener('submit', (event) =>{
    event.preventDefault();
    let senha = document.querySelector("#senhaVendedor");
    let repetirSenha = document.querySelector("#repetirSenhaVendedor");
    let msgErro = document.querySelector("#msgErroVendedor");

    if (senha.value !== repetirSenha.value) {
        msgErro.style.display = 'block';
        repetirSenha.style.background = 'red';
        senha.style.background = 'red';
        return false;
    }else{
        msgErro.style.display = 'none';
        repetirSenha.style.background = 'white';
        senha.style.background = 'white';
        vendedorCadastro.submit();
        return true;
    }
})