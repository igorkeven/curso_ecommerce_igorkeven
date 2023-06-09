


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

