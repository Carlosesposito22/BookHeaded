function adicionarOpcao() {
    const opcoesContainer = document.getElementById('opcoesContainer');
    const novaOpcao = document.createElement('div');
    novaOpcao.classList.add('input-group', 'mb-2');
    novaOpcao.innerHTML = `
        <input type="text" class="form-control" name="opcoes" id="opcoes1" placeholder="New Option" required>
        <button type="button" class="btn btn-outline-danger" onclick="removerOpcao(this)">-</button>
    `;
    opcoesContainer.appendChild(novaOpcao);
}

function removerOpcao(button) {
    button.parentElement.remove();
}

function votarNaOpcao(enqueteId, opcaoId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/votar/${enqueteId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ 'opcao_id': opcaoId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            const votosContador = document.querySelector(`#votos-contador-${opcaoId}`);
            votosContador.textContent = parseInt(votosContador.textContent) + 1;
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Erro ao registrar o voto:', error);
    });
}

function toggleEnqueteDetails(enqueteId) {
    document.querySelectorAll('.enquete-details').forEach(element => {
        if (element.getAttribute('id') !== `enqueteDetails-${enqueteId}`) {
            element.classList.remove('show');
        }
    });

    const details = document.getElementById(`enqueteDetails-${enqueteId}`);
    details.classList.toggle('show');
}

