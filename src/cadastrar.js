/**
     * Função responsável por validar RA inserido.
     * @param {onkeydownEvent} v - Evento emitido pela função onkeydown colocada no input
     * @return {undefined}
    */
function validarRA(v) {
    var tecla = v.key;

    var num = /[0-9]/.test(tecla);
    var operador = ['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight'].includes(tecla) || (event.ctrlKey || event.metaKey) && tecla === 'a';

    var temSeteDigitos = v.target.value.length >= 7;;

    if (!num && !operador) {
        v.preventDefault();
    }

    if (num && temSeteDigitos && !operador) {
        v.preventDefault();
    }
}

/**
     * Função responsável por manipular requests na página de cadastro.
     * @param {onkeydownEvent} e - Evento emitido pela função onsubmit colocada no form
     * @return {undefined}
    */
function cadastrar(e) {
    e.preventDefault()
    document.querySelector('.loader').style.display = 'inline-grid';

    var formData = new FormData();
    formData.append('nome', document.getElementById('nome').value);
    formData.append('ra', document.getElementById('ra').value);
    formData.append('sala', document.getElementById('sala').value);

    fetch('/cadastrar', {
        method: 'POST',
        body: formData
    })
    .then(response => {})
    .then(data => {
        // document.getElementById('loading').style.display = 'none';
        console.log('Resposta da API:', data);
    })
    .catch(error => {
        // document.getElementById('loading').style.display = 'none';

        console.error('Erro:', error);
    });
}