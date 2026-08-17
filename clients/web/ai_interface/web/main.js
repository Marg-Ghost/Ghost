const input = document.getElementById("input");
const answer = document.getElementById("answer_input");

async function request_chat(prompt) {
  const response = await fetch("http://localhost:4100/", {
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