const form = document.getElementById('search-form');
const input = document.getElementById('search-input');
const resultBox = document.getElementById('search-result');

if (form) form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const q = input.value.trim();
    if (!q) {
        resultBox.textContent = 'Digite um nome para pesquisar.';
        return;
    }

    try {
        const res = await fetch(`/search_books?q=${encodeURIComponent(q)}`);
        const data = await res.json();

        if (!data || Object.keys(data).length === 0) {
            resultBox.textContent = 'Nenhum livro encontrado.';
            return;
        }

        resultBox.innerHTML = `
            <div class="result-card">
                <div><strong>ID:</strong> ${data.id_livro}</div>
                <div><strong>Título:</strong> ${data.titulo}</div>
                <div><strong>Autor:</strong> ${data.autor}</div>
                <div><strong>Editora:</strong> ${data.editora ?? '-'}</div>
                <div><strong>Ano:</strong> ${data.ano_publicacao ?? '-'}</div>
                <div><strong>ISBN:</strong> ${data.isbn ?? '-'}</div>
                <div><strong>Categoria:</strong> ${data.categoria ?? '-'}</div>
                <div><strong>Total:</strong> ${data.total_unidades}</div>
                <div><strong>Disponíveis:</strong> ${data.unidades_disponiveis}</div>
            </div>
        `;
    } catch (err) {
        resultBox.textContent = 'Erro ao buscar livros.';
    }
});

// social links
const linkedinLink = document.getElementById('linkedin');
const githubLink = document.getElementById('git');

if (linkedinLink) {
    linkedinLink.addEventListener('click', (e) => {
        const hrefAttr = linkedinLink.getAttribute('href');
        if (!hrefAttr) {
            e.preventDefault();
            window.open('https://www.linkedin.com/in/petrakiio/', '_blank');
        }
    });
}

if (githubLink) {
    githubLink.addEventListener('click', (e) => {
        const hrefAttr = githubLink.getAttribute('href');
        if (!hrefAttr) {
            e.preventDefault();
            window.open('https://github.com/petrakiio', '_blank');
        }
    });
}
