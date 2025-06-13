/**
 * TaskPro - JavaScript para a página principal
 */

document.addEventListener('DOMContentLoaded', function() {
    // Adicionar funcionalidade para marcar tarefas como concluídas
    document.querySelectorAll('li[data-id]').forEach(item => {
        // Adiciona listener de clique no conteúdo da tarefa
        const taskContent = item.querySelector('.task-content');
        if (taskContent) {
            taskContent.addEventListener('click', function() {
                const taskId = item.dataset.id;
                toggleTaskStatus(taskId, item);
            });
        }
        
        // Adiciona listener para o botão de fechar (excluir tarefa)
        const closeBtn = item.querySelector('.close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                const taskId = item.dataset.id;
                deleteTask(taskId, item);
            });
        }
    });
    
    // Adiciona animações sutis para melhorar a experiência do usuário
    animateElements();
});

// Função para alternar o status da tarefa (concluída/pendente)
function toggleTaskStatus(taskId, element) {
    fetch(`/marcar_concluida/${taskId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.concluida) {
                element.classList.add('checked');
            } else {
                element.classList.remove('checked');
            }
        }
    })
    .catch(error => {
        console.error('Erro ao atualizar status da tarefa:', error);
    });
}

// Função para excluir uma tarefa
function deleteTask(taskId, element) {
    if (confirm('Tem certeza que deseja excluir esta tarefa?')) {
        fetch(`/excluir/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Animação suave de saída antes de remover
                element.style.opacity = '0';
                element.style.transform = 'translateY(-10px)';
                element.style.transition = 'all 0.3s ease';
                
                setTimeout(() => {
                    element.remove();
                    
                    // Verifica se a categoria ficou vazia
                    const categorySection = element.closest('.category-section');
                    const remainingTasks = categorySection.querySelectorAll('li[data-id]');
                    
                    if (remainingTasks.length === 0) {
                        const emptyMessage = document.createElement('li');
                        emptyMessage.textContent = 'Nenhuma tarefa nesta categoria';
                        categorySection.querySelector('ul').appendChild(emptyMessage);
                    }
                }, 300);
            }
        })
        .catch(error => {
            console.error('Erro ao excluir tarefa:', error);
        });
    }
}

// Função para adicionar animações aos elementos da interface
function animateElements() {
    // Animação para o cabeçalho
    const header = document.querySelector('.header');
    if (header) {
        header.classList.add('slide-in');
    }
    
    // Animação para as categorias
    const categories = document.querySelectorAll('.category-section');
    if (categories.length) {
        categories.forEach((category, index) => {
            setTimeout(() => {
                category.style.opacity = '0';
                category.style.transform = 'translateY(20px)';
                category.style.transition = 'all 0.5s ease';
                
                setTimeout(() => {
                    category.style.opacity = '1';
                    category.style.transform = 'translateY(0)';
                }, 50);
            }, index * 100); // Atraso escalonado para cada categoria
        });
    }
    
    // Animação para os formulários
    const forms = document.querySelectorAll('form');
    if (forms.length) {
        forms.forEach(form => {
            form.classList.add('fade-in');
        });
    }
    
    // Animação para tarefas
    const tasks = document.querySelectorAll('li[data-id]');
    if (tasks.length) {
        tasks.forEach((task, index) => {
            task.style.opacity = '0';
            task.style.transform = 'translateX(-10px)';
            task.style.transition = 'all 0.3s ease';
            
            setTimeout(() => {
                task.style.opacity = '1';
                task.style.transform = 'translateX(0)';
            }, index * 50); // Atraso escalonado para cada tarefa
        });
    }
}

// Adiciona um sutil efeito de hover às tarefas
document.addEventListener('mouseover', function(e) {
    if (e.target.closest('li[data-id]')) {
        const task = e.target.closest('li[data-id]');
        task.style.boxShadow = '0 4px 8px rgba(123, 104, 238, 0.15)';
    }
});

document.addEventListener('mouseout', function(e) {
    if (e.target.closest('li[data-id]')) {
        const task = e.target.closest('li[data-id]');
        task.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.05)';
    }
});