function votarEnquete(event, enqueteId) {
    event.preventDefault();
    const form = document.getElementById(`votacaoForm-${enqueteId}`);
    const opcaoSelecionada = form.querySelector('input[name="opcao_id"]:checked');
    const mensagemContainer = document.getElementById(`votacaoMensagem-${enqueteId}`);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (!opcaoSelecionada) {
        mensagemContainer.innerHTML = `<div class="alert alert-danger">Por favor, selecione uma opção para votar.</div>`;
        return;
    }

    const opcaoId = opcaoSelecionada.value;

    fetch(`/votar/${enqueteId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ 'opcao_id': opcaoId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mensagemContainer.innerHTML = `<div class="alert alert-success">Voto registrado com sucesso!</div>`;
            form.style.display = 'none';
            setTimeout(() => location.reload(), 1500);
        } else {
            mensagemContainer.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
        }
    })
    .catch(error => {
        console.error('Erro ao votar:', error);
        mensagemContainer.innerHTML = `<div class="alert alert-danger">Ocorreu um erro. Tente novamente.</div>`;
    });
}

document.getElementById('listarResultadosEnquetes').addEventListener('click', function() {
    const clubeId = this.getAttribute('data-clube-id');
    fetchResultadosEnquetes(clubeId);
});

function fetchResultadosEnquetes(clubeId) {
    fetch(`/clube/${clubeId}/resultados_enquetes/`)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('resultadosContainer');
            container.innerHTML = '';

            if (data.success) {
                data.enquetes.forEach(enquete => {
                    const enqueteTitle = document.createElement('button');
                    enqueteTitle.classList.add('btn', 'btn-outline-primary', 'mb-2', 'w-100');
                    enqueteTitle.textContent = enquete.titulo;
                    enqueteTitle.setAttribute('data-enquete-id', enquete.id);
                    enqueteTitle.addEventListener('click', function() {
                        toggleChartVisibility(enquete.id, enquete.prazo);
                    });
                    container.appendChild(enqueteTitle);

                    const totalVotes = enquete.opcoes.reduce((sum, opcao) => sum + opcao.votos, 0);
                    if (totalVotes === 0) {
                        const noVotesMessage = document.createElement('div');
                        noVotesMessage.classList.add('no-votes-message');
                        noVotesMessage.setAttribute('id', `noVotesMessage-${enquete.id}`);
                        noVotesMessage.textContent = 'Nenhum voto foi feito nesta enquete!';
                        container.appendChild(noVotesMessage);
                    } else {
                        const chartContainer = document.createElement('div');
                        chartContainer.classList.add('small-chart-container');
                        chartContainer.setAttribute('id', `chartContainer-${enquete.id}`);
                        chartContainer.style.display = 'none';
                        chartContainer.innerHTML = `<canvas id="chart-${enquete.id}" width="200" height="150"></canvas>`;
                        container.appendChild(chartContainer);

                        const ctx = document.getElementById(`chart-${enquete.id}`).getContext('2d');
                        const labels = enquete.opcoes.map(opcao => opcao.texto);
                        const votes = enquete.opcoes.map(opcao => opcao.votos);
                        const colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'];

                        const isHorizontal = labels.length > 4;
                        
                        new Chart(ctx, {
                            type: 'bar',
                            data: {
                                labels: labels,
                                datasets: [{
                                    label: 'Votos',
                                    data: votes,
                                    backgroundColor: colors.slice(0, labels.length),
                                    borderColor: '#333333',
                                    borderWidth: 1
                                }]
                            },
                            options: {
                                responsive: true,
                                indexAxis: isHorizontal ? 'y' : 'x',
                                plugins: {
                                    legend: { display: isHorizontal }
                                },
                                scales: isHorizontal ? {
                                    x: {
                                        beginAtZero: true,
                                        grid: { display: false }
                                    },
                                    y: {
                                        grid: { display: false }
                                    }
                                } : {
                                    x: {
                                        grid: { display: false }
                                    },
                                    y: {
                                        beginAtZero: true,
                                        grid: { display: false }
                                    }
                                }
                            }
                        });
                    }
                });

                const modal = new bootstrap.Modal(document.getElementById('resultadosEnquetesModal'));
                modal.show();
            } else {
                container.innerHTML = '<p>Nenhuma enquete foi encontrada.</p>';
            }
        })
        .catch(error => {
            console.error('Erro na requisição:', error);
        });
}

function toggleChartVisibility(enqueteId, prazo) {
    document.querySelectorAll('.small-chart-container, .no-votes-message, .prazo-element').forEach(element => {
        if (element.getAttribute('id') !== `chartContainer-${enqueteId}` && 
            element.getAttribute('id') !== `noVotesMessage-${enqueteId}` && 
            element.getAttribute('id') !== `prazo-${enqueteId}`) {
            element.style.display = 'none';
        }
    });

    const chartContainer = document.getElementById(`chartContainer-${enqueteId}`);
    const noVotesMessage = document.getElementById(`noVotesMessage-${enqueteId}`);

    let prazoElement = document.getElementById(`prazo-${enqueteId}`);
    if (!prazoElement && chartContainer) {
        prazoElement = document.createElement('p');
        prazoElement.classList.add('text-muted', 'ms-2', 'prazo-element');
        prazoElement.setAttribute('id', `prazo-${enqueteId}`);
        prazoElement.textContent = `Data de Encerramento: ${prazo}`;
        chartContainer.parentNode.insertBefore(prazoElement, chartContainer);
    }

    if (chartContainer) {
        const isCurrentlyHidden = chartContainer.style.display === 'none' || chartContainer.style.display === '';
        chartContainer.style.display = isCurrentlyHidden ? 'block' : 'none';
        if (prazoElement) prazoElement.style.display = isCurrentlyHidden ? 'block' : 'none';
        if (noVotesMessage) noVotesMessage.style.display = 'none';
    } else if (noVotesMessage) {
        noVotesMessage.style.display = 'block';
        if (prazoElement) prazoElement.style.display = 'block';
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getCSRFToken() {
    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrfToken;
}

document.getElementById('saveProgress').addEventListener('click', function () {
    const currentCapitulo = parseInt(document.getElementById('currentcapitulo').value);
    const totalCapitulos = parseInt(document.getElementById('totalcapitulo').value);

    if (currentCapitulo > 0 && totalCapitulos > 0) {
        if (currentCapitulo > totalCapitulos) {
            alert('O capítulo atual não pode ser maior que o total de capítulos.');
        } else {
            fetch(`{% url 'atualizar_progresso' clube.pk %}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    current_capitulo: currentCapitulo,
                    total_capitulos: totalCapitulos
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data); 
                if (data.success) {
                    const progressPercent = (currentCapitulo / totalCapitulos) * 100;
                    document.getElementById('progressBar').style.width = progressPercent + '%';
                    document.getElementById('progressBar').setAttribute('aria-valuenow', progressPercent);
                    document.getElementById('progressBar').innerText = Math.round(progressPercent) + '%';

                    document.getElementById('capituloAtualSpan').innerText = currentCapitulo;

                    $('#progressModal').modal('hide');
                } else {
                    alert('Erro ao salvar progresso.');
                }
            });
        }
    } else {
        alert('Por favor, insira valores positivos para os capítulos.');
    }
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('saveProgress').addEventListener('click', function () {
        const currentCapitulo = parseInt(document.getElementById('currentcapitulo').value);
        const totalCapitulos = parseInt(document.getElementById('totalcapitulo').value);
        const url = this.getAttribute('data-url');

        if (currentCapitulo > 0 && totalCapitulos > 0) {
            if (currentCapitulo > totalCapitulos) {
                alert('O capítulo atual não pode ser maior que o total de capítulos.');
            } else {
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        current_capitulo: currentCapitulo,
                        total_capitulos: totalCapitulos
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data); 
                    if (data.success) {
                        const progressPercent = (currentCapitulo / totalCapitulos) * 100;
                        const progressBar = document.getElementById('progressBar');
                        
                        progressBar.style.width = progressPercent + '%';
                        progressBar.setAttribute('aria-valuenow', progressPercent);
                        progressBar.innerText = Math.round(progressPercent) + '%';
    
                        document.getElementById('capituloAtualSpan').innerText = currentCapitulo;
    
                        if (progressPercent === 100) {
                            progressBar.classList.add('progress-bar-green');
                        } else {
                            progressBar.classList.remove('progress-bar-green');
                            progressBar.style.backgroundColor = '#4169E1';
                        }

                        $('#progressModal').modal('hide');
                    } else {
                        alert('Erro ao salvar progresso.');
                    }
                });
            }
        } else {
            alert('Por favor, insira valores positivos para os capítulos.');
        }
    });
});

