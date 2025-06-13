document.addEventListener('DOMContentLoaded', function() {
    // Manipulador para marcar tarefas como concluídas
    document.querySelectorAll("#taskList li").forEach(function(li) {
        li.addEventListener('click', function(e) {
            if (e.target !== this && !e.target.classList.contains('close')) return;
            if (e.target.classList.contains('close')) return;
            
            const tarefaId = this.getAttribute('data-id');
            if (!tarefaId) return;
            
            // Envia solicitação para marcar tarefa como concluída
            fetch(`/marcar_concluida/${tarefaId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.classList.toggle('checked');
                }
            })
            .catch(error => console.error('Erro ao marcar tarefa:', error));
        });
    });

    // Manipulador para excluir tarefas
    document.querySelectorAll(".close").forEach(function(span) {
        span.addEventListener('click', function(e) {
            e.stopPropagation();
            const li = this.parentElement;
            const tarefaId = li.getAttribute('data-id');
            if (!tarefaId) return;
            
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
                    li.style.opacity = '0';
                    setTimeout(() => {
                        li.remove();
                    }, 300);
                }
            })
            .catch(error => console.error('Erro ao excluir tarefa:', error));
        });
    });
});
