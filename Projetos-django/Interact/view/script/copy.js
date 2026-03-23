const copyButtons = document.querySelectorAll('.copy-btn');
        copyButtons.forEach((btn) => {
            btn.addEventListener('click', async () => {
                const targetId = btn.getAttribute('data-copy-target');
                const target = document.getElementById(targetId);
                if (!target) return;
                const text = target.textContent.trim();
                try {
                    await navigator.clipboard.writeText(text);
                    btn.textContent = 'Copiado!';
                } catch (err) {
                    btn.textContent = 'Falhou';
                }
                setTimeout(() => {
                    btn.textContent = 'Copiar';
                }, 1400);
            });
        });