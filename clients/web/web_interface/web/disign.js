const canvas = document.getElementById('ghost-canvas');
const ctx = canvas.getContext('2d');

// Größe des Canvas an das CSS anpassen
function resizeCanvas() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// Setup für den Binär-Regen
const letters = "01"; 
const fontSize = 18;
let columns = canvas.width / fontSize;
let drops = [];

// Startpositionen für die Tropfen
for(let x = 0; x < columns; x++) {
    drops[x] = 1;
}

function draw() {
    // Zeichnet einen leicht transparenten weißen Hintergrund,
    // um den "Schweif"-Effekt der fallenden Zahlen zu erzeugen.
    // (Weiß, weil dein --background-color weiß ist)
    ctx.fillStyle = "rgba(255, 255, 255, 0.1)"; 
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#ff0000"; // Deine rote --primary-color
    ctx.font = "bold " + fontSize + "px monospace";

    for(let i = 0; i < drops.length; i++) {
        // Wähle zufällig 0 oder 1
        const text = letters.charAt(Math.floor(Math.random() * letters.length));
        
        // Zeichne das Zeichen
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

        // Schicke den Tropfen wieder nach oben, wenn er unten ankommt (mit etwas Zufall)
        if(drops[i] * fontSize > canvas.height && Math.random() > 0.95) {
            drops[i] = 0;
        }
        // Tropfen einen Schritt nach unten bewegen
        drops[i]++;
    }
}

// Führe die Zeichen-Funktion alle 50 Millisekunden aus
setInterval(draw, 50);