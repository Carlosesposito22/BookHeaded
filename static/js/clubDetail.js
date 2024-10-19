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