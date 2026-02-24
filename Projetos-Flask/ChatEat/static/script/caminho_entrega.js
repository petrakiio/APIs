const entregador = document.getElementById('entregador');
const etaElement = document.getElementById('eta');
const statusText = document.getElementById('status-text');

const steps = [
    { left: 12, top: 70, eta: 24, text: 'Entregador saiu da loja' },
    { left: 28, top: 62, eta: 18, text: 'Passando pela Av. Central' },
    { left: 44, top: 56, eta: 13, text: 'Pedido no bairro da entrega' },
    { left: 62, top: 50, eta: 8, text: 'A poucas quadras de voce' },
    { left: 78, top: 44, eta: 4, text: 'Entregador chegando no endereco' },
    { left: 88, top: 38, eta: 1, text: 'Entregador na sua porta' }
];

let index = 0;

function renderStep(step) {
    entregador.style.left = step.left + '%';
    entregador.style.top = step.top + '%';
    etaElement.textContent = step.eta;
    statusText.textContent = step.text;
}

renderStep(steps[index]);

const interval = setInterval(() => {
    index += 1;
    if (index >= steps.length) {
        clearInterval(interval);
        return;
    }
    renderStep(steps[index]);
}, 4000);
