const btn = document.getElementById('git');
const githubUrl = 'https://github.com/petrakiio';

btn.addEventListener('click', () => {
    window.open(githubUrl, '_blank', 'noopener,noreferrer');
});