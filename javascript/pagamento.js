const checkbox = document.getElementById('estrangeiro');
const caixaTexto = document.getElementById('caixa_texto');

checkbox.addEventListener('change',()=>{
    if(checkbox.checked){
        caixaTexto.disabled = true;
    } else{
        caixaTexto.disabled = false;
    }
});

document.getElementById('cartao').addEventListener('click',()=>{
    const formulario = document.getElementById('forma_cartao');
    formulario.style.display='flex';

    const botao = document.getElementById('voltar');
    botao.addEventListener('click',(e)=>{
        e.preventDefault();
        formulario.style.display='none';
    });
});

document.getElementById('pix').addEventListener('click',()=>{
    const formulario = document.getElementById('forma_pix');
    formulario.style.display='flex';

    const botao = document.getElementById('voltar');
    botao.addEventListener('click',(e)=>{
        e.preventDefault();
        formulario.style.display='none';
    });
});