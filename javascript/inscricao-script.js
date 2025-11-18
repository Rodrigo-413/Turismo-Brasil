const form = document.getElementById("inscricaoForm");

form.addEventListener('submit', function(event) {

  event.preventDefault();

  const endereco = document.getElementById('adress').value;
  const pontoRef = document.getElementById('refPoint').value;
  const tipoTurismo = document.getElementById('tType').value;
  const cidade = document.getElementById('city').value;
  const UF = document.getElementById('UF').value;

});
