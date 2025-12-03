const form = document.getElementById("cadastroForm");

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        nome: document.getElementById('input_nome').value,
        email: document.getElementById('input_email').value,
        senha: document.getElementById('input_senha').value,
    };

    try {
        // Primeiro tenta vincular com assinatura existente
        const respVinculo = await fetch("http://127.0.0.1:5000/vincular-assinatura", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: data.email,
                senha: data.senha
            })
        });

        const jsonVinculo = await respVinculo.json();
        
        if (jsonVinculo.status === "ok") {

            alert("Cadastro realizado com sucesso! Sua assinatura foi vinculada à sua conta.");
            window.location.href = "index.html";
        } else {

            const respCadastro = await fetch("http://127.0.0.1:5000/add-user", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const jsonCadastro = await respCadastro.json();
            
            if (jsonCadastro.status === "ok") {
                alert("Cadastro realizado com sucesso!");
                window.location.href = "login.html";
            } else {
                alert("Erro: " + jsonCadastro.mensagem);
            }
        }
    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao conectar com o servidor");
    }
});