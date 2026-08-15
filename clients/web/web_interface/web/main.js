////////////////////////////////////////////////
// Server-health
/////////////////////////////////////////////////
async function dashboard() {
    const timeElement = document.getElementById("Time");
    const cpuTempElement = document.getElementById("cpu_temp");
    const cpuLoadElement = document.getElementById("cpu_load");
    const diskFreeElement = document.getElementById("disk_free");
    const ramInfoElement = document.getElementById("ram_free");

    try {
        const response = await fetch('/dashboard', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data_type: 'text' })
        });
        const data = await response.json();
        if (timeElement) timeElement.textContent = "Time: " + data.time;
        if (cpuTempElement) cpuTempElement.textContent = "CPU Temp: " + data.cpu_temp;
        if (cpuLoadElement) cpuLoadElement.textContent = "CPU Load: " + data.cpu_load;
        if (diskFreeElement) diskFreeElement.textContent = "Disk Free: " + data.disk_free;
        if (ramInfoElement) ramInfoElement.textContent = "RAM Info: " + data.ram_info;
    } catch (err) {
        console.error("Refresh Error:", err);
    }
}
////////////////////////////////////////////////
// Ordner-preview
/////////////////////////////////////////////////
async function show_section(sectionId) {
    const section_use = document.getElementById("folder");
    if (!section_use) return;
    section_use.style.display = "block";
    const h2 = section_use.querySelector('h2');
    if (h2) h2.innerHTML = sectionId;

    const list = document.getElementById("file-list");
    try {
        const response = await fetch('/dashboard/src', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ section: sectionId })
        });
        const data = await response.json();
        list.innerHTML = "";
        if (Array.isArray(data)) {
            data.forEach(item => {
                const listItem = document.createElement("li");
                listItem.textContent = item.name || JSON.stringify(item);
                list.appendChild(listItem);
            });
        } else if (data && typeof data === 'object') {
            Object.values(data).flat().forEach(item => {
                const listItem = document.createElement("li");
                listItem.textContent = item.name || JSON.stringify(item);
                list.appendChild(listItem);
            });
        }
    } catch (err) {
        console.error("Refresh Error:", err);
    }
}


// Aktualisierungslogik
setInterval(dashboard, 2000);
dashboard();

