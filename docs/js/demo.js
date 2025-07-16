// Script para interatividade da demo
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se a imagem da demo carregou corretamente
    const demoImage = document.querySelector('.hero-image img');
    if (demoImage) {
        // Verificar se a imagem carregou
        if (demoImage.complete) {
            console.log('Imagem carregada com sucesso!');
        } else {
            demoImage.addEventListener('error', function() {
                console.error('Erro ao carregar a imagem demo');
                this.src = 'https://via.placeholder.com/800x450?text=TaskPro+Demo';
            });
            
            demoImage.addEventListener('load', function() {
                console.log('Imagem carregada com sucesso!');
            });
        }
    }
    
    // Adicionar botão de fallback se a imagem não carregar após 3 segundos
    setTimeout(function() {
        const heroImage = document.querySelector('.hero-image');
        const img = heroImage.querySelector('img');
        if (img && !img.complete) {
            const fallbackBtn = document.createElement('button');
            fallbackBtn.textContent = 'Recarregar imagem';
            fallbackBtn.className = 'btn';
            fallbackBtn.style.marginTop = '10px';
            fallbackBtn.addEventListener('click', function() {
                img.src = './images/taskpro-demo.png?v=' + new Date().getTime();
            });
            heroImage.appendChild(fallbackBtn);
        }
    }, 3000);
    // Interatividade dos checkboxes na demo
    const checkboxes = document.querySelectorAll('.task-item input[type="checkbox"]');
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const taskItem = this.closest('.task-item');
            if (this.checked) {
                taskItem.classList.add('completed');
            } else {
                taskItem.classList.remove('completed');
            }
        });
    });

    // Animação suave de scroll para links internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Simulação de login demo (apenas alerta)
    const loginBtn = document.querySelector('.login-btn');
    if (loginBtn) {
        loginBtn.addEventListener('click', function() {
            alert('Esta é uma versão demo estática do TaskPro.\n\nPara experimentar todas as funcionalidades, clone o repositório do GitHub e execute a aplicação localmente.');
        });
    }
});
