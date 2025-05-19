document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("fileInput");
  const uploadBtn = document.getElementById("uploadBtn");
  const summarizeBtn = document.getElementById("summarizeBtn");
  const textArea = document.getElementById("textArea");
  const summaryArea = document.getElementById("summaryArea");
  const status = document.getElementById("status");

  // Create spinner & progress bar elements dynamically (or have them in your HTML)
  const spinner = document.createElement("div");
  spinner.id = "spinner";
  spinner.style.display = "none";
  spinner.innerText = "⏳ Loading...";
  status.parentNode.insertBefore(spinner, status.nextSibling);

  const progressContainer = document.createElement("div");
  progressContainer.id = "progressContainer";
  progressContainer.style.display = "none";
  progressContainer.style.width = "100%";
  progressContainer.style.background = "#eee";
  progressContainer.style.marginTop = "10px";
  progressContainer.style.height = "20px";
  progressContainer.style.borderRadius = "10px";
  status.parentNode.insertBefore(progressContainer, spinner.nextSibling);

  const progressBar = document.createElement("div");
  progressBar.id = "progressBar";
  progressBar.style.height = "100%";
  progressBar.style.width = "0%";
  progressBar.style.background = "#4caf50";
  progressBar.style.borderRadius = "10px";
  progressContainer.appendChild(progressBar);

  // Upload file and extract text from backend
  uploadBtn.addEventListener("click", async () => {
    const file = fileInput.files[0];
    if (!file) {
      status.innerText = "⚠️ Please select a file first.";
      return;
    }

    // Reset UI
    summaryArea.value = "";
    status.innerText = "";
    progressContainer.style.display = "none";

    uploadBtn.disabled = true;
    summarizeBtn.disabled = true;
    spinner.style.display = "inline-block";
    status.innerText = "Uploading and extracting text...";

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();

      if (data.error) throw new Error(data.error);
      textArea.value = data.text || "";
      status.innerText = "✅ Text extracted.";
      summarizeBtn.disabled = false;
    } catch (err) {
      status.innerText = "❌ " + err.message;
      textArea.value = "";
    } finally {
      uploadBtn.disabled = false;
      spinner.style.display = "none";
    }
  });

  // Summarize the extracted text
  summarizeBtn.addEventListener("click", async () => {
    const text = textArea.value.trim();
    if (!text) {
      status.innerText = "⚠️ No text to summarize.";
      return;
    }

    summarizeBtn.disabled = true;
    uploadBtn.disabled = true;
    status.innerText = "Summarizing...";
    summaryArea.value = "";
    spinner.style.display = "none";

    progressContainer.style.display = "block";
    progressBar.style.width = "0%";

    try {
      const res = await fetch("/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();

      if (data.error) throw new Error(data.error);

      // Animate progress bar and type summary text
      let progress = 0;
      const summaryText = data.summary || "";
      const totalLength = summaryText.length;

      const interval = setInterval(() => {
        progress += 2; // Increase progress by 2% every 100ms
        if (progress > 100) progress = 100;

        progressBar.style.width = progress + "%";

        // Show part of summary text based on progress
        const charsToShow = Math.floor((progress / 100) * totalLength);
        summaryArea.value = summaryText.substring(0, charsToShow);

        if (progress === 100) {
          clearInterval(interval);
          status.innerText = "✅ Summary complete.";
          summarizeBtn.disabled = false;
           progressContainer.style.display = "none";
          uploadBtn.disabled = false;
        }
      }, 100);
    } catch (err) {
      progressContainer.style.display = "none";
      status.innerText = "❌ " + err.message;
      summarizeBtn.disabled = false;
      uploadBtn.disabled = false;
    }
  });
});
