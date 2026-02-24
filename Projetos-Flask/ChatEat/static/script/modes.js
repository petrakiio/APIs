const btn = document.getElementById('btn')
const container = document.querySelector('.container')
btn.textContent= 'Modo Escuro'

btn.addEventListener('click', () =>{
    container.classList.toggle('dark-mode')
    btn.textContent='Modo Claro'
})