// ---- Tabs ----
document.addEventListener("click", (e) => {
  const tabBtn = e.target.closest("[data-tabs] .tab");
  if (!tabBtn) return;
  if (tabBtn.disabled) return;

  const tabsRoot = tabBtn.closest("[data-tabs]");
  const tabName = tabBtn.getAttribute("data-tab");

  // set active button
  tabsRoot.querySelectorAll(".tab").forEach(btn => btn.classList.remove("active"));
  tabBtn.classList.add("active");

  // toggle panels
  document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
  const panel = document.getElementById("tab-" + tabName);
  if (panel) panel.classList.add("active");
});

// ---- AJAX Helpers ----
async function postForm(url, dataObj) {
  const formData = new URLSearchParams();
  Object.keys(dataObj).forEach(k => formData.append(k, dataObj[k]));

  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData.toString()
  });

  const payload = await res.json().catch(() => ({}));
  return { status: res.status, payload };
}

// ---- Client form: link/unlink contact ----
window.linkContact = async function(clientId) {
  const select = document.getElementById("linkContactSelect");
  const contactId = select ? parseInt(select.value, 10) : NaN;
  if (!contactId) {
    alert("Please select a contact to link.");
    return;
  }

  const { status, payload } = await postForm(`/clients/${clientId}/link-contact`, { contact_id: contactId });

  if (status === 200) {
    // simplest: refresh page to reflect list + dropdown changes
    window.location.reload();
  } else {
    alert(payload.message || "Failed to link contact.");
  }
};

window.unlinkContact = async function(ev, clientId, contactId) {
  ev.preventDefault();
  const { status, payload } = await postForm(`/clients/${clientId}/unlink-contact`, { contact_id: contactId });

  if (status === 200) {
    window.location.reload();
  } else {
    alert(payload.message || "Failed to unlink contact.");
  }
};

// ---- Contact form: link/unlink client ----
window.linkClient = async function(contactId) {
  const select = document.getElementById("linkClientSelect");
  const clientId = select ? parseInt(select.value, 10) : NaN;
  if (!clientId) {
    alert("Please select a client to link.");
    return;
  }

  const { status, payload } = await postForm(`/contacts/${contactId}/link-client`, { client_id: clientId });

  if (status === 200) {
    window.location.reload();
  } else {
    alert(payload.message || "Failed to link client.");
  }
};

window.unlinkClient = async function(ev, contactId, clientId) {
  ev.preventDefault();
  const { status, payload } = await postForm(`/contacts/${contactId}/unlink-client`, { client_id: clientId });

  if (status === 200) {
    window.location.reload();
  } else {
    alert(payload.message || "Failed to unlink client.");
  }
};
