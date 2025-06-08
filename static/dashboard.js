document.addEventListener("DOMContentLoaded", async () => {
  const socket = io();
  const logBody = document.getElementById("logBody");
  const latestAlert = document.getElementById("latest-alert");
  const pieCtx = document.getElementById("intrusionPie").getContext("2d");
  const timeCtx = document.getElementById("timeSeries").getContext("2d");

  let pieChart;
  let timeChart;
  const intrusionCounts = {};
  const intrusionTimeline = [];

  function updatePieChart(label) {
    intrusionCounts[label] = (intrusionCounts[label] || 0) + 1;
    const labels = Object.keys(intrusionCounts);
    const data = Object.values(intrusionCounts);

    if (pieChart) pieChart.destroy();
    pieChart = new Chart(pieCtx, {
      type: 'pie',
      data: { labels, datasets: [{ data, backgroundColor: ["#ff66ff", "#00ffff", "#ff9999"] }] },
      options: { responsive: true, plugins: { legend: { labels: { color: "white" } } } }
    });
  }

  function updateTimeSeries(timestamp) {
    intrusionTimeline.push({ x: new Date(timestamp), y: 1 });
    const grouped = {};
    intrusionTimeline.forEach(({ x }) => {
      const key = x.toISOString().slice(0, 16);
      grouped[key] = (grouped[key] || 0) + 1;
    });
    const labels = Object.keys(grouped);
    const values = Object.values(grouped);

    if (timeChart) timeChart.destroy();
    timeChart = new Chart(timeCtx, {
      type: 'line',
      data: { labels, datasets: [{ label: 'Intrusions Over Time', data: values, borderColor: '#ff66ff' }] },
      options: {
        responsive: true,
        plugins: { legend: { labels: { color: "white" } } },
        scales: {
          x: { ticks: { color: "white" } },
          y: { ticks: { color: "white" }, beginAtZero: true }
        }
      }
    });
  }

  function addRow(log) {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${log.timestamp}</td>
      <td>${log.ip}</td>
      <td>${log.username}</td>
      <td>${log.password}</td>
      <td>${log.label}</td>
    `;
    logBody.prepend(row);
  }

  function initLogs(logs) {
    logs.forEach((log) => {
      addRow(log);
      updatePieChart(log.label);
      updateTimeSeries(log.timestamp);
    });
  }

  // ✅ Load logs on page load
  try {
    const res = await fetch("/logs/labeled_intrusions.json");
    if (res.ok) {
      const logs = await res.json();
      initLogs(logs);
    }
  } catch (err) {
    console.error("Failed to load initial logs:", err);
  }

  socket.on("new_log", (log) => {
    addRow(log);
    latestAlert.textContent = `⚠️ Intrusion Detected: ${log.label}`;
    latestAlert.classList.add("alert-glow");
    setTimeout(() => latestAlert.classList.remove("alert-glow"), 3000);
    updatePieChart(log.label);
    updateTimeSeries(log.timestamp);
  });
});
