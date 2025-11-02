document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const fileInput = document.getElementById("fileInput");
  const uploadBtn = document.getElementById("uploadBtn");
  const summarizeBtn = document.getElementById("summarizeBtn");
  const textArea = document.getElementById("textArea");
  const summaryArea = document.getElementById("summaryArea");
  const statusEl = document.getElementById("status");
  const spinner = document.getElementById("spinner");
  const progressContainer = document.getElementById("progressContainer");
  const progressBar = document.getElementById("progressBar");
  const cursorLabel = document.getElementById("cursorLabel");
  const dropZone = document.getElementById("dropZone");

  // Config
  const AUTO_UPLOAD_ON_DROP = true;
  const AUTO_UPLOAD_ON_SELECT = false; // set true if you want auto-upload after choosing a file

  // Helpers
  const setStatus = (msg) => { if (statusEl) statusEl.textContent = msg || ""; };
  const showSpinner = (show = true) => { if (spinner) spinner.style.display = show ? "inline-block" : "none"; };
  const showProgress = (show = true) => { if (progressContainer) progressContainer.style.display = show ? "block" : "none"; };
  const setProgress = (pct) => { if (progressBar) progressBar.style.width = `${Math.max(0, Math.min(100, pct))}%`; };
  const setBusy = (busy) => {
    [uploadBtn, summarizeBtn, fileInput].forEach(el => el && (el.disabled = !!busy));
    document.body.setAttribute("aria-busy", busy ? "true" : "false");
  };

  // Cursor label: follow pointer
  document.addEventListener("mousemove", (e) => {
    if (!cursorLabel) return;
    cursorLabel.style.top = `${e.clientY + 15}px`;
    cursorLabel.style.left = `${e.clientX + 15}px`;
  });

  // Summary expand/collapse with label updates
  let hideLabelTimer = null;
  const updateCursorLabelText = () => {
    if (!cursorLabel) return;
    cursorLabel.textContent = summaryArea.classList.contains("expanded") ? "Collapse" : "Expand";
  };

  if (summaryArea && cursorLabel) {
    summaryArea.addEventListener("mouseenter", () => {
      updateCursorLabelText();
      cursorLabel.style.opacity = 1;
    });
    summaryArea.addEventListener("mouseleave", () => {
      if (hideLabelTimer) clearTimeout(hideLabelTimer);
      hideLabelTimer = setTimeout(() => (cursorLabel.style.opacity = 0), 150);
    });
    summaryArea.addEventListener("click", () => {
      summaryArea.classList.toggle("expanded");
      updateCursorLabelText();
    });
    // Collapse with Escape key
    summaryArea.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        summaryArea.classList.remove("expanded");
        updateCursorLabelText();
      }
    });
    // Click outside to collapse
    document.addEventListener("click", (e) => {
      if (!summaryArea.contains(e.target)) {
        summaryArea.classList.remove("expanded");
        if (cursorLabel) cursorLabel.style.opacity = 0;
      }
    });
  }

  // Upload logic
  async function handleUpload(selectedFile) {
    const file = selectedFile || (fileInput && fileInput.files && fileInput.files[0]);
    if (!file) {
      setStatus("⚠️ Please select a file first.");
      return;
    }
    if (!/\.docx?$/i.test(file.name)) {
      setStatus("Please choose a .doc or .docx file.");
      return;
    }

    // Reset UI
    summaryArea.value = "";
    setStatus("");
    showProgress(false);
    setBusy(true);
    showSpinner(true);
    setStatus("Uploading and extracting text...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (!res.ok || data.error) throw new Error(data.error || "Upload failed");

      textArea.value = data.text || "";
      setStatus("✅ Text extracted.");
      summarizeBtn.disabled = false;
    } catch (err) {
      setStatus("❌ " + (err.message || "Upload error"));
      textArea.value = "";
    } finally {
      setBusy(false);
      showSpinner(false);
    }
  }

  // Summarize logic
  async function handleSummarize() {
    const text = (textArea.value || "").trim();
    if (!text) {
      setStatus("⚠️ No text to summarize.");
      return;
    }

    let typeInterval = null;
    try {
      setBusy(true);
      setStatus("Summarizing...");
      summaryArea.value = "";
      showSpinner(false);

      showProgress(true);
      setProgress(0);

      const res = await fetch("/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      if (!res.ok || data.error) throw new Error(data.error || "Summarization failed");

      const summaryText = data.summary || "";
      const totalLength = summaryText.length;

      // Type/Progress animation
      let progress = 0;
      typeInterval = setInterval(() => {
        progress = Math.min(progress + 2, 100);
        setProgress(progress);

        const charsToShow = Math.floor((progress / 100) * totalLength);
        summaryArea.value = summaryText.substring(0, charsToShow);

        if (progress >= 100) {
          clearInterval(typeInterval);
          typeInterval = null;
          summaryArea.value = summaryText; // ensure full text
          setStatus("✅ Summary complete.");
          showProgress(false);
          setBusy(false);
        }
      }, 90);
    } catch (err) {
      if (typeInterval) clearInterval(typeInterval);
      showProgress(false);
      setStatus("❌ " + (err.message || "Summarization error"));
      setBusy(false);
    }
  }

  // Event: Upload click
  if (uploadBtn) uploadBtn.addEventListener("click", () => handleUpload());

  // Event: Summarize click
  if (summarizeBtn) summarizeBtn.addEventListener("click", handleSummarize);

  // Event: Auto-upload when selecting a file (optional)
  if (fileInput) {
    fileInput.addEventListener("change", () => {
      if (fileInput.files && fileInput.files[0]) {
        setStatus(`Selected: ${fileInput.files[0].name}`);
        if (AUTO_UPLOAD_ON_SELECT) handleUpload();
      }
    });
  }

  // Drag & Drop
  if (dropZone && fileInput) {
    const preventDefaults = (e) => { e.preventDefault(); e.stopPropagation(); };

    // Prevent browser from opening file when dropped anywhere
    ["dragover", "drop"].forEach(evt => {
      document.addEventListener(evt, (e) => e.preventDefault());
    });

    ["dragenter", "dragover"].forEach(evt => {
      dropZone.addEventListener(evt, (e) => {
        preventDefaults(e);
        dropZone.classList.add("is-dragover");
      });
    });

    ["dragleave", "dragend", "drop"].forEach(evt => {
      dropZone.addEventListener(evt, (e) => {
        preventDefaults(e);
        dropZone.classList.remove("is-dragover");
      });
    });

    dropZone.addEventListener("click", () => fileInput.click());
    dropZone.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        fileInput.click();
      }
    });

    dropZone.addEventListener("drop", async (e) => {
      const files = e.dataTransfer?.files;
      if (!files || !files.length) return;
      const file = files[0];

      if (!/\.docx?$/i.test(file.name)) {
        setStatus("Please drop a .doc or .docx file.");
        return;
      }

      // Reflect dropped file into the input (for consistency)
      try {
        if (window.DataTransfer) {
          const dt = new DataTransfer();
          dt.items.add(file);
          fileInput.files = dt.files;
        } else {
          fileInput.files = files; // fallback
        }
      } catch (_) { /* ignore */ }

      setStatus(`Selected: ${file.name}`);

      if (AUTO_UPLOAD_ON_DROP) {
        await handleUpload(file);
      }
    });
  }
});