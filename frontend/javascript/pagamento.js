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


document.querySelector('#forma_cartao').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    await processarPagamento('cartao');
});


document.querySelector('#forma_pix').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    await processarPagamento('pix');
});

async function processarPagamento(metodo) {
    const nome = document.querySelector('.caixaUm input[type="text"]').value;
    const email = document.querySelector('.caixaUm input[type="text"]:nth-child(4)').value;
    const telefone = document.querySelector('.caixaDois input[type="text"]').value;
    
    // Validar campos obrigatórios
    if (!nome || !email || !telefone) {
        alert("Por favor, preencha todos os campos obrigatórios.");
        return;
    }

    // Determinar plano e valor
    let tipo_plano = 'viajante';
    let valor = 14.90;
    
    if (window.location.search.includes('plano=explorador')) {
        tipo_plano = 'explorador';
        valor = 35.99;
    }

    const data = {
        nome: nome,
        email: email,
        telefone: telefone,
        tipo_plano: tipo_plano,
        valor: valor,
        metodo_pagamento: metodo
    };

    try {
        const resp = await fetch("http://127.0.0.1:5000/add-assinatura", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const json = await resp.json();
        
        if (json.status === "ok") {
            alert("Pagamento realizado com sucesso! Assinatura ativada.\n\nVocê pode criar uma senha posteriormente para acessar sua conta.");
            window.location.href = "index.html";
        } else {
            alert("Erro: " + json.mensagem);
        }
    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao processar pagamento");
    }
}