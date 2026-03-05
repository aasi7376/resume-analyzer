// ── File Upload Display ───────────────────────────────
document.addEventListener("DOMContentLoaded", function () {
  const resumeFile = document.getElementById("resumeFile");
  if (resumeFile) {
    resumeFile.addEventListener("change", function () {
      const fileName = this.files[0]?.name;
      const fileNameEl = document.getElementById("fileName");
      if (fileName && fileNameEl) {
        fileNameEl.textContent = "✅ " + fileName;
        fileNameEl.style.display = "block";
      }
    });
  }
});

// ── Drag and Drop ─────────────────────────────────────
const dropZone = document.getElementById("dropZone");
if (dropZone) {
  dropZone.addEventListener("dragover", function (e) {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });

  dropZone.addEventListener("dragleave", function () {
    dropZone.classList.remove("dragover");
  });

  dropZone.addEventListener("drop", function (e) {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    const file = e.dataTransfer.files[0];
    if (file && file.type === "application/pdf") {
      const fileInput = document.getElementById("resumeFile");
      const dt = new DataTransfer();
      dt.items.add(file);
      fileInput.files = dt.files;
      const fileNameEl = document.getElementById("fileName");
      fileNameEl.textContent = "✅ " + file.name;
      fileNameEl.style.display = "block";
    }
  });
}

// ── Main Analyze Function ─────────────────────────────
function analyzeResume() {
  const fileInput     = document.getElementById("resumeFile");
  const jobDesc       = document.getElementById("jobDescription").value.trim();
  const errorBox      = document.getElementById("errorBox");
  const btn           = document.getElementById("analyzeBtn");
  const btnText       = document.getElementById("btnText");
  const spinner       = document.getElementById("spinner");

  // Reset UI
  errorBox.style.display = "none";
  document.getElementById("results").style.display = "none";

  // Validate
  if (!fileInput.files[0]) {
    showError("Please upload a resume PDF.");
    return;
  }
  if (!jobDesc) {
    showError("Please enter a job description.");
    return;
  }

  // Show loading
  btn.disabled          = true;
  btnText.style.display = "none";
  spinner.style.display = "block";

  // Build form data
  const formData = new FormData();
  formData.append("resume", fileInput.files[0]);
  formData.append("job_description", jobDesc);

  // Send to Flask
  fetch("/analyze", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      // Reset button
      btn.disabled          = false;
      btnText.style.display = "block";
      spinner.style.display = "none";

      if (data.error) {
        showError(data.error);
        return;
      }

      displayResults(data);
    })
    .catch(() => {
      btn.disabled          = false;
      btnText.style.display = "block";
      spinner.style.display = "none";
      showError("Something went wrong. Please try again.");
    });
}

// ── Display Results ───────────────────────────────────
function displayResults(data) {
  const results = document.getElementById("results");
  results.style.display = "block";

  // ── Score Ring ──────────────────────────────────────
  const score       = data.final_score;
  const scoreFill   = document.getElementById("scoreFill");
  const circumference = 339.29;
  const offset      = circumference - (score / 100) * circumference;

  // Color logic
  let color = "#ff6b6b";
  if (score >= 70)      color = "#00d4aa";
  else if (score >= 40) color = "#f5a623";

  scoreFill.style.stroke            = color;
  scoreFill.style.strokeDashoffset  = offset;

  document.getElementById("scoreNumber").textContent = score + "%";
  document.getElementById("scoreNumber").style.color = color;

  // Score title and description
  let title, desc;
  if (score >= 70) {
    title = "Strong Match 🎉";
    desc  = "Your resume is well aligned with this job description.";
  } else if (score >= 40) {
    title = "Moderate Match ⚠️";
    desc  = "Your resume partially matches. Add the missing keywords.";
  } else {
    title = "Weak Match ❌";
    desc  = "Your resume needs significant improvement for this role.";
  }

  document.getElementById("scoreTitle").textContent = title;
  document.getElementById("scoreDesc").textContent  = desc;

  // Sub scores
  document.getElementById("similarityScore").textContent = data.similarity_score + "%";
  document.getElementById("keywordScore").textContent    = data.keyword_match_ratio + "%";

  // ── Keywords ────────────────────────────────────────
  document.getElementById("matchedCount").textContent =
    data.total_matched + " of " + data.total_jd_keywords + " keywords found";
  document.getElementById("missingCount").textContent =
    data.missing_keywords.length + " keywords missing";

  // Matched tags
  const matchedEl = document.getElementById("matchedKeywords");
  matchedEl.innerHTML = "";
  data.matched_keywords.forEach((kw) => {
    const tag       = document.createElement("span");
    tag.className   = "tag tag-matched";
    tag.textContent = kw;
    matchedEl.appendChild(tag);
  });

  // Missing tags
  const missingEl = document.getElementById("missingKeywords");
  missingEl.innerHTML = "";
  data.missing_keywords.forEach((kw) => {
    const tag       = document.createElement("span");
    tag.className   = "tag tag-missing";
    tag.textContent = kw;
    missingEl.appendChild(tag);
  });

  // ── Suggestions ──────────────────────────────────────
  const suggList  = document.getElementById("suggestionsList");
  suggList.innerHTML = "";
  data.suggestions.forEach((s) => {
    const li       = document.createElement("li");
    li.textContent = s;
    suggList.appendChild(li);
  });

  // Scroll to results
  results.scrollIntoView({ behavior: "smooth" });
}

// ── Show Error ────────────────────────────────────────
function showError(message) {
  const errorBox      = document.getElementById("errorBox");
  errorBox.textContent = message;
  errorBox.style.display = "block";
}