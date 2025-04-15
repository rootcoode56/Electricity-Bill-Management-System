let user = null;

// Loading state
function showLoading(formId, buttonText) {
  const form = document.getElementById(formId);
  if (form) {
    const button = form.querySelector("button");
    button.innerText = "Processing...";
    button.disabled = true;
  } else {
    const button = document.querySelector(`button[onclick="${formId}()"]`);
    if (button) {
      button.innerText = "Processing...";
      button.disabled = true;
    }
  }
}

function hideLoading(formId, buttonText) {
  const form = document.getElementById(formId);
  if (form) {
    const button = form.querySelector("button");
    button.innerText = buttonText;
    button.disabled = false;
  } else {
    const button = document.querySelector(`button[onclick="${formId}()"]`);
    if (button) {
      button.innerText = buttonText;
      button.disabled = false;
    }
  }
}

// Login
document.getElementById("login-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  showLoading("login-form", "Login");
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();

    if (data.success) {
      user = { user_id: data.user_id, role: data.role };
      localStorage.setItem("user", JSON.stringify(user));
      window.location.href = "/dashboard.html";
    } else {
      document.getElementById("error-message").innerText =
        "❌ Invalid credentials! Try again.";
    }
  } catch (error) {
    document.getElementById("error-message").innerText = "Error logging in";
  } finally {
    hideLoading("login-form", "Login");
  }
});

// Dashboard: Show role-based menu
document.addEventListener("DOMContentLoaded", () => {
  user = JSON.parse(localStorage.getItem("user"));
  if (!user && window.location.pathname !== "/index.html") {
    window.location.href = "/index.html";
    return;
  }

  if (document.getElementById("username-display")) {
    document.getElementById("username-display").innerText = user.user_id;
    document.getElementById(`${user.role}-menu`).style.display = "block";
  }

  if (window.location.pathname === "/notifications.html") {
    fetchNotifications();
  }

  if (window.location.pathname === "/admin.html" && window.location.hash) {
    const section = window.location.hash.substring(1);
    document.getElementById(section)?.scrollIntoView();
  }
});

// Logout
function logout() {
  localStorage.removeItem("user");
  window.location.href = "/index.html";
}

// Customer: View bill
document.getElementById("bill-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  showLoading("bill-form", "View Bill");
  const month = document.getElementById("month").value;

  try {
    const response = await fetch(`/api/bills/${user.user_id}?month=${month}`);
    const data = await response.json();
    document.getElementById("bill-details").innerText = JSON.stringify(
      data,
      null,
      2
    );
    document.getElementById("month-pay").value = month;
  } catch (error) {
    document.getElementById("message").innerText = "Error fetching bill";
  } finally {
    hideLoading("bill-form", "View Bill");
  }
});

// Customer: Pay bill
document.getElementById("pay-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  showLoading("pay-form", "Pay Bill");
  const month = document.getElementById("month-pay").value;
  const payment_method = document.getElementById("payment_method").value;

  try {
    const response = await fetch(`/api/bills/${user.user_id}/pay`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ month, payment_method }),
    });
    const data = await response.json();
    document.getElementById("message").innerText = data.message;
  } catch (error) {
    document.getElementById("message").innerText = "Error paying bill";
  } finally {
    hideLoading("pay-form", "Pay Bill");
  }
});

// Customer: Lodge complaint
document
  .getElementById("complaint-form")
  ?.addEventListener("submit", async (e) => {
    e.preventDefault();
    showLoading("complaint-form", "Submit Complaint");
    const complaint_text = document.getElementById("complaint_text").value;

    try {
      const response = await fetch(`/api/complaints/${user.user_id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ complaint_text }),
      });
      const data = await response.json();
      document.getElementById("message").innerText = data.message;
      document.getElementById("complaint_text").value = "";
    } catch (error) {
      document.getElementById("message").innerText =
        "Error submitting complaint";
    } finally {
      hideLoading("complaint-form", "Submit Complaint");
    }
  });

// Customer: Track complaints
async function trackComplaints() {
  try {
    const response = await fetch(`/api/complaints/${user.user_id}`);
    const data = await response.json();
    document.getElementById("complaints").innerText = JSON.stringify(
      data,
      null,
      2
    );
  } catch (error) {
    document.getElementById("message").innerText = "Error fetching complaints";
  }
}

// Customer: Apply for service
async function applyService(service_type) {
  let connection_data = null;
  if (service_type === "new_connection") {
    const name = document.getElementById("name")?.value;
    const address = document.getElementById("address")?.value;
    if (!name || !address) {
      document.getElementById("message").innerText =
        "Please fill out name and address";
      return;
    }
    connection_data = { name, address };
  }

  try {
    const response = await fetch(`/api/services/${user.user_id}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ service_type, connection_data }),
    });
    const data = await response.json();
    document.getElementById("message").innerText = data.message;
  } catch (error) {
    document.getElementById(
      "message"
    ).innerText = `Error applying for ${service_type}`;
  }
}

// Handle new connection form
document
  .getElementById("new-connection-form")
  ?.addEventListener("submit", async (e) => {
    e.preventDefault();
    applyService("new_connection");
  });

// Load notifications
async function fetchNotifications() {
  try {
    const response = await fetch(`/api/notifications/${user.user_id}`);
    const notifications = await response.json();
    const list = document.getElementById("notification-list");
    list.innerHTML = "";
    if (notifications.length === 0) {
      document.getElementById("message").innerText = "No notifications found.";
    } else {
      notifications.forEach((notification) => {
        const li = document.createElement("li");
        li.innerText = notification;
        list.appendChild(li);
      });
    }
  } catch (error) {
    document.getElementById("message").innerText =
      "Error fetching notifications";
  }
}

