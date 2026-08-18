async function load_memory(type) {
    const overlay = document.getElementById("memory-overlay");
    const display = document.getElementById("memory-display");
    const title = document.getElementById("memory-title");

    title.innerText = type === "long" ? "Long Term Memory" : "Short Term Memory";
    display.innerText = "Loading...";
    overlay.classList.remove("hidden"); 

    try {
        const response = await fetch("/load_data", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ role: "user", content: type })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        display.innerText = JSON.stringify(data.memory, null, 2);
    } catch (e) {
        display.innerText = `[Fehler] ${e.message}`;
    }
}

function close_memory() {
    document.getElementById("memory-overlay").classList.add("hidden");
}

// Optional: Klick auf den dunklen Hintergrund schließt das Overlay ebenfalls
document.getElementById("memory-overlay").addEventListener("click", (e) => {
    if (e.target.id === "memory-overlay") {
        close_memory();
    }
});


const input = document.getElementById("input");
const answer = document.getElementById("answer_input");

async function request_chat(prompt) {
  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ role: "user", content: prompt })
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  const data = await response.json();
  return data;
}

function handle_chat(event) {
  if (event.key !== "Enter" || event.shiftKey) {
    return;
  }

  event.preventDefault();

  const text = input.value.trim();
  if (!text) {
    return;
  }

  answer.textContent = "Thinking...";
  input.value = "";

  request_chat(text)
    .then((response) => {
      answer.textContent = response;
    })
    .catch((error) => {
      answer.textContent = `[Error] ${error.message}`;
    });
}

input.addEventListener("keydown", handle_chat);