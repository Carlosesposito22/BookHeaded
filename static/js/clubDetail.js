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
  window.addEventListener('resize', () => {
    cw = canvas.width = window.innerWidth;
    ch = canvas.height = window.innerHeight;
    updateLines();
  });
    $(document).ready(function() {
        $('#maratonaModal').on('show.bs.modal', function () {
            $('#overlay').show();
        });
        $('#maratonaModal').on('hide.bs.modal', function () {
            $('#overlay').hide();
        });
    });


// Adiciona o JS da maratona daqui pra baixo, viu Mateus. 3 horas só pra descobrir que era só colocar meu código na parte de cima. A vida não é um morango. PS: Carlos
//Ps de novo: Porrrrraa.

document.getElementById('listarHistorico').addEventListener('click', function() {
    const clubeId = this.getAttribute('data-clube-id');
    listarHistorico(clubeId);
});

function listarHistorico(clubeId) {
    fetch(`/clube/${clubeId}/listar_historico_maratona/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            const historicoBody = document.getElementById('historicoBody');
            historicoBody.innerHTML = '';

            if (data.success) {
                if (data.historico.length === 0) {
                    historicoBody.innerHTML = '<tr><td colspan="5">Nenhum histórico encontrado.</td></tr>';
                } else {
                    data.historico.forEach(historico => {
                        const diasDuracao = calcularDuracao(historico.data_inicio, historico.data_fim);
                        const totalCapitulos = calcularTotalCapitulos(historico.capitulo_final, historico.capitulo_atual);
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${historico.nome_maratona}</td>
                            <td>${historico.data_inicio}</td>
                            <td>${historico.data_fim}</td>
                            <td>${diasDuracao} dias</td>
                            <td>${historico.capitulo_atual}</td>
                            <td>${historico.capitulo_final}</td>
                            <td>${totalCapitulos}</td>
                        `;
                        historicoBody.appendChild(row);
                    });
                }

                const modal = new bootstrap.Modal(document.getElementById('historicoMaratonasModal'));
                modal.show();
            } else {
                historicoBody.innerHTML = '<tr><td colspan="5">Nenhum histórico encontrado.</td></tr>';
            }
        })
        .catch(error => {
            console.error('Erro na requisição:', error);
        });
}


    document.getElementById('finalizarMaratona').addEventListener('click', function() {
    const createButton = document.getElementById('createMaratona');
    const clubeId = createButton.getAttribute('data-clube-id');

    fetch(`/clube/${clubeId}/finalizar_maratona/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Maratona finalizada com sucesso!');
            location.reload(true);
        } else {
            alert('Erro ao finalizar maratona.');
            console.error('Erro:', data);
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
    });
    location.reload(true);
});

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

function carregarDadosMaratona(clubeId) {
    fetch(`/clube/${clubeId}/detalhes_maratona/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.maratona_ativa) {
                    document.getElementById('nomeMaratona').value = data.nome_maratona;
                    document.getElementById('dataFim').value = data.data_fim;
                    document.getElementById('capituloFinal').value = data.capitulo_final;
                    document.getElementById('finalizarMaratona').style.display = 'block';
                    document.getElementById('saveMaratona').innerText = 'Salvar Mudança';
                } else {
                    document.getElementById('nomeMaratona').value = '';
                    document.getElementById('dataFim').value = '';
                    document.getElementById('capituloFinal').value = '';
                    document.getElementById('finalizarMaratona').style.display = 'none';
                    document.getElementById('saveMaratona').innerText = 'Criar Maratona';
                }
            } else {
                alert('Erro ao carregar dados da maratona.');
                console.error('Erro:', data);
            }
        })
        .catch(error => {
            console.error('Erro na requisição:', error);
        });
}


document.getElementById('saveMaratona').addEventListener('click', function() {
    const createButton = document.getElementById('createMaratona');
    const clubeId = createButton.getAttribute('data-clube-id');
    
    const nomeMaratona = document.getElementById('nomeMaratona').value;
    const dataFim = document.getElementById('dataFim').value;
    const dataInicio = document.getElementById('dataInicio').value;
    const capituloFinal = parseInt(document.getElementById('capituloFinal').value, 10);
    const capituloAtual = parseInt(document.getElementById('capituloAtual').value, 10);

    if (new Date(dataFim) < new Date(dataInicio)) {
        alert('A data final não pode ser menor que a data inicial.');
        return;
    }

    if (capituloFinal < capituloAtual) {
        alert('O capítulo final não pode ser menor que o capítulo atual.');
        return;
    }

    verificarNomeMaratonaExistente(nomeMaratona, clubeId)
        .then(nomeExistente => {
            if (nomeExistente) {
                alert('Já existe uma maratona com este nome. Por favor, escolha um nome diferente.');
                return;
            }

            fetch(`/clube/${clubeId}/criar_maratona/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    nome_maratona: nomeMaratona,
                    data_fim: dataFim,
                    data_inicio: dataInicio,
                    capitulo_final: capituloFinal,
                    capitulo_atual: capituloAtual,
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    carregarDadosMaratona(clubeId); 
                    location.reload(true);
                } else {
                    alert('Erro ao salvar maratona: ' + data.message);
                    console.error('Erro:', data);
                }
            })
            .catch(error => {
                console.error('Erro na requisição:', error);
            });
        });
});

function verificarNomeMaratonaExistente(nomeMaratona, clubeId) {
    return fetch(`/clube/${clubeId}/listar_historico_maratona/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                return data.historico.some(historico => historico.nome_maratona === nomeMaratona);
            } else {
                throw new Error('Erro ao carregar histórico.');
            }
        })
        .catch(error => {
            console.error('Erro na verificação do nome da maratona:', error);
            return false; 
        });
}


function calcularDuracao(dataInicio, dataFim) {
    const inicio = new Date(dataInicio);
    const fim = new Date(dataFim);
    const duracao = Math.abs(fim - inicio);
    const dias = Math.ceil(duracao / (1000 * 60 * 60 * 24));
    return dias;
}

function calcularTotalCapitulos(capituloFinal, capituloAtual) {
    return capituloFinal - capituloAtual;
}

document.getElementById('createMaratona').addEventListener('click', function(event) {
    const createButton = event.currentTarget;
    const clubeId = createButton.getAttribute('data-clube-id');

    if (!clubeId) {
        console.error('Clube ID não encontrado.');
        return;
    }

    carregarDadosMaratona(clubeId); 
});


window.onload = function() {
    const createButton = document.getElementById('createMaratona');
    const clubeId = createButton.getAttribute('data-clube-id');
    if (clubeId) {
        carregarDadosMaratona(clubeId);
    }
};

    document.addEventListener('DOMContentLoaded', function() {
                const today = new Date().toISOString().split('T')[0];
                document.getElementById('dataInicio').value = today;
            });