// Admin: View all users
async function viewAllUsers() {
  showLoading("viewAllUsers", "View All Users");
  const tableBody = document.querySelector("#users-table tbody");
  const message = document.getElementById("users-message");
  tableBody.innerHTML = "";
  message.innerText = "";

  try {
    const response = await fetch("/api/admin/users");
    const users = await response.json();
    if (Object.keys(users).length === 0) {
      message.innerText = "No users found.";
      return;
    }
    Object.values(users).forEach((user) => {
      const row = document.createElement("tr");
      row.innerHTML = `
                <td>${user.user_id}</td>
                <td>${user.username}</td>
                <td>${user.name}</td>
                <td>${user.address}</td>
                <td>${user.meter_id || "N/A"}</td>
                <td>${user.role}</td>
            `;
      tableBody.appendChild(row);
    });
  } catch (error) {
    message.innerText = "Error fetching users";
  } finally {
    hideLoading("viewAllUsers", "View All Users");
  }
}

// Admin: Manage requests
async function manageRequests() {
  showLoading("manageRequests", "Manage Requests");
  const tableBody = document.querySelector("#requests-table tbody");
  const message = document.getElementById("requests-message");
  tableBody.innerHTML = "";
  message.innerText = "";

  try {
    const response = await fetch("/api/admin/requests");
    const requests = await response.json();
    if (requests.length === 0) {
      message.innerText = "No requests found.";
      return;
    }
    requests.forEach((req) => {
      const row = document.createElement("tr");
      row.innerHTML = `
                <td>${req.user_id}</td>
                <td>${req.name}</td>
                <td>${req.service.type}</td>
                <td>${req.service.status}</td>
                <td><pre>${JSON.stringify(
                  req.service.connection_details || {},
                  null,
                  2
                )}</pre></td>
            `;
      tableBody.appendChild(row);
    });
  } catch (error) {
    message.innerText = "Error fetching requests";
  } finally {
    hideLoading("manageRequests", "Manage Requests");
  }
}

// Admin: View bill details
async function viewAllBills() {
  showLoading("viewAllBills", "View Bill Details");
  const tableBody = document.querySelector("#bills-table tbody");
  const message = document.getElementById("bills-message");
  tableBody.innerHTML = "";
  message.innerText = "";

  try {
    const response = await fetch("/api/admin/bills");
    const bills = await response.json();
    if (bills.length === 0) {
      message.innerText = "No bills found.";
      return;
    }
    bills.forEach((bill) => {
      const row = document.createElement("tr");
      row.innerHTML = `
                <td>${bill.user_id}</td>
                <td>${bill.name}</td>
                <td>${bill.bill.month}</td>
                <td>${bill.bill.amount}</td>
                <td>${bill.bill.paid ? "Yes" : "No"}</td>
            `;
      tableBody.appendChild(row);
    });
  } catch (error) {
    message.innerText = "Error fetching bills";
  } finally {
    hideLoading("viewAllBills", "View Bill Details");
  }
}

// Admin: Track complaints
async function trackAllComplaints() {
  showLoading("trackAllComplaints", "Track Complaints");
  const tableBody = document.querySelector("#complaints-table tbody");
  const message = document.getElementById("complaints-message");
  tableBody.innerHTML = "";
  message.innerText = "";

  try {
    const response = await fetch("/api/admin/complaints");
    const complaints = await response.json();
    if (complaints.length === 0) {
      message.innerText = "No complaints found.";
      return;
    }
    complaints.forEach((complaint) => {
      const row = document.createElement("tr");
      // Handle complaint as string or object
      const complaintText =
        typeof complaint.complaint === "string"
          ? complaint.complaint
          : complaint.complaint?.complaint_text || "Unknown complaint";
      row.innerHTML = `
                <td>${complaint.user_id}</td>
                <td>${complaint.name}</td>
                <td>${complaintText}</td>
            `;
      tableBody.appendChild(row);
    });
  } catch (error) {
    message.innerText = "Error fetching complaints";
  } finally {
    hideLoading("trackAllComplaints", "Track Complaints");
  }
}

// Admin: Search user
document
  .getElementById("search-form")
  ?.addEventListener("submit", async (e) => {
    e.preventDefault();
    showLoading("search-form", "Search");
    const tableBody = document.querySelector("#search-table tbody");
    const message = document.getElementById("search-message");
    const search_type = document.getElementById("search_type").value;
    const query = document.getElementById("query").value;
    tableBody.innerHTML = "";
    message.innerText = "";

    try {
      const response = await fetch(
        `/api/admin/search?search_type=${search_type}&query=${query}`
      );
      const user = await response.json();
      if (user.error) {
        message.innerText = `Error: ${user.error}`;
        return;
      }
      const row = document.createElement("tr");
      row.innerHTML = `
            <td>${user.user_id}</td>
            <td>${user.username}</td>
            <td>${user.name}</td>
            <td>${user.address}</td>
            <td>${user.meter_id || "N/A"}</td>
            <td>${user.role}</td>
        `;
      tableBody.appendChild(row);
    } catch (error) {
      message.innerText = "Error searching user";
    } finally {
      hideLoading("search-form", "Search");
    }
  });
