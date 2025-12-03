const form = document.getElementById("loginForm");

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        email: document.getElementById('email').value,
        senha: document.getElementById('password').value
    };

    try {
        const resp = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const json = await resp.json();
        
        if (json.status === "ok") {
            alert("Login realizado com sucesso!");
            // Redireciona para a página inicial após login
            window.location.href = "index.html";
        } else {
            alert("Erro: " + json.mensagem);
        }
    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao conectar com o servidor");
    }
});