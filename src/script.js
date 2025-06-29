const mario = document.getElementById("mario");

let x = 100;
let y = 0; // Começa no chão
let yVelocity = 0;
const gravity = 1;
let onGround = true;
let keys = {};
let jumpPressed = false;

function update() {
  // Movimento lateral com "d" (direita) e "a" (esquerda)
  if (keys["d"] || keys["D"]) x += 5;
  if (keys["a"] || keys["A"]) x -= 5;

  // Gravidade
  yVelocity += gravity;
  y += yVelocity;

  // Chão
  if (y < 0) {
    y = 0;
    yVelocity = 0;
    onGround = true;
  } else {
    onGround = false;
  }

  mario.style.left = `${x}px`;
  mario.style.bottom = `${y}px`;

  requestAnimationFrame(update);
}

document.addEventListener("keydown", (e) => {
  keys[e.key] = true;
  // Só pula se a tecla foi solta desde o último pulo e está no chão
  if ((e.key === " " || e.key === "ArrowUp") && onGround && !jumpPressed) {
    yVelocity = -18;
    onGround = false;
    jumpPressed = true;
  }
});

document.addEventListener("keyup", (e) => {
  keys[e.key] = false;
  // Libera o pulo só ao soltar a tecla
  if (e.key === " " || e.key === "ArrowUp") {
    jumpPressed = false;
  }
});

update();