document.querySelectorAll('[id^="topLivrosModal-"]').forEach(function (modal) {
    modal.addEventListener('show.bs.modal', function (event) {
        const clubeId = event.target.getAttribute('id').split('-')[1];
        const modalContent = document.getElementById(`topLivrosContent-${clubeId}`);
        
        fetch(`/clube/${clubeId}/top-livros/`)
            .then(response => response.text())
            .then(html => {
                modalContent.innerHTML = html;
            })
            .catch(err => {
                modalContent.innerHTML = '<p>Erro ao carregar os top livros.</p>';
            });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[id^="favoritar-btn-"]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var clubeId = this.getAttribute('data-clube-id');
            var url = `/clube/favoritar/${clubeId}/`;
            var buttonElement = this;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json',
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na requisição: ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                if (data.favoritado) {
                    buttonElement.innerHTML = '<i class="bi bi-star-fill"></i>';
                } else {
                    buttonElement.innerHTML = '<i class="bi bi-star"></i>';
                }
            })
            .catch(error => console.error('Erro:', error));
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
document.querySelectorAll('[id^="updateModal-"]').forEach(function (modal) {
    modal.addEventListener('show.bs.modal', function (event) {
        const clubeId = event.target.getAttribute('id').split('-')[1];
        const modalidadeSelect = modal.querySelector('#modalidade');
        const categoriaSelect = modal.querySelector('#categoria');

        fetch('/api/modalidades/')
            .then(response => response.json())
            .then(modalidades => {
                modalidadeSelect.innerHTML = '<option value="">Selecione uma modalidade</option>';
                modalidades.forEach(modalidade => {
                    const option = document.createElement('option');
                    option.value = modalidade.id;
                    option.textContent = modalidade.nome;
                    
                    if (modalidade.id == modal.getAttribute('data-modalidade-id')) {
                        option.selected = true;
                    }
                    modalidadeSelect.appendChild(option);
                });
            })
            .catch(err => console.error('Erro ao carregar modalidades:', err));

        fetch('/api/categorias/')
            .then(response => response.json())
            .then(categorias => {
                categoriaSelect.innerHTML = '<option value="">Selecione uma categoria</option>';
                categorias.forEach(categoria => {
                    const option = document.createElement('option');
                    option.value = categoria.id;
                    option.textContent = categoria.nome;
                    
                    if (categoria.id == modal.getAttribute('data-categoria-id')) {
                        option.selected = true;
                    }
                    categoriaSelect.appendChild(option);
                });
            })
            .catch(err => console.error('Erro ao carregar categorias:', err));
    });
});
});

const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  let cw = canvas.width = window.innerWidth;
  let ch = canvas.height = window.innerHeight;
  const rand = (min, max) => (min + Math.random() * (max - min));
  class SpeedLine {
    constructor(x, y) {
      this.x = x;
      this.y = y;
      this.speed = rand(2, 4);
      this.life = this.curLife = rand(500, 900);
      this.alpha = rand(0.25, 1);
      this.angle = Math.PI * rand(0, 2);
      this.size = rand(20, 40);
      this.inRadius = rand(200, 400);
      this.outRadius = cw;
    }
    update() {
      this.curLife -= this.speed;
      this.inRadius += this.speed * 4;
      this.alpha *= this.curLife / this.life;
      this.size *= this.curLife / this.life;
      this.draw();
    }
    draw() {
      const { x, y, size, angle, alpha } = this,
        { inRadius, outRadius } = this;
      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(angle);
      ctx.beginPath();
      ctx.moveTo(0, inRadius);
      ctx.lineTo(size, outRadius);
      ctx.lineTo(-size, outRadius);
      ctx.closePath();
      ctx.fillStyle = `rgba(255,255,255, ${alpha})`;
      ctx.fill();
      ctx.restore();
    }
  }
  const lines = [];
  const MAX_LINES = 300;
  function updateLines() {
    lines.forEach((line, i) => {
      if (!line || line.curLife < 0) lines[i] = new SpeedLine(cw / 2, ch / 2);
      lines[i].update();
    });
  }
  for (let i = 0; i < MAX_LINES; i++) {
    lines[i] = new SpeedLine(cw / 2, ch / 2);
  }
  function animate() {
    requestAnimationFrame(animate);
    ctx.clearRect(0, 0, cw, ch);
    updateLines();
  }
  animate();



// ###########################################################################