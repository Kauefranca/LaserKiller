/**
     * Função responsável por gerar cards de forma dinâmica.
     * @param {string} name - Nome do card
     * @param {string} path - Rota de destino do card
     * @param {string} imgPath - Caminho da imagem do card
     * @param {array} color - Lista com cores do card
     * @return {undefined}
    */
function createCard(name, path, imgPath, colors) {
    var cardContainer = document.createElement('a');
    cardContainer.href = path;

    var card = document.createElement('div');
    card.classList.add('cartao');
    card.style = colors[0] ? `background-color: ${colors[0]};` : '';
    cardContainer.appendChild(card);

    var cardText = document.createElement('div');
    cardText.classList.add('card-text');
    
    var h3 = document.createElement('h3');
    h3.innerHTML = name;
    h3.style = colors[1] && colors[2] ? `background-color: ${colors[1]}; color: ${colors[2]};` : '';
    cardText.appendChild(h3);

    var p = document.createElement('p');
    cardText.appendChild(p);

    var br = document.createElement('br');
    cardText.appendChild(br);

    var cardAcessar = document.createElement('div');
    cardAcessar.classList.add('card-acessar');

    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    svg.setAttribute("width", "42");
    svg.setAttribute("height", "42");
    svg.setAttribute("viewBox", "0 0 42 42");
    svg.setAttribute("fill", "none");

    var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", "21");
    circle.setAttribute("cy", "21");
    circle.setAttribute("r", "20.5");
    circle.setAttribute("fill", colors[3] ? colors[3] : '#000');

    var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", "M11.75 25.201C11.0326 25.6152 10.7867 26.5326 11.201 27.25C11.6152 27.9674 12.5326 28.2133 13.25 27.799L11.75 25.201ZM31.2694 16.8882C31.4838 16.088 31.0089 15.2655 30.2087 15.0511L17.1687 11.5571C16.3685 11.3426 15.546 11.8175 15.3316 12.6177C15.1172 13.4179 15.5921 14.2404 16.3923 14.4548L27.9834 17.5607L24.8776 29.1518C24.6631 29.952 25.138 30.7745 25.9382 30.9889C26.7384 31.2033 27.5609 30.7284 27.7753 29.9282L31.2694 16.8882ZM13.25 27.799L30.5705 17.799L29.0705 15.201L11.75 25.201L13.25 27.799Z");
    path.setAttribute("fill", colors[5] ? colors[5] : '#0071BB');

    svg.appendChild(circle);
    svg.appendChild(path);
    cardAcessar.appendChild(svg);
    
    var acessarText = document.createElement('div');
    acessarText.classList.add('acessar');
    acessarText.innerHTML = 'Acessar';
    acessarText.style = colors[4] ? `color: ${colors[4]};` : '';
    cardAcessar.appendChild(acessarText);
    
    card.appendChild(cardText);
    
    cardText.appendChild(cardAcessar);

    var imgDiv = document.createElement('div');
    imgDiv.classList.add('card-img');

    var img = document.createElement('img');
    img.src = imgPath;

    imgDiv.appendChild(img);
    card.appendChild(imgDiv);

    document.querySelector('.card-container').appendChild(cardContainer);
    return;
}
const AplicationsList = [
    {
        name: 'Reconhecimento',
        path: '/reconhecimento',
        imgPath: '/static/img/reconhecimento.png',
        colors: []
    },
    {
        name: 'Cadastrar',
        path: '/cadastrar',
        imgPath: '/static/img/cadastrar.png',
        colors: ['#0071BB', '#FFF', '#000', '#FFF', '#FFF']
    },
    {
        name: 'Treinamento',
        path: '/treinamento',
        imgPath: '/static/img/treinamento.png',
        bgColor: '#191A23',
        colors: ['#191A23', '#FFF', '#000', '#0071BB', '#FFF', '#FFF']
    },
    {
        name: 'Relatórios',
        path: '/relatorio',
        imgPath: '/static/img/relatorio.png',
        colors: []
    },
];

for (let application of AplicationsList) {
    createCard(application.name, application.path, application.imgPath, application.colors);
};