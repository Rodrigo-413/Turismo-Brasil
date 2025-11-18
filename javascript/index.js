function irParaPagina() {
            const pagina = document.getElementById("pagina");
            const url = pagina.value;
            if (url) {
                window.location.href = url;
            }
        }