const form = document.getElementById("inscricaoForm");

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const diasSelecionados = [];
    document.querySelectorAll('input[name="dias"]:checked').forEach(checkbox => {
        diasSelecionados.push(checkbox.value);
    });

    const necessitaIngresso = document.querySelector('input[name="ingresso"]:checked')?.value === "sim";

    const data = {
        nomeLocal: document.getElementById('nomeLocal').value,
        endereco: document.getElementById('adress').value,
        pontoRef: document.getElementById('refPoint').value,
        tipoTurismo: document.getElementById('tType').value,
        cidade: document.getElementById('city').value,
        UF: document.getElementById('UF').value,
        dias_funcionamento: diasSelecionados.join(', '),
        preco_minimo: document.querySelector('.caixaUm input[type="text"]').value || 0,
        necessita_ingresso: necessitaIngresso
    };

    try {
        const resp = await fetch("http://127.0.0.1:5000/add-inscricao", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const json = await resp.json();
        
        if (json.status === "ok") {
            alert("Inscrição enviada com sucesso!");
            form.reset();
        } else {
            alert("Erro: " + json.mensagem);
        }
    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao conectar com o servidor");
    }
});