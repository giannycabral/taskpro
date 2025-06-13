document.addEventListener('DOMContentLoaded', function() {
    // Adiciona classes para efeitos de entrada nos elementos principais
    const container = document.querySelector('.container');
    const header = document.querySelector('.header');
    const sections = document.querySelectorAll('.category-section');
    
    if (container) {
        container.classList.add('fade-in');
    }
    
    if (header) {
        setTimeout(() => {
            header.classList.add('slide-in');
        }, 100);
    }
    
    // Adiciona animação sequencial para as seções de categorias
    if (sections.length > 0) {
        sections.forEach((section, index) => {
            setTimeout(() => {
                section.classList.add('fade-in');
            }, 200 + (index * 100));
        });
    }

    // Manipulador para marcar tarefas como concluídas com efeito visual
    document.querySelectorAll('li[data-id]').forEach(function(li) {
        li.addEventListener('click', function(e) {
            if (e.target !== this && !e.target.classList.contains('task-content')) return;
            if (e.target.classList.contains('close')) return;
            
            const tarefaId = this.getAttribute('data-id');
            if (!tarefaId) return;
            
            // Adiciona efeito visual antes do envio da requisição
            this.classList.add('processing');
            
            // Envia solicitação para marcar tarefa como concluída
            fetch(`/marcar_concluida/${tarefaId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                // Remove o efeito de processamento
                this.classList.remove('processing');
                
                if (data.success) {
                    // Adiciona efeito de toggle com animação
                    const wasChecked = this.classList.contains('checked');
                    
                    if (!wasChecked) {
                        // Adicionando classe checked com animação
                        this.classList.add('task-completing');
                        setTimeout(() => {
                            this.classList.add('checked');
                            this.classList.remove('task-completing');
                        }, 300);
                    } else {
                        // Removendo classe checked com animação
                        this.classList.add('task-uncompleting');
                        setTimeout(() => {
                            this.classList.remove('checked');
                            this.classList.remove('task-uncompleting');
                        }, 300);
                    }
                }
            })
            .catch(error => {
                console.error('Erro ao marcar tarefa:', error);
                this.classList.remove('processing');
                
                // Feedback visual de erro
                this.classList.add('error-shake');
                setTimeout(() => {
                    this.classList.remove('error-shake');
                }, 500);
            });
        });
    });

    // Manipulador para excluir tarefas com animação suave
    document.querySelectorAll(".close").forEach(function(span) {
        span.addEventListener('click', function(e) {
            e.stopPropagation();
            const li = this.parentElement;
            const tarefaId = li.getAttribute('data-id');
            if (!tarefaId) return;
            
            // Feedback visual de início de exclusão
            span.classList.add('deleting');
            li.classList.add('deleting-item');
            
            // Envia solicitação para excluir tarefa
            fetch(`/excluir/${tarefaId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Animação de saída mais suave
                    li.style.height = li.offsetHeight + 'px';
                    setTimeout(() => {
                        li.style.height = '0';
                        li.style.opacity = '0';
                        li.style.marginTop = '0';
                        li.style.marginBottom = '0';
                        li.style.padding = '0';
                    }, 50);
                    
                    setTimeout(() => {
                        li.remove();
                    }, 350);
                } else {
                    // Restaura estado caso a exclusão falhe
                    span.classList.remove('deleting');
                    li.classList.remove('deleting-item');
                    
                    // Feedback visual de erro
                    li.classList.add('error-shake');
                    setTimeout(() => {
                        li.classList.remove('error-shake');
                    }, 500);
                }
            })
            .catch(error => {
                console.error('Erro ao excluir tarefa:', error);
                // Restaura estado visual caso haja erro
                span.classList.remove('deleting');
                li.classList.remove('deleting-item');
            });
        });
    });
    
    // Detecta flash messages e adiciona animação de saída automática
    const flashMessages = document.querySelectorAll('.flash');
    if (flashMessages.length > 0) {
        flashMessages.forEach(message => {
            setTimeout(() => {
                message.style.opacity = '0';
                message.style.transform = 'translateY(-10px)';
                setTimeout(() => {
                    message.remove();
                }, 500);
            }, 5000);
        });
    }
});
