const API = "/api/v1";
const state = { token: localStorage.getItem("wallet_token"), wallets: [], operations: [], modalMode: "wallet" };
const $ = (id) => document.getElementById(id);
const authScreen = $("auth-screen"), app = $("app");

function notify(message, isError = false) {
  const toast = $("toast");
  toast.textContent = message;
  toast.className = `toast show${isError ? " error" : ""}`;
  clearTimeout(notify.timer);
  notify.timer = setTimeout(() => toast.className = "toast", 3200);
}
function setAuth(token) {
  state.token = token;
  localStorage.setItem("wallet_token", token);
  $("user-name").textContent = token;
  $("user-avatar").textContent = token.slice(0, 1).toUpperCase();
  authScreen.classList.add("hidden");
  app.classList.remove("hidden");
}
function logout() {
  localStorage.removeItem("wallet_token");
  state.token = null;
  app.classList.add("hidden");
  authScreen.classList.remove("hidden");
  $("login-input").value = "";
}
async function request(path, options = {}) {
  const headers = { ...(options.body ? { "Content-Type": "application/json" } : {}), ...(state.token ? { Authorization: `Bearer ${state.token}` } : {}), ...options.headers };
  const response = await fetch(`${API}${path}`, { ...options, headers });
  const raw = await response.text();
  let data = null;
  try { data = raw ? JSON.parse(raw) : null; } catch { data = raw; }
  if (!response.ok) {
    const detail = data?.detail;
    throw new Error(typeof detail === "string" ? detail : detail ? JSON.stringify(detail) : `Ошибка ${response.status}`);
  }
  return data;
}
function currency(value) {
  const code = String(value || "rub").toUpperCase();
  const symbols = { RUB: "₽", USD: "$", EUR: "€" };
  return symbols[code] || code;
}
function money(value, code = "rub") {
  const number = Number(value || 0);
  return `${number.toLocaleString("ru-RU", { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ${currency(code)}`;
}
function dateFormat(value) {
  if (!value) return "—";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "—" : date.toLocaleDateString("ru-RU", { day: "2-digit", month: "short", year: "numeric" });
}
function pluralWallet(n) {
  const mod10 = n % 10, mod100 = n % 100;
  return `${n} ${mod100 >= 11 && mod100 <= 14 ? "кошельков" : mod10 === 1 ? "кошелёк" : mod10 >= 2 && mod10 <= 4 ? "кошелька" : "кошельков"}`;
}
async function loadDashboard() {
  try {
    const [wallets, operations, total] = await Promise.all([
      request("/wallets"), request("/operations"), request("/balance")
    ]);
    state.wallets = wallets || [];
    state.operations = operations || [];
    $("total-balance").textContent = money(total?.total_balance, "rub");
    $("wallet-count").textContent = pluralWallet(state.wallets.length);
    renderWallets();
    renderOperations();
  } catch (error) {
    if (/401|Unauthorized/i.test(error.message)) logout();
    notify(error.message || "Не удалось загрузить данные", true);
  }
}
function renderWallets() {
  const root = $("wallet-list");
  if (!state.wallets.length) {
    root.innerHTML = `<div class="empty-state">Пока нет кошельков. Создайте первый, чтобы начать вести финансы.</div>`;
    return;
  }
  root.innerHTML = state.wallets.map(wallet => `
    <article class="wallet-card">
      <div class="wallet-top"><div class="wallet-icon">▣</div><span class="currency-tag">${String(wallet.currency).toUpperCase()}</span></div>
      <div class="wallet-name">${escapeHtml(wallet.name)}</div>
      <div class="wallet-amount">${money(wallet.balance, wallet.currency)}</div>
      <div class="wallet-actions">
        <button class="mini-action" data-action="income" data-id="${wallet.id}">＋ Пополнить</button>
        <button class="mini-action" data-action="expense" data-id="${wallet.id}">− Списать</button>
        <button class="mini-action" data-action="transfer" data-id="${wallet.id}">↗ Перевод</button>
      </div>
    </article>`).join("");
  root.querySelectorAll("[data-action]").forEach(button => button.addEventListener("click", () => {
    const wallet = state.wallets.find(item => item.id === Number(button.dataset.id));
    if (button.dataset.action === "transfer") openModal("transfer", wallet);
    else openModal(button.dataset.action, wallet);
  }));
}
function renderOperations() {
  const root = $("operations-list");
  const walletById = new Map(state.wallets.map(wallet => [wallet.id, wallet]));
  const items = [...state.operations].sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).slice(0, 10);
  if (!items.length) {
    root.innerHTML = `<tr><td colspan="4" class="table-empty">Операций пока нет — они появятся здесь.</td></tr>`;
    return;
  }
  root.innerHTML = items.map(operation => {
    const type = String(operation.type || "").toLowerCase();
    const isIncome = type === "income";
    const isTransfer = type === "transfer";
    const wallet = walletById.get(operation.wallet_id);
    const label = isIncome ? "Пополнение" : isTransfer ? "Перевод" : "Расход";
    const icon = isIncome ? "↙" : isTransfer ? "↗" : "↗";
    const sign = isIncome ? "+" : isTransfer ? "" : "−";
    const cls = isIncome ? "income" : isTransfer ? "transfer" : "expense";
    const description = operation.category || label;
    return `<tr><td><div class="operation-cell"><span class="operation-icon ${cls}">${icon}</span><span>${escapeHtml(description)}</span></div></td><td>${escapeHtml(wallet?.name || `Кошелёк #${operation.wallet_id}`)}</td><td>${dateFormat(operation.created_at)}</td><td class="align-right amount-${cls}">${sign}${money(operation.amount, operation.currency)}</td></tr>`;
  }).join("");
}
function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
}
function showModal() { $("modal-backdrop").classList.remove("hidden"); }
function closeModal() { $("modal-backdrop").classList.add("hidden"); $("modal-form").reset(); }
function fillWalletSelect(select, selectedId) {
  select.innerHTML = state.wallets.map(wallet => `<option value="${wallet.id}" ${wallet.id === selectedId ? "selected" : ""}>${escapeHtml(wallet.name)} · ${String(wallet.currency).toUpperCase()}</option>`).join("");
}
function openModal(mode, wallet = null) {
  state.modalMode = mode;
  const isWallet = mode === "wallet";
  const isTransfer = mode === "transfer";
  $("wallet-fields").classList.toggle("hidden", !isWallet);
  $("operation-fields").classList.toggle("hidden", isWallet || isTransfer);
  $("transfer-fields").classList.toggle("hidden", !isTransfer);
  // Управляем доступностью полей в зависимости от типа операции
  [
      "wallet-fields",
      "operation-fields",
      "transfer-fields"
  ].forEach(id => {
      const section = $(id);
      const isHidden = section.classList.contains("hidden");

      section.querySelectorAll("input, select, textarea").forEach(field => {
          field.disabled = isHidden;
      });
  });
  $("modal-eyebrow").textContent = isWallet ? "НОВЫЙ КОШЕЛЁК" : isTransfer ? "МЕЖДУ СЧЕТАМИ" : "НОВАЯ ОПЕРАЦИЯ";
  $("modal-title").textContent = isWallet ? "Создать кошелёк" : isTransfer ? "Перевести средства" : mode === "income" ? "Пополнить кошелёк" : "Добавить расход";
  $("modal-description").textContent = isWallet ? "Добавьте новый счёт, чтобы отслеживать его баланс." : isTransfer ? "Выберите кошельки и укажите сумму перевода." : "Заполните детали операции.";
  $("modal-submit").innerHTML = `${isWallet ? "Создать кошелёк" : isTransfer ? "Перевести" : "Подтвердить"} <span>→</span>`;
  if (!isWallet) {
    fillWalletSelect($("operation-wallet"), wallet?.id);
    fillWalletSelect($("from-wallet"), wallet?.id);
    fillWalletSelect($("to-wallet"), state.wallets.find(w => w.id !== wallet?.id)?.id);
  }
  showModal();
}
async function submitModal(event) {
  event.preventDefault();
  const button = $("modal-submit");
  button.disabled = true;
  try {
    if (state.modalMode === "wallet") {
      await request("/wallets", { method: "POST", body: JSON.stringify({ name: $("wallet-name").value.trim(), currency: $("wallet-currency").value, initial_balance: Number($("wallet-balance").value) }) });
      notify("Кошелёк успешно создан");
    } else if (state.modalMode === "transfer") {
      await request("/operations/transfer", { method: "POST", body: JSON.stringify({ from_wallet_id: Number($("from-wallet").value), to_wallet_id: Number($("to-wallet").value), amount: Number($("transfer-amount").value) }) });
      notify("Перевод выполнен");
    } else {
      const wallet = state.wallets.find(w => w.id === Number($("operation-wallet").value));
      await request(`/operations/${state.modalMode}`, { method: "POST", body: JSON.stringify({ wallet_name: wallet.name, amount: Number($("operation-amount").value), description: $("operation-description").value.trim() || null }) });
      notify(state.modalMode === "income" ? "Кошелёк пополнен" : "Расход добавлен");
    }
    closeModal();
    await loadDashboard();
  } catch (error) {
    notify(error.message || "Не удалось выполнить операцию", true);
  } finally {
    button.disabled = false;
  }
}
$("auth-form").addEventListener("submit", async event => {
  event.preventDefault();
  const login = $("login-input").value.trim();
  if (!login) return;
  const submit = event.submitter;
  submit.disabled = true;
  try {
    // Текущая backend-схема использует login как Bearer credential.
    state.token = login;
    try {
      await request("/users/me");
    } catch (error) {
      if (!/401|Unauthorized/i.test(error.message)) throw error;
      await request("/users", { method: "POST", body: JSON.stringify({ login }) });
    }
    setAuth(login);
    await loadDashboard();
  } catch (error) {
    state.token = null;
    notify(error.message || "Не удалось войти", true);
  } finally {
    submit.disabled = false;
  }
});
$("logout-btn").addEventListener("click", logout);
$("add-wallet-open").addEventListener("click", () => openModal("wallet"));
$("add-wallet-inline").addEventListener("click", () => openModal("wallet"));
$("refresh-btn").addEventListener("click", loadDashboard);
$("modal-close").addEventListener("click", closeModal);
$("modal-backdrop").addEventListener("click", event => { if (event.target === $("modal-backdrop")) closeModal(); });
$("modal-form").addEventListener("submit", submitModal);
document.addEventListener("keydown", event => { if (event.key === "Escape") closeModal(); });

if (state.token) {
  setAuth(state.token);
  loadDashboard();
}
