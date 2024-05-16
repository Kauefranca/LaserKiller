function updateClock() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    const dayOfWeek = new Intl.DateTimeFormat('pt-BR', { weekday: 'long' }).format(now);
    const month = new Intl.DateTimeFormat('pt-BR', { month: 'long' }).format(now);
    const year = now.getFullYear();  
    const timeString = `${hours}:${minutes}:${seconds}`;
    const dateString = `${dayOfWeek}, ${now.getDate()} de ${month} de ${year}`;
    document.getElementById('clock-hours').textContent = timeString;
    document.getElementById('clock-date').textContent = dateString;
};

setInterval(updateClock, 1000);
updateClock();

function renderChart(id, descricao, data, options) {
    var graficoContainer = document.getElementById('grafico-container');
    
    var div = document.createElement('div');
    div.classList.add('chart-container');
    
    var canvas = document.createElement('canvas');
    canvas.id = id;

    var p = document.createElement('p');
    p.classList.add('chart-description');
    p.innerHTML = descricao;

    div.appendChild(canvas);
    div.appendChild(p);
    graficoContainer.appendChild(div);

    var ctx = document.getElementById(id).getContext('2d');
    return new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: options,
    });
};

document.addEventListener("DOMContentLoaded", () => {
    const charts = [
        {
            id: 'grafico1',
            texto: 'Lorem ipsum dolor sit amet consectetur, adipisicing elit...',
            data: {
                labels: ["Presente", "Ausente"],
                datasets: [{ data: [28, 4], backgroundColor: ["#0071BB", "#FFF"] }],
            },
            opcoes: {
                responsive: false,
                maintainAspectRatio: false,
                cutout: "85%",
                legend: { display: true, position: "bottom"}
            },
        },
        {
            id: 'grafico2',
            texto: 'Lorem ipsum dolor sit amet consectetur, adipisicing elit...',
            data: {
                labels: ["Presente", "Ausente"],
                datasets: [{ data: [28, 4], backgroundColor: ["#0071BB", "#FFF"] }],
            },
            opcoes: {
                responsive: false,
                maintainAspectRatio: false,
                cutout: "85%",
                legend: { display: true, position: "bottom" },
            },
        },
        {
            id: 'grafico3',
            texto: 'Lorem ipsum dolor sit amet consectetur, adipisicing elit...',
            data: {
                labels: ["Presente", "Ausente"],
                datasets: [{data: [28, 4], backgroundColor: ["#0071BB", "#FFF"]}],
            },
            opcoes: {
                responsive: false,
                maintainAspectRatio: false,
                cutout: "85%",
                legend: { display: true, position: "bottom"}
            },
        },
    ];

    for (let chart of charts) {
        renderChart(chart.id, chart.texto, chart.data, chart.opcoes);
    };
});

var start_button = document.querySelector('button#start');
start_button.addEventListener("click", start_aula);
var end_button = document.querySelector('button#end');
end_button.addEventListener("click", end_aula);

function start_aula() {
    Swal.fire({
        position: "top",
        icon: "success",
        title: "Aula iniciada!",
        showConfirmButton: false,
        timer: 1300
    });

    start_button.setAttribute('disabled', true);
    end_button.removeAttribute('disabled');

    fetch('http://' + document.domain + ':' + location.port + '/start_aula', {
        method: 'POST'
    });
};

function end_aula() {
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: "btn btn-success",
            cancelButton: "btn btn-danger"
        },
        buttonsStyling: false
    });

    swalWithBootstrapButtons.fire({
        title: "Encerrar aula",
        text: "Deseja encerrar a aula?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sim",
        cancelButtonText: "Não",
        reverseButtons: true
    })
    .then((result) => {
        if (result.isConfirmed) {
            swalWithBootstrapButtons.fire({
            title: "Aula encerrada!",
            text: "A aula foi encerrada com sucesso",
            icon: "success"
        });
            end_button.setAttribute('disabled', true);
            start_button.removeAttribute('disabled')

            fetch('http://' + document.domain + ':' + location.port + '/end_aula', {
                method: 'POST'
            });
        }
    });
}