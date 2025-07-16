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
    
    // Configurar o sistema de notificações
    setupNotificationSystem();
    
    // Adiciona animações sutis para melhorar a experiência do usuário
    animateElements();
    
    // Configurar o sistema de compartilhamento
    setupSharingSystem();
});

// Função para alternar o status da tarefa (concluída/pendente)
function toggleTaskStatus(taskId, element) {
    // Usar a URL definida no template HTML
    const url = typeof ROTAS !== 'undefined' ? 
        `${ROTAS.marcar_concluida}/${taskId}` : 
        `/tarefas/marcar_concluida/${taskId}`;
        
    console.log("Tentando alternar status da tarefa:", url);
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Alternar classe checked
            if (data.concluida) {
                element.classList.add('checked');
            } else {
                element.classList.remove('checked');
            }
            
            // Atualizar ícone do botão de toggle
            const toggleBtn = element.querySelector('.btn-toggle .toggle-icon');
            if (toggleBtn) {
                toggleBtn.textContent = data.concluida ? '↩️' : '✓';
            }
            
            // Atualizar título do botão
            const toggleLink = element.querySelector('.btn-toggle');
            if (toggleLink) {
                toggleLink.title = data.concluida ? 'Marcar como pendente' : 'Marcar como concluída';
            }
            
            // Mostrar mensagem de sucesso
            const flashContainer = document.querySelector('.flash-messages');
            if (flashContainer) {
                const flashMessage = document.createElement('div');
                flashMessage.className = 'flash sucesso';
                flashMessage.textContent = data.concluida ? 'Tarefa concluída!' : 'Tarefa reaberta como pendente!';
                flashContainer.appendChild(flashMessage);
                
                // Remover mensagem após alguns segundos
                setTimeout(() => {
                    flashMessage.style.opacity = '0';
                    setTimeout(() => flashMessage.remove(), 500);
                }, 3000);
            }
        }
    })
    .catch(error => {
        console.error('Erro ao atualizar status da tarefa:', error);
    });
}

// Função para excluir uma tarefa
function deleteTask(taskId, element) {
    if (confirm('Tem certeza que deseja excluir esta tarefa? Esta ação não pode ser desfeita.')) {
        // Usar a URL definida no template HTML
        const url = typeof ROTAS !== 'undefined' ? 
            `${ROTAS.excluir_tarefa}/${taskId}` : 
            `/tarefas/excluir/${taskId}`;
        
        console.log("Tentando excluir tarefa:", url);
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Adicionar classe para animar a remoção
                element.classList.add('removing');
                
                setTimeout(() => {
                    element.remove();
                    
                    // Verifica se a categoria ficou vazia
                    const categorySection = element.closest('.category-section');
                    if (categorySection) {
                        const remainingTasks = categorySection.querySelectorAll('li[data-id]');
                        
                        if (remainingTasks.length === 0) {
                            const emptyMessage = document.createElement('li');
                            emptyMessage.textContent = 'Nenhuma tarefa nesta categoria';
                            categorySection.querySelector('ul').appendChild(emptyMessage);
                        }
                    }
                    
                    // Mostrar mensagem de sucesso
                    const flashContainer = document.querySelector('.flash-messages');
                    if (flashContainer) {
                        const flashMessage = document.createElement('div');
                        flashMessage.className = 'flash sucesso';
                        flashMessage.textContent = 'Tarefa excluída com sucesso!';
                        flashContainer.appendChild(flashMessage);
                        
                        // Remover mensagem após alguns segundos
                        setTimeout(() => {
                            flashMessage.style.opacity = '0';
                            setTimeout(() => flashMessage.remove(), 500);
                        }, 3000);
                    }
                }, 300);
            } else {
                alert('Ocorreu um erro ao excluir a tarefa. Por favor, tente novamente.');
            }
        })
        .catch(error => {
            console.error('Erro ao excluir tarefa:', error);
            alert('Ocorreu um erro ao excluir a tarefa. Por favor, tente novamente.');
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

// Função para configurar o sistema de notificações
function setupNotificationSystem() {
    // Elementos DOM
    const notificationBell = document.querySelector('.notification-bell');
    const notificationCount = document.getElementById('notificationCount');
    const notificationsArea = document.getElementById('notificationsArea');
    const closeNotifications = document.getElementById('closeNotifications');
    const notificationList = document.getElementById('notificationList');
    
    // Verifica se estamos na página que possui os elementos de notificação
    // Se não encontrarmos os elementos necessários, saímos da função
    if (!notificationBell || !notificationCount || !notificationsArea) {
        console.log('Elementos de notificação não encontrados na página atual');
        return;
    }
    
    // Variável para armazenar as notificações
    let notifications = [];
    
    // Verifica tarefas próximas ao vencimento ou vencidas
    checkDueTasks();
    
    // Alterna a visibilidade da área de notificações
    notificationBell.addEventListener('click', function() {
        notificationsArea.classList.toggle('show');
        if (notificationsArea.classList.contains('show')) {
            // Marca as notificações como lidas
            notificationBell.classList.remove('has-new');
        }
    });
    
    // Fecha o painel de notificações
    if (closeNotifications) {
        closeNotifications.addEventListener('click', function() {
            notificationsArea.classList.remove('show');
        });
    }
    
    // Clique fora da área de notificações fecha o painel
    document.addEventListener('click', function(event) {
        if (!notificationsArea.contains(event.target) && 
            !notificationBell.contains(event.target) && 
            notificationsArea.classList.contains('show')) {
            notificationsArea.classList.remove('show');
        }
    });
    
    // Função para verificar tarefas próximas ao vencimento ou vencidas
    function checkDueTasks() {
        let count = 0;
        notifications = [];
        
        // Procura todas as tarefas com classes de vencimento
        const proximasTasks = document.querySelectorAll('li.proxima:not(.checked)');
        const vencidasTasks = document.querySelectorAll('li.vencida:not(.checked)');
        
        // Adiciona tarefas próximas às notificações
        proximasTasks.forEach(task => {
            const taskContent = task.querySelector('.task-content');
            const taskMeta = task.querySelector('.task-meta');
            
            if (taskContent) {
                count++;
                
                const taskText = taskContent.childNodes[0].textContent.trim();
                const dueDate = taskMeta ? taskMeta.textContent.replace('Vence em:', '').trim() : 'Em breve';
                
                notifications.push({
                    id: task.dataset.id,
                    title: 'Tarefa próxima do vencimento',
                    message: taskText,
                    date: dueDate,
                    type: 'proxima',
                    element: task
                });
            }
        });
        
        // Adiciona tarefas vencidas às notificações
        vencidasTasks.forEach(task => {
            const taskContent = task.querySelector('.task-content');
            const taskMeta = task.querySelector('.task-meta');
            
            if (taskContent) {
                count++;
                
                const taskText = taskContent.childNodes[0].textContent.trim();
                const dueDate = taskMeta ? taskMeta.textContent.replace('Vence em:', '').trim() : 'Vencida';
                
                notifications.push({
                    id: task.dataset.id,
                    title: 'Tarefa vencida!',
                    message: taskText,
                    date: dueDate,
                    type: 'vencida',
                    element: task
                });
            }
        });
        
        // Atualiza a contagem de notificações
        updateNotificationCount(count);
        
        // Renderiza as notificações
        renderNotifications();
        
        // Adiciona classe especial se houver notificações
        if (count > 0 && notificationBell) {
            notificationBell.classList.add('has-new');
        }
    }
    
    // Atualiza o contador de notificações
    function updateNotificationCount(count) {
        if (notificationCount) {
            notificationCount.textContent = count > 0 ? count : '';
        }
    }
    
    // Renderiza as notificações na área de notificações
    function renderNotifications() {
        // Verifica se o elemento existe
        if (!notificationList) return;
        
        // Limpa a lista de notificações
        notificationList.innerHTML = '';
        
        if (notifications.length === 0) {
            const emptyNotification = document.createElement('div');
            emptyNotification.className = 'notification-item';
            emptyNotification.innerHTML = `
                <div class="notification-content">
                    <div class="notification-message">Não há notificações no momento.</div>
                </div>
            `;
            notificationList.appendChild(emptyNotification);
            return;
        }
        
        // Adiciona cada notificação à lista
        notifications.forEach(notification => {
            const notificationItem = document.createElement('div');
            notificationItem.className = `notification-item notification-${notification.type}`;
            notificationItem.dataset.id = notification.id;
            
            let icon = '⏰';
            if (notification.type === 'vencida') {
                icon = '⚠️';
            }
            
            notificationItem.innerHTML = `
                <div class="notification-icon">${icon}</div>
                <div class="notification-content">
                    <div class="notification-title">${notification.title}</div>
                    <div class="notification-message">${notification.message}</div>
                    <div class="notification-time">${notification.date}</div>
                </div>
            `;
            
            // Adiciona evento de clique na notificação para ir até a tarefa
            notificationItem.addEventListener('click', function() {
                // Fecha o painel de notificações
                notificationsArea.classList.remove('show');
                
                // Scroll até a tarefa e destaca-a
                const taskElement = notification.element;
                if (taskElement) {
                    // Remove destaques anteriores
                    document.querySelectorAll('.highlight-task').forEach(el => {
                        el.classList.remove('highlight-task');
                    });
                    
                    // Adiciona destaque à tarefa
                    taskElement.classList.add('highlight-task');
                    
                    // Scroll até a tarefa com animação suave
                    taskElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            });
            
            notificationList.appendChild(notificationItem);
        });
    }
    
    // Recarrega as notificações a cada 30 segundos
    setInterval(checkDueTasks, 30000);
}

// Função para gerenciar o sistema de compartilhamento
function setupSharingSystem() {
    // Verificar se estamos na página de tarefas compartilhadas
    const sharedTasksList = document.querySelector('.shared-tasks');
    if (sharedTasksList) {
        // Adicionar funcionalidade para visualizar detalhes de tarefas compartilhadas
        document.querySelectorAll('.shared-task-item').forEach(item => {
            item.addEventListener('click', function(e) {
                // Ignora se o clique foi em um botão ou link
                if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON') {
                    return;
                }
                
                // Alterna a classe expanded para mostrar/ocultar detalhes completos
                this.classList.toggle('expanded');
            });
        });
    }
    
    // Verificar se estamos na página de compartilhar tarefa
    const shareForm = document.querySelector('.share-form');
    if (shareForm) {
        // Adicionar validação ao formulário de compartilhamento
        shareForm.addEventListener('submit', function(e) {
            const emailInput = document.getElementById('email');
            if (!emailInput.value || !emailInput.value.includes('@')) {
                e.preventDefault();
                alert('Por favor, insira um email válido para compartilhar a tarefa.');
            }
        });
        
        // Adicionar exibição prévia do compartilhamento
        const emailInput = document.getElementById('email');
        const permissionCheckbox = document.getElementById('permissao_edicao');
        const previewContainer = document.createElement('div');
        previewContainer.className = 'share-preview';
        previewContainer.style.display = 'none';
        
        if (emailInput && permissionCheckbox) {
            const updatePreview = function() {
                if (emailInput.value && emailInput.value.includes('@')) {
                    const permissionText = permissionCheckbox.checked ? 'poderá editar esta tarefa' : 'apenas poderá visualizar esta tarefa';
                    previewContainer.innerHTML = `
                        <div class="preview-content">
                            <strong>${emailInput.value}</strong> ${permissionText}.
                        </div>
                    `;
                    previewContainer.style.display = 'block';
                } else {
                    previewContainer.style.display = 'none';
                }
            };
            
            emailInput.addEventListener('input', updatePreview);
            permissionCheckbox.addEventListener('change', updatePreview);
            
            // Inserir a prévia após o último form-group
            const formGroups = document.querySelectorAll('.form-group');
            if (formGroups.length) {
                formGroups[formGroups.length - 1].after(previewContainer);
            }
        }
    }
    
    // Se houver um botão de compartilhamento na página principal
    document.querySelectorAll('.btn-share').forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Evita a propagação do clique para não marcar a tarefa como concluída
            e.stopPropagation();
        });
    });
}
