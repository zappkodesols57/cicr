const state = {
  view: "home",
  aboutTab: "app",
  heroIndex: 0,
  historyReady: false,
  varietyZone: null,
  varietyItem: null,
  detailSlug: null,
  advisoryPage: 1,
};

const API_BASE = "http://128.199.7.234";
const API = {
  banners: `${API_BASE}/api/banners/`,
  advisory: `${API_BASE}/api/advisory/`,
  news: `${API_BASE}/api/news-articles/list/`,
};

const navItems = [
  ["about", "i", "About CICR"],
  ["contact", "tel", "Contact Us"],
  ["home", "home", "Home"],
  ["advisory", "bell", "Advisory"],
  ["aboutApp", "cal", "About App"],
];

const desktopNavItems = [
  ["home", "Home"],
  ["about", "About CICR"],
  ["advisory", "Advisory"],
  ["contact", "Contact Us"],
  ["aboutApp", "About App"],
];

const drawerItems = [
  ...navItems,
  ["varieties", "leaf", "Varieties and Hybrids"],
  ["cultivars", "leaf", "Cultivars of SAUs"],
  ["production", "tractor", "Production Technology"],
  ["protection", "shield", "Protection Technology"],
  ["facts", "chart", "Facts and Figures"],
  ["gallery", "image", "Gallery"],
];

const pageTitles = {
  home: "Home",
  about: "About CICR",
  contact: "Contact Us",
  advisory: "Advisory",
  aboutApp: "About App",
  varieties: "Varieties and Hybrids",
  cultivars: "Cultivars of SAUs",
  production: "Production Technology",
  protection: "Protection Technology",
  facts: "Facts and Figures",
  gallery: "Gallery",
  outreach: "Farmers Outreach",
  cottonTech: "Cotton Technology",
  news: "Cotton News",
};

const featureCards = [
  ["varieties", "leaf", "Varieties and Hybrids", "#4caf50"],
  ["cultivars", "leaf", "Cultivars of SAUs", "#8bc34a"],
  ["production", "tractor", "Production Technology", "#ff9800"],
  ["protection", "shield", "Protection Technology", "#f44336"],
  ["advisory", "bell", "Weekly Advisory For Cotton Cultivation", "#4caf50"],
  ["facts", "chart", "Facts and Figures", "#2196f3"],
  ["gallery", "image", "Gallery", "#e91e63"],
  ["outreach", "users", "Farmers Outreach", "#009688"],
  ["cottonTech", "flask", "Cotton Technology", "#3f51b5"],
  ["news", "news", "Cotton News", "#795548"],
];

const view = document.querySelector("#view");
const pageTitle = document.querySelector("#pageTitle");
const subHeader = document.querySelector("#subHeader");
const bottomNav = document.querySelector("#bottomNav");
const drawerNav = document.querySelector("#drawerNav");
const drawer = document.querySelector("#drawer");
const drawerScrim = document.querySelector("#drawerScrim");
const pageFooter = document.querySelector("#pageFooter");
const APP_BASE_PATH = "/cotton_app/";

function slugifyRoute(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function pathForState(viewId = state.view, zone = state.varietyZone, varietyItem = state.varietyItem, detailSlug = state.detailSlug) {
  if (viewId === "home" && !zone) return APP_BASE_PATH;
  if (viewId === "varieties" && zone && varietyItem) return `${APP_BASE_PATH}varieties-${slugifyRoute(zone)}/${varietyItem}/`;
  if (viewId === "varieties" && zone) return `${APP_BASE_PATH}varieties-${slugifyRoute(zone)}/`;
  if (detailSlug) return `${APP_BASE_PATH}${viewId}/${detailSlug}/`;
  return `${APP_BASE_PATH}${viewId}/`;
}

function routeFromLocation() {
  const cleanPath = location.pathname.replace(APP_BASE_PATH, "").replace(/^\/+|\/+$/g, "");
  return cleanPath || location.hash.replace("#", "") || "home";
}

function assetPath(path) {
  if (!path) return "";
  const raw = String(path).replace(/\\/g, "/").trim();
  if (/^(https?:|data:|blob:)/i.test(raw)) return raw;
  const cleaned = raw
    .replace(/^\/+/, "")
    .replace(/^(\.\.\/)+/, "")
    .replace(/^\.?\//, "")
    .replace(/^CICR-Cotton-main\/assets\//i, "assets/")
    .replace(/^CICR-Cotton-webapp\//i, "");
  return `${APP_BASE_PATH}${cleaned}`;
}

function icon(name) {
  const icons = {
    i: "i",
    tel: "Tel",
    home: "Home",
    bell: "Alert",
    cal: "App",
    leaf: "Leaf",
    tractor: "CR",
    shield: "Safe",
    chart: "Bar",
    image: "Img",
    users: "Grp",
    flask: "Lab",
    news: "News",
    pin: "Pin",
    phone: "Tel",
    fax: "Fax",
    web: "Web",
    mail: "Mail",
  };
  return icons[name] || "-";
}

function init() {
  const initialView = routeFromLocation();
  const varietyRoute = parseVarietyRoute(initialView);
  if (varietyRoute.zone) {
    state.view = "varieties";
    state.varietyZone = varietyRoute.zone;
    state.varietyItem = varietyRoute.item;
  } else {
    const detailRoute = parseDetailRoute(initialView);
    if (pageTitles[detailRoute.view] || ["outreach", "cottonTech", "news"].includes(detailRoute.view)) {
      state.view = detailRoute.view;
      state.detailSlug = detailRoute.slug;
    }
  }
  bottomNav.innerHTML = navItems.map(navButton).join("");
  drawerNav.innerHTML = drawerItems.map(drawerButton).join("");
  document.querySelector("#desktopNav").innerHTML = desktopNavItems.map(([id, label]) => `<button data-view="${id}">${label}</button>`).join("");

  bottomNav.addEventListener("click", onNavClick);
  drawerNav.addEventListener("click", onNavClick);
  pageFooter.addEventListener("click", onNavClick);
  document.querySelector("#desktopNav").addEventListener("click", onNavClick);
  document.querySelector(".desktop-brand").addEventListener("click", onNavClick);
  document.querySelector("#menuBtn").addEventListener("click", openDrawer);
  drawerScrim.addEventListener("click", closeDrawer);
  document.querySelector("#desktopA11y").addEventListener("click", () => document.querySelector("#a11yPanel").classList.toggle("open"));
  document.querySelector("#desktopLanguageSelect").addEventListener("change", (event) => {
    document.querySelector("#languageSelect").value = event.target.value;
  });
  setupAccessibility();
  setupImageLightbox();
  window.addEventListener("popstate", (event) => {
    const routeView = routeFromLocation();
    const varietyRoute = parseVarietyRoute(routeView);
    const detailRoute = parseDetailRoute(routeView);
    state.view = event.state?.view || (varietyRoute.zone ? "varieties" : detailRoute.view) || "home";
    state.varietyZone = event.state?.varietyZone || varietyRoute.zone || null;
    state.varietyItem = event.state?.varietyItem || varietyRoute.item || null;
    state.detailSlug = event.state?.detailSlug !== undefined ? event.state.detailSlug : (detailRoute.slug || null);
    closeDrawer();
    render();
  });
  history.replaceState({ view: state.view, varietyZone: state.varietyZone, varietyItem: state.varietyItem, detailSlug: state.detailSlug }, "", pathForState());
  state.historyReady = true;
  render();
  fetchLiveData();

  setInterval(() => {
    state.heroIndex = (state.heroIndex + 1) % appData.banners.length;
    if (state.view === "home") renderHeroOnly();
  }, 3800);
}

function navButton([id, iconName, label]) {
  return `<button class="bottom-item" data-view="${id}">
    <span class="nav-icon">${icon(iconName)}</span>
    <span class="nav-label">${label}</span>
  </button>`;
}

function drawerButton([id, iconName, label]) {
  return `<button data-view="${id}"><span>${icon(iconName)}</span>${label}</button>`;
}

function onNavClick(event) {
  const button = event.target.closest("[data-view]");
  if (!button) return;
  setView(button.dataset.view);
}

function setView(id) {
  if (id === state.view && !(id === "varieties" && (state.varietyZone || state.varietyItem)) && !state.detailSlug) return;
  state.view = id;
  if (id !== "varieties") {
    state.varietyZone = null;
    state.varietyItem = null;
  } else {
    state.varietyItem = null;
  }
  state.detailSlug = null;
  if (state.historyReady) {
    history.pushState({ view: state.view, varietyZone: state.varietyZone, varietyItem: state.varietyItem, detailSlug: null }, "", pathForState());
  }
  closeDrawer();
  render();
}

function parseVarietyZoneHash(hashValue) {
  const normalized = String(hashValue || "").toLowerCase();
  return {
    "varieties-north-zone": "North Zone",
    "varieties-central-zone": "Central Zone",
    "varieties-south-zone": "South Zone",
  }[normalized] || null;
}

function parseVarietyRoute(routeValue) {
  const parts = String(routeValue || "").toLowerCase().replace(/^\/+|\/+$/g, "").split("/");
  const zone = parseVarietyZoneHash(parts[0]);
  return { zone, item: zone ? parts[1] || null : null };
}

function parseDetailRoute(routeValue) {
  const parts = String(routeValue || "").replace(/^\/+|\/+$/g, "").split("/");
  return { view: parts[0], slug: parts[1] || null };
}

function itemSlug(item) {
  return slugifyRoute(item.detailTitle || item.name);
}

function varietiesInZone(zone = state.varietyZone) {
  return appData.varieties.filter((item) => item.category === zone);
}

function findVarietyBySlug(slug, zone = state.varietyZone) {
  return varietiesInZone(zone).find((item) => itemSlug(item) === slug) || null;
}

async function fetchLiveData() {
  const [banners, advisories, news] = await Promise.allSettled([
    fetchJson(API.banners),
    fetchJson(API.advisory),
    fetchJson(API.news),
  ]);

  if (banners.status === "fulfilled") {
    const liveBanners = normalizeBanners(banners.value);
    if (liveBanners.length) appData.banners = liveBanners;
  }

  if (advisories.status === "fulfilled") {
    const liveAdvisories = normalizeAdvisories(advisories.value);
    if (liveAdvisories.length) appData.liveAdvisories = liveAdvisories;
  }

  if (news.status === "fulfilled") {
    const liveNews = normalizeNews(news.value);
    if (liveNews.length) appData.liveNews = liveNews;
  }

  if (["home", "advisory", "news"].includes(state.view)) render();
}

async function fetchJson(url) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 12000);
  const response = await fetch(url, { cache: "no-store", signal: controller.signal });
  clearTimeout(timeout);
  if (!response.ok) throw new Error(`Request failed: ${url}`);
  return response.json();
}

function normalizeBanners(payload) {
  const rows = Array.isArray(payload?.banners) ? payload.banners : [];
  return rows
    .map((item) => item.image_url ? `${API_BASE}${item.image_url}` : "")
    .filter(Boolean);
}

function normalizeAdvisories(payload) {
  const rows = Array.isArray(payload?.value) ? payload.value : [];
  return rows.map((item) => {
    const langs = [
      ["English", item.path_pdf_en],
      ["Hindi", item.path_pdf_hi],
      ["Gujarati", item.path_pdf_gu],
      [item.lang_1, item.lang_1_pdf],
      [item.lang_2, item.lang_2_pdf],
      [item.lang_3, item.lang_3_pdf],
      [item.lang_4, item.lang_4_pdf],
      [item.lang_5, item.lang_5_pdf],
      [item.lang_6, item.lang_6_pdf],
      [item.lang_7, item.lang_7_pdf],
    ]
      .map(([label, file]) => [label, normalizePdfUrl(file)])
      .filter(([label, file]) => label && file && label !== "Select language");

    return {
      week: item.week_en || "-",
      title: item.date_range_en || "Weekly Advisory",
      date: item.start_date_en || "-",
      month: item.month_en || "-",
      languages: langs,
      file: normalizePdfUrl(item.path_pdf_en) || langs[0]?.[1] || "",
    };
  });
}

function normalizePdfUrl(file) {
  if (!file) return "";
  if (/^https?:\/\//i.test(file)) return file;
  return `${API_BASE}${String(file).startsWith("/") ? "" : "/"}${file}`;
}

function normalizeNews(payload) {
  const rows = Array.isArray(payload?.value) ? payload.value : [];
  return rows.map((item) => ({
    name: `Cotton News Issue ${item.issue_no || ""}`.trim(),
    description: `${item.month || ""} ${item.date || ""}`.trim(),
    file: item.pdf,
  }));
}

function openDrawer() {
  drawer.classList.add("open");
  drawerScrim.classList.add("open");
}

function closeDrawer() {
  drawer.classList.remove("open");
  drawerScrim.classList.remove("open");
}

function setActiveNav() {
  document.body.classList.toggle("is-home", state.view === "home");
  document.querySelectorAll("[data-view]").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === state.view);
  });
}

function render() {
  pageTitle.textContent = pageTitles[state.view] || "Home";
  setActiveNav();
  renderSubHeader();

  const routes = {
    home: renderHome,
    about: renderAboutCicr,
    contact: renderContact,
    advisory: renderAdvisory,
    aboutApp: renderAboutApp,
    varieties: renderVarieties,
    cultivars: renderCultivars,
    production: () => renderCollection("production", appData.production),
    protection: renderProtection,
    facts: () => renderCollection("facts", appData.facts),
    gallery: renderGallery,
    outreach: renderOutreach,
    cottonTech: renderCottonTech,
    news: renderNews,
  };
  (routes[state.view] || renderHome)();
  renderPageTrail();
}

function renderPageTrail() {
  view.querySelector(".page-trail")?.remove();
  view.querySelector(".page-crumbs")?.remove();
  if (state.view === "home") return;

  const currentVariety = state.varietyItem ? findVarietyBySlug(state.varietyItem) : null;
  const currentDetail = !currentVariety && state.detailSlug ? findDetailItem(state.view, state.detailSlug) : null;
  const currentTitle = currentVariety?.name || currentDetail?.name || state.varietyZone || pageTitles[state.view] || "Page";
  const trail = document.createElement("nav");
  trail.className = "page-trail";
  trail.setAttribute("aria-label", "Breadcrumb");
  trail.innerHTML = `
    <button class="trail-back" type="button" aria-label="Go back">←</button>
    <div class="trail-crumbs">
      <button type="button" data-view="home">Home</button>
      <span>/</span>
      ${state.varietyZone ? `<button type="button" data-view="varieties">Varieties and Hybrids</button><span>/</span>` : ""}
      ${state.varietyZone && state.varietyItem ? `<button type="button" data-zone-link="${state.varietyZone}">${state.varietyZone}</button><span>/</span>` : ""}
      ${currentDetail ? `<button type="button" data-detail-back="${state.view}">${pageTitles[state.view] || "Back"}</button><span>/</span>` : ""}
      <strong>${currentTitle}</strong>
    </div>
  `;
  view.prepend(trail);
  trail.querySelector(".trail-back").addEventListener("click", goBack);
  trail.querySelectorAll("[data-view]").forEach((el) => el.addEventListener("click", onNavClick));
  trail.querySelectorAll("[data-zone-link]").forEach((el) => {
    el.addEventListener("click", () => openVarietyZone(el.dataset.zoneLink));
  });
  trail.querySelectorAll("[data-detail-back]").forEach((el) => {
    el.addEventListener("click", () => closeDetail(el.dataset.detailBack));
  });
}

function goBack() {
  if (state.varietyItem) {
    openVarietyZone(state.varietyZone);
    return;
  }
  if (state.varietyZone) {
    openVarietyZone(null);
    return;
  }
  if (state.detailSlug) {
    closeDetail(state.view);
    return;
  }
  if (history.length > 1) {
    history.back();
    return;
  }
  setView("home");
}

function renderSubHeader() {
  if (state.view === "aboutApp") {
    subHeader.innerHTML = `<div class="tabbar">
      <button data-about-tab="app" class="${state.aboutTab === "app" ? "active" : ""}">About App</button>
      <button data-about-tab="developers" class="${state.aboutTab === "developers" ? "active" : ""}">About Developers</button>
    </div>`;
    subHeader.querySelectorAll("[data-about-tab]").forEach((button) => {
      button.addEventListener("click", () => {
        state.aboutTab = button.dataset.aboutTab;
        render();
      });
    });
    return;
  }
  if (state.view === "contact") {
    subHeader.innerHTML = `<div class="sub-title">ICAR - CICR</div>`;
    return;
  }
  if (state.view === "advisory") {
    subHeader.innerHTML = `<div class="sub-title">Weekly Advisory For Cotton Cultivation</div>`;
    return;
  }
  subHeader.innerHTML = "";
}

function renderHeroOnly() {
  const img = document.querySelector(".hero-slider img, .landing-hero-media img");
  if (img) img.src = appData.banners[state.heroIndex];
  document.querySelectorAll(".dots span").forEach((dot, index) => {
    dot.classList.toggle("active", index === state.heroIndex);
  });
}

function renderHome() {
  view.className = "landing-view";
  view.innerHTML = `
    <section class="landing-hero">
      <div class="landing-copy">
        <h2>Empowering Cotton Farming<br>Through Research</h2>
        <p>Your comprehensive guide to cotton farming</p>
        <div class="landing-buttons">
          <button class="landing-primary" data-view="varieties">Explore Research <span>-></span></button>
          <button class="landing-secondary" data-view="advisory">Weekly Advisory <span>-></span></button>
        </div>
      </div>
      <div class="landing-hero-media">
      <img src="${assetPath(appData.banners[state.heroIndex])}" alt="Cotton research field visit">
        <div class="dots">${appData.banners.map((_, i) => `<span class="${i === state.heroIndex ? "active" : ""}"></span>`).join("")}</div>
      </div>
    </section>
    <section class="landing-resources">
      <h2>Explore Cotton Research & Resources</h2>
      <p>Access our research, technologies and resources to enhance cotton productivity and sustainability.</p>
      <div class="resource-grid">
      ${featureCards.map(([target, iconName, title, color]) => `
        <article class="resource-card" data-view="${target}" style="--accent:${color};--soft:${soft(color)}">
          <span class="resource-icon">${featureIcon(target, iconName)}</span>
          <div>
            <h3>${title}</h3>
            <p>${resourceDescription(target)}</p>
          </div>
          <span class="resource-arrow">-></span>
        </article>`).join("")}
      </div>
    </section>
    <section class="landing-strip">
      <span class="brand-mark">CR</span>
      <h2>CICR Cotton Research</h2>
      <p>Your comprehensive guide to cotton farming</p>
    </section>
  `;
  view.querySelectorAll("[data-view]").forEach((el) => el.addEventListener("click", onNavClick));
}

function renderVarieties() {
  view.className = "content varieties-view";
  if (!state.varietyZone) {
    const zones = [
      {
        name: "North Zone",
        region: "Punjab, Haryana, Rajasthan and nearby regions",
        accent: "#ff8f1f",
        badge: "North cotton belt",
      },
      {
        name: "Central Zone",
        region: "Maharashtra, Madhya Pradesh, Gujarat and nearby regions",
        accent: "#21a844",
        badge: "Major cotton belt",
      },
      {
        name: "South Zone",
        region: "Telangana, Andhra Pradesh, Karnataka, Tamil Nadu and nearby regions",
        accent: "#2196f3",
        badge: "South cotton belt",
      },
    ];
    view.innerHTML = `
      <section class="variety-hero">
        <div>
          <h2>Varieties and Hybrids</h2>
          <p>Explore region-specific cotton varieties developed for diverse agro-climatic conditions across India.</p>
        </div>
        <div class="cotton-line-art">Cotton</div>
      </section>
      <section class="zone-heading">
        <h3>Select Your Cotton-Growing Zone</h3>
        <p>Choose a zone to view recommended cotton varieties and hybrids.</p>
      </section>
      <section class="zone-grid">
        ${zones.map((zone) => `
          <button class="zone-card" data-zone="${zone.name}" style="--zone:${zone.accent}">
            <span class="zone-icon">${zone.name}</span>
            <span class="zone-copy">
              <strong>${zone.name}</strong>
              <small>${zone.region}</small>
            </span>
            <span class="zone-badge">${zone.badge}</span>
            <span class="zone-foot"><em>${appData.varieties.filter((item) => item.category === zone.name).length}+ varieties</em><b>Explore Zone -></b></span>
          </button>
        `).join("")}
      </section>
      <section class="variety-tip-strip">
        <span class="tip-icon">Target</span>
        <div>
          <strong>Find the right variety for your region</strong>
          <p>Our zone-wise recommendations help you make informed decisions for better yields.</p>
        </div>
        <span>Region-specific recommendations</span>
        <span>Research-backed information</span>
        <span>Easy comparison</span>
      </section>
    `;
    view.querySelectorAll("[data-view]").forEach((el) => el.addEventListener("click", onNavClick));
    view.querySelectorAll("[data-zone]").forEach((button) => {
      button.addEventListener("click", () => {
        openVarietyZone(button.dataset.zone);
      });
    });
    return;
  }

  const items = varietiesInZone();
  if (state.varietyItem) {
    const item = findVarietyBySlug(state.varietyItem);
    if (item) {
      renderVarietyDetail(item, items);
      return;
    }
    state.varietyItem = null;
  }
  view.innerHTML = `
    <section class="zone-heading with-back">
      <button class="inline-back" id="zoneBack">Back</button>
      <div>
        <h2>${state.varietyZone}</h2>
        <p>${items.length} varieties and hybrids available.</p>
      </div>
    </section>
    <div class="collection-grid">${items.map(dataCard).join("")}</div>
  `;
  document.querySelector("#zoneBack").addEventListener("click", () => openVarietyZone(null));
  bindDataCards(items, (item) => openVarietyDetail(item));
}

function openVarietyZone(zone) {
  state.view = "varieties";
  state.varietyZone = zone;
  state.varietyItem = null;
  state.detailSlug = null;
  if (state.historyReady) {
    history.pushState({ view: "varieties", varietyZone: zone, varietyItem: null, detailSlug: null }, "", pathForState("varieties", zone, null));
  }
  closeDrawer();
  render();
}

function openVarietyDetail(itemOrSlug) {
  const slug = typeof itemOrSlug === "string" ? itemOrSlug : itemSlug(itemOrSlug);
  state.view = "varieties";
  state.varietyItem = slug;
  if (state.historyReady) {
    history.pushState({ view: "varieties", varietyZone: state.varietyZone, varietyItem: slug, detailSlug: null }, "", pathForState("varieties", state.varietyZone, slug));
  }
  render();
}

function openDetail(viewId, item) {
  if (!item) return;
  state.view = viewId;
  state.detailSlug = itemSlug(item);
  if (state.historyReady) {
    history.pushState({ view: viewId, varietyZone: null, varietyItem: null, detailSlug: state.detailSlug }, "", pathForState(viewId, null, null, state.detailSlug));
  }
  render();
  window.scrollTo({ top: 0, behavior: "auto" });
}

function closeDetail(viewId) {
  state.view = viewId;
  state.detailSlug = null;
  if (state.historyReady) {
    history.pushState({ view: viewId, varietyZone: null, varietyItem: null, detailSlug: null }, "", pathForState(viewId, null, null, null));
  }
  render();
}

function renderVarietyDetail(item, items) {
  const title = item.detailTitle || item.name;
  const currentIndex = Math.max(0, items.findIndex((entry) => itemSlug(entry) === itemSlug(item)));
  const previous = items[(currentIndex - 1 + items.length) % items.length];
  const next = items[(currentIndex + 1) % items.length];
  view.className = "content wide variety-detail-page";
  view.innerHTML = `
    <section class="variety-detail-panel">
      <div class="variety-detail-copy">
        <button class="inline-back" id="zoneBack">Back to ${state.varietyZone}</button>
        <span>${state.varietyZone}</span>
        <h2>${title}</h2>
        <p>${item.description || "Cotton variety or hybrid available in CICR Cotton mobile app assets."}</p>
        ${renderVarietyPointList(item)}
      </div>
      ${item.image ? `
        <figure class="variety-detail-figure">
          <img src="${assetPath(item.image)}" alt="${title}">
          <figcaption>${title}</figcaption>
        </figure>
      ` : ""}
    </section>
    ${item.sections ? renderSections(item.sections) : ""}
    <section class="variety-detail-actions">
      <button class="outline-link" type="button" data-variety-link="${itemSlug(previous)}">
        <small>Previous</small><span>${previous.name}</span>
      </button>
      <button class="solid-link" type="button" data-variety-link="${itemSlug(next)}">
        <small>Next</small><span>${next.name}</span>
      </button>
    </section>
  `;
  view.querySelector("#zoneBack").addEventListener("click", () => openVarietyZone(state.varietyZone));
  view.querySelectorAll("[data-variety-link]").forEach((button) => {
    button.addEventListener("click", () => openVarietyDetail(button.dataset.varietyLink));
  });
}

function renderVarietyPointList(item) {
  const rows = item.details && item.details.length
    ? item.details
    : [["Overview", item.description || "Cotton variety or hybrid available in CICR Cotton mobile app assets."]];
  return `
    <ul class="variety-point-list">
      ${rows.map(([label, value]) => `
        <li>
          <span class="point-check">&#10003;</span>
          <div>
            <strong>${label}</strong>
            <p>${value}</p>
          </div>
        </li>
      `).join("")}
    </ul>
  `;
}

function renderCultivars() {
  view.className = "content wide";
  const zones = ["North Zone", "Central Zone", "South Zone"];
  view.innerHTML = `
    <section class="zone-heading">
      <h3>Cultivars of SAUs</h3>
      <p>Cotton cultivars released by State Agricultural Universities (SAUs) across India's cotton-growing zones.</p>
    </section>
    ${zones.map((zone) => renderCultivarZone(zone)).join("")}
  `;
}

function renderCultivarZone(zone) {
  const items = appData.cultivars.filter((item) => item.zone === zone);
  if (!items.length) return "";
  const groups = [];
  items.forEach((item) => {
    const label = item.group || "";
    let group = groups.find((g) => g.label === label);
    if (!group) {
      group = { label, items: [] };
      groups.push(group);
    }
    group.items.push(item);
  });
  return `
    <section style="margin-top:34px">
      <h2>${zone}</h2>
      ${groups.map((group) => `
        ${group.label ? `<h3 style="margin:18px 0 10px;color:var(--green-dark)">${group.label}</h3>` : ""}
        <div class="technology-list">
          ${group.items.map((item, index) => `
            <article class="technology-row">
              <span>${index + 1}</span>
              <div>
                <h3>${item.name}</h3>
                <p>${item.description}</p>
              </div>
            </article>
          `).join("")}
        </div>
      `).join("")}
    </section>
  `;
}

function resourceDescription(target) {
  return {
    varieties: "Explore improved cotton varieties and hybrids.",
    cultivars: "Cotton cultivars released by State Agricultural Universities.",
    production: "Best practices for better production.",
    protection: "Effective solutions for pest and disease management.",
    advisory: "Timely advisory for better crop decisions.",
    facts: "Key statistics and important insights.",
    gallery: "Explore images and moments from the field.",
    outreach: "Programs and support for farmers.",
    cottonTech: "Innovations and technological advancements.",
    news: "Latest news and updates on cotton.",
  }[target] || "Cotton research resource.";
}

function featureIcon(target, fallback) {
  const icons = {
    varieties: "assets/images/varieties.jpg",
    cultivars: "assets/images/variety2.JPG",
    production: "assets/images/production.JPG",
    protection: "assets/images/security.JPG",
    advisory: "assets/icon/weather.jpg",
    facts: "assets/images/bar-chart.png",
    gallery: "assets/images/gallery.png",
    outreach: "assets/images/farmerReach.JPG",
    cottonTech: "assets/production/n-cropping-1.jpg",
    news: "assets/icon/CICR_logo.png",
  };
  const src = icons[target];
  return src ? `<img src="${assetPath(src)}" alt="${pageTitles[target] || fallback}">` : icon(fallback);
}

function soft(color) {
  return `${color}18`;
}

function renderAboutCicr() {
  view.className = "content about-cicr-view";
  view.innerHTML = `
    <section class="about-hero">
      <div>
        <h2>About ICAR-CICR</h2>
        <p>Science. Innovation. Impact.</p>
      </div>
    </section>
    <section class="about-institute">
      <article>
        <span class="section-kicker">The Institute</span>
        <p>ICAR-Central Institute for Cotton Research (ICAR-CICR) was established at Nagpur, in 1976. The main goal of providing scientific leadership in cotton research. It has two regional stations located at Sirsa, Haryana and Coimbatore, Tamil Nadu. These centres cater to the needs of north and south India, respectively.</p>
        <button data-view="contact">Know More About CICR -></button>
      </article>
      <img src="${assetPath("assets/banner/bann2.JPG")}" alt="ICAR CICR cotton field">
    </section>
    <section class="about-two-col">
      <article class="about-panel">
        <span class="panel-icon">M</span>
        <div>
          <h3>Mission</h3>
          <p>To accelerate growth in national cotton productivity and minimize yield gaps by developing farm technologies for the different agro-ecoregions and to provide products and services to various stakeholders.</p>
        </div>
      </article>
      <article class="about-panel">
        <span class="panel-icon">R</span>
        <div>
          <h3>Mandate</h3>
          <ul>
            <li>Basic, strategic and adaptive research on cotton production, protection, fibre quality and value addition.</li>
            <li>Technology assessment, refinement and frontline demonstrations.</li>
            <li>Capacity building and human resource development.</li>
          </ul>
        </div>
      </article>
    </section>
    <section class="about-stats">
      <div><strong>1976</strong><span>Established at Nagpur</span></div>
      <div><strong>2</strong><span>Regional Stations</span></div>
      <div><strong>Serving</strong><span>North and South India</span></div>
      <div><strong>Science Led</strong><span>Cotton research</span></div>
      <div><strong>Impact Driven</strong><span>Innovations for farmers</span></div>
    </section>
  `;
  view.querySelectorAll("[data-view]").forEach((el) => el.addEventListener("click", onNavClick));
}

function infoCard(title, body, center = false) {
  return `<article class="info-card ${center ? "center" : ""}"><h2>${title}</h2><div class="body">${body}</div></article>`;
}

function renderAboutApp() {
  view.className = "content about-app-view";
  if (state.aboutTab === "developers") {
    view.innerHTML = `
      ${infoCard("Published By", "Dr. Vijay N. Waghmare, Director, ICAR-CICR, Nagpur")}
      ${infoCard("Lead developer", "Dr V. S. Nagrare", true)}
      ${infoCard("Co-Developers", "Dr. S. Manickam<br>Dr Rahul Fuke<br>Dr Babasaheb B.Fand<br>Dr Dipak Nagrale<br>Dr. GI Ramakrushna<br>Dr. Amarpreet Singh<br>Dr K. Velmourougane<br>Dr K Rameash", true)}
      ${infoCard("Hindi translation", "Dr Rachna Pande<br>Dr Pooja Verma", true)}
      ${infoCard("Software Providers", "Zappkode Solutions, Nagpur", true)}
    `;
    return;
  }
  view.innerHTML = `
    <section class="about-app-title"><h2>About App</h2></section>
    <section class="about-app-grid">
      <article class="about-app-card">
        <h3>About the App</h3>
        <ul>
          <li>This App is a user friendly software tool developed to support the cotton stakeholders involved with cotton production.</li>
          <li>It covers A to Z about cotton cultivation including crop improvement, crop production and crop protection.</li>
          <li>The user can refer at any time in offline mode as well.</li>
          <li>The size of the app is 45 MB that makes the users to download it no time.</li>
          <li>The targeted end users are not only the Farmers but also Students, Researchers, State Department personnel, Extension functionaries, KVK personnel and Policy makers.</li>
        </ul>
        <a href="https://cicr.org.in/privacypolicy/" target="_blank" rel="noopener">Privacy Policy</a>
      </article>
      <article class="app-showcase">
        <img class="app-phone-image" src="${assetPath("assets/images/mobilepng.png")}" alt="Cotton Knowledge App">
      </article>
    </section>
    <section class="developer-heading">About Developers</section>
    <section class="developer-grid">
      ${developerBox("Published By", "Dr. Vijay N. Waghmare<br>Director, ICAR-CICR, Nagpur")}
      ${developerBox("Lead Developer", "Dr V. S. Nagrare")}
      ${developerBox("Co-Developers", "Dr. S. Manickam<br>Dr Rahul Fuke<br>Dr Babasaheb B.Fand<br>Dr Dipak Nagrale<br>Dr. GI Ramakrushna<br>Dr. Amarpreet Singh<br>Dr K. Velmourougane<br>Dr K Rameash")}
      ${developerBox("Hindi Translation", "Dr Rachna Pande<br>Dr Pooja Verma")}
      ${developerBox("Software Providers", "Zappkode Solutions, Nagpur")}
    </section>
  `;
}

function developerBox(title, body) {
  return `<article class="developer-box"><span>${title}</span><p>${body}</p></article>`;
}

function renderContact() {
  view.className = "content contact-view";
  const offices = [
    { name: "ICAR- Central Institute for Cotton Research (Nagpur)", bg: "#eef3ff", rows: [["pin", "Post Bag No. 2, Shankar Nagar PO, Nagpur, Maharashtra, India, Pincode-440010"], ["phone", "07103-275536/37/38/39"], ["fax", "07103-275529"], ["web", "http://www.cicr.org.in"], ["mail", "cicrnagpur@gmail.com"]] },
    { name: "ICAR- Central Institute For Cotton Research (Coimbatore)", bg: "#eefaf5", rows: [["pin", "Coimbatore (Tamil Nadu), Pincode-641003"], ["phone", "0422-2430045"], ["fax", "0422-2454021"], ["web", "http://www.cicr.org.in"], ["mail", "cicrcbe@gmail.com"]] },
    { name: "ICAR- Central Institute for Cotton Research (Sirsa)", bg: "#fff3ec", rows: [["pin", "Sirsa (Haryana), Pincode- 125055"], ["phone", "01666-220428"], ["fax", "01666-230271"], ["web", "http://www.cicr.org.in"], ["mail", "cicrsirsa@yahoo.co.in"]] },
  ];
  view.innerHTML = `
    <section class="contact-hero">
      <div>
        <h2>Contact ICAR-CICR</h2>
        <p>We have multiple research centres across India to serve you better.<br>Reach out to any of our locations for inquiries, collaborations and support.</p>
      </div>
    </section>
    <section class="contact-grid">${offices.map(contactCard).join("")}</section>
    <section class="map-strip">
      <div><span>Pin</span><strong>Nagpur</strong><small>Maharashtra</small></div>
      <div><span>Pin</span><strong>Coimbatore</strong><small>Tamil Nadu</small></div>
      <div><span>Pin</span><strong>Sirsa</strong><small>Haryana</small></div>
    </section>
    <section class="enquiry-strip">
      <div class="enquiry-icon">Tel</div>
      <div>
        <h3>Have an Enquiry?</h3>
        <p>We're here to help! Reach out to any of our centres or email us for general queries.</p>
      </div>
      <a href="mailto:cicrnagpur@gmail.com">Send Enquiry -></a>
    </section>
  `;
  view.querySelectorAll("[data-view]").forEach((el) => el.addEventListener("click", onNavClick));
}

function contactCard(office) {
  return `<article class="contact-card" style="background:${office.bg}"><h2>${office.name}</h2>
    ${office.rows.map(([iconName, text]) => `<div class="contact-row"><span class="contact-icon">${icon(iconName)}</span><span>${text}</span></div>`).join("")}
  </article>`;
}

function renderAdvisory() {
  view.className = "content advisory-view";
  const fallbackCards = buildFallbackAdvisoryCards();
  const cards = appData.liveAdvisories?.length ? appData.liveAdvisories : fallbackCards;
  const pageSize = 3;
  const totalPages = Math.max(1, Math.ceil(cards.length / pageSize));
  state.advisoryPage = Math.min(Math.max(state.advisoryPage, 1), totalPages);
  const pageStart = (state.advisoryPage - 1) * pageSize;
  const visibleCards = cards.slice(pageStart, pageStart + pageSize);
  view.innerHTML = `
    <section class="advisory-hero">
      <div>
        <h2>Weekly Advisory for Cotton Cultivation</h2>
        <p>Timely, science-based advisories to help cotton growers make informed decisions for better crop management and higher productivity.</p>
      </div>
      <div class="cotton-line-art">Cotton</div>
    </section>
    <section class="advisory-filters">
      <label>Month<select><option>All Months</option><option>August</option><option>July</option></select></label>
      <label>Year<select><option>All Years</option><option>2026</option><option>2024</option></select></label>
      <label>Search<span class="search-wrap"><input type="search" placeholder="Search by advisory title..."><button>Search</button></span></label>
      <label>Language<select><option>All Languages</option><option>English</option><option>Hindi</option><option>Marathi</option></select></label>
      <button class="reset-filter">Reset</button>
    </section>
    <section class="advisory-grid">
      ${visibleCards.map(advisoryCard).join("")}
    </section>
    ${renderPagination(state.advisoryPage, totalPages)}
  `;
  bindAdvisoryPagination(totalPages);
}

function buildFallbackAdvisoryCards() {
  const pdf = (week, language) => {
    const file = appData.advisories.find((item) => {
      const name = item.file.toLowerCase();
      const isGujarati = name.includes("gujarati");
      return name.includes(week.toLowerCase()) && (language === "Gujarati" ? isGujarati : !isGujarati);
    });
    return file?.file || "";
  };

  return [
    {
      week: "XIV",
      title: "Cotton Cultivation Advisory 10-16 Sept 2024",
      date: "10-09-2024",
      month: "September",
      languages: [["English", pdf("10_16", "English")], ["Gujarati", pdf("10to16", "Gujarati")]].filter(([, file]) => file),
    },
    {
      week: "XIII",
      title: "Cotton Cultivation Advisory 3-9 Sept 2024",
      date: "03-09-2024",
      month: "September",
      languages: [["English", pdf("3-9", "English")], ["Gujarati", pdf("3_to_9", "Gujarati")]].filter(([, file]) => file),
    },
    {
      week: "XII",
      title: "Cotton Cultivation Advisory 27 Aug to 2 Sep 2024",
      date: "27-08-2024",
      month: "August",
      languages: [["English", pdf("27_aug", "English")], ["Gujarati", pdf("27_aug", "Gujarati")]].filter(([, file]) => file),
    },
    {
      week: "XI",
      title: "Cotton Cultivation Advisory 20-26 Aug 2024",
      date: "20-08-2024",
      month: "August",
      languages: [["English", pdf("20_26", "English")], ["Gujarati", pdf("20-26", "Gujarati")]].filter(([, file]) => file),
    },
  ].map((item) => ({ ...item, file: item.languages[0]?.[1] || "" }));
}

function renderPagination(currentPage, totalPages) {
  const pages = Array.from({ length: totalPages }, (_, index) => index + 1);
  return `<nav class="advisory-pagination" aria-label="Advisory pagination">
    <button data-page="first" ${currentPage === 1 ? "disabled" : ""}>&lt;&lt;</button>
    <button data-page="prev" ${currentPage === 1 ? "disabled" : ""}>&lt;</button>
    ${pages.map((page) => `<button data-page="${page}" class="${page === currentPage ? "active" : ""}">${page}</button>`).join("")}
    <button data-page="next" ${currentPage === totalPages ? "disabled" : ""}>&gt;</button>
    <button data-page="last" ${currentPage === totalPages ? "disabled" : ""}>&gt;&gt;</button>
  </nav>`;
}

function bindAdvisoryPagination(totalPages) {
  view.querySelector(".advisory-pagination")?.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-page]");
    if (!button || button.disabled) return;
    const page = button.dataset.page;
    if (page === "first") state.advisoryPage = 1;
    else if (page === "prev") state.advisoryPage = Math.max(1, state.advisoryPage - 1);
    else if (page === "next") state.advisoryPage = Math.min(totalPages, state.advisoryPage + 1);
    else if (page === "last") state.advisoryPage = totalPages;
    else state.advisoryPage = Number(page);
    renderAdvisory();
    view.scrollIntoView({ behavior: "smooth", block: "start" });
  });
}

function advisoryCard(item) {
  return `<article class="advisory-card">
    <div class="week-badge">${item.week}</div>
    <div>
      <h2>${item.title}</h2>
      <p>Starting Date: ${item.date}<br>Month: ${item.month}</p>
      <p class="available-label">Available Languages:</p>
      <div class="chips">${item.languages.map(([lang, file]) => file ? `<a href="${file}" target="_blank" rel="noopener">${lang}</a>` : `<span>${lang}</span>`).join("")}</div>
      ${item.file ? `<a class="view-advisory" href="${item.file}" target="_blank" rel="noopener">View Advisory -></a>` : `<button class="view-advisory" disabled>PDF Not Available</button>`}
    </div>
  </article>`;
}

function renderProtection() {
  const combined = [...appData.pests, ...appData.diseases];
  if (state.detailSlug) {
    const item = combined.find((entry) => itemSlug(entry) === state.detailSlug);
    if (item) {
      const siblings = appData.pests.includes(item) ? appData.pests : appData.diseases;
      renderDetailPage("protection", siblings, item);
      return;
    }
  }
  view.className = "content wide";
  view.innerHTML = `
    <section>
      <h2>Pest Management</h2>
      <div class="collection-grid">${appData.pests.map(dataCard).join("")}</div>
    </section>
    <section style="margin-top:34px">
      <h2>Disease Management</h2>
      <div class="collection-grid">${appData.diseases.map(dataCard).join("")}</div>
    </section>
  `;
  bindDataCards(combined, (item) => openDetail("protection", item));
}

function renderCollection(viewId, items) {
  if (state.detailSlug) {
    const item = items.find((entry) => itemSlug(entry) === state.detailSlug);
    if (item) {
      renderDetailPage(viewId, items, item);
      return;
    }
  }
  view.className = "content wide";
  view.innerHTML = `<h2>${pageTitles[viewId]}</h2><div class="collection-grid">${items.map(dataCard).join("")}</div>`;
  bindDataCards(items, (item) => openDetail(viewId, item));
}

function dataCard(item, index) {
  return `<article class="data-card" data-index="${index}">
    <img src="${assetPath(item.image)}" alt="${item.name}">
    <div><h3>${item.name}</h3><p>${item.description || ""}</p></div>
  </article>`;
}

function bindDataCards(items, onClick) {
  view.querySelectorAll(".data-card").forEach((card, index) => card.addEventListener("click", () => onClick(items[index], index)));
}

function galleryItems() {
  return appData.galleryAlbums?.length
    ? appData.galleryAlbums
    : appData.gallery.map((image, index) => ({
      name: mobileDetails.galleryTitles?.[index] || `Gallery Photo ${index + 1}`,
      image,
      images: [image],
      type: "galleryAlbum",
      description: "CICR Cotton gallery image from mobile app assets.",
    }));
}

function renderGallery() {
  const items = galleryItems();
  if (state.detailSlug) {
    const item = items.find((entry) => itemSlug(entry) === state.detailSlug);
    if (item) {
      renderDetailPage("gallery", items, item);
      return;
    }
  }
  view.className = "content wide";
  view.innerHTML = `<h2>Gallery</h2><div class="collection-grid">${items.map(dataCard).join("")}</div>`;
  bindDataCards(items, (item) => openDetail("gallery", item));
}

function renderOutreach() {
  const items = mobileDetails.outreach || [];
  if (state.detailSlug) {
    const item = items.find((entry) => itemSlug(entry) === state.detailSlug);
    if (item) {
      renderDetailPage("outreach", items, item);
      return;
    }
  }
  view.className = "content wide";
  view.innerHTML = `<h2>Farmers Outreach</h2><div class="collection-grid">${items.map(dataCard).join("")}</div>`;
  bindDataCards(items, (item) => openDetail("outreach", item));
}

function findDetailItem(viewId, slug) {
  if (!slug) return null;
  const collections = {
    production: appData.production,
    facts: appData.facts,
    outreach: mobileDetails.outreach || [],
    gallery: galleryItems(),
    protection: [...appData.pests, ...appData.diseases],
  };
  return (collections[viewId] || []).find((entry) => itemSlug(entry) === slug) || null;
}

function renderDetailPage(viewId, items, item) {
  const currentIndex = Math.max(0, items.findIndex((entry) => itemSlug(entry) === itemSlug(item)));
  const previous = items[(currentIndex - 1 + items.length) % items.length];
  const next = items[(currentIndex + 1) % items.length];
  view.className = "content wide variety-detail-page";
  view.innerHTML = `
    <section class="detail-page-card">
      <button class="inline-back" id="detailBack">Back to ${pageTitles[viewId] || "list"}</button>
      ${renderDetailMarkup(item)}
    </section>
    ${items.length > 1 ? `
    <section class="variety-detail-actions">
      <button class="outline-link" type="button" data-detail-link="${itemSlug(previous)}">
        <small>Previous</small><span>${previous.detailTitle || previous.name}</span>
      </button>
      <button class="solid-link" type="button" data-detail-link="${itemSlug(next)}">
        <small>Next</small><span>${next.detailTitle || next.name}</span>
      </button>
    </section>` : ""}
  `;
  view.querySelector("#detailBack").addEventListener("click", () => closeDetail(viewId));
  view.querySelectorAll("[data-detail-link]").forEach((button) => {
    button.addEventListener("click", () => {
      const nextItem = items.find((entry) => itemSlug(entry) === button.dataset.detailLink);
      openDetail(viewId, nextItem);
    });
  });
  if (item.type === "galleryAlbum") setupGallerySlider(view);
}

function renderCottonTech() {
  const technologies = mobileDetails.cottonTechnologies || [];
  view.className = "content wide";
  view.innerHTML = `
    <section class="technology-page">
      <h2>Cotton Technologies</h2>
      <p>Readable technology particulars from the CICR Cotton mobile app content.</p>
      <div class="technology-list">
        ${technologies.map((item) => `
          <article class="technology-row">
            <span>${item.slNo}</span>
            <div>
              <h3>${item.name}</h3>
              <p><strong>Year of invention:</strong> ${item.year}</p>
              <p><strong>Inventors:</strong> ${item.inventors}</p>
              ${item.remarks ? `<p><strong>Remarks:</strong> ${item.remarks}</p>` : ""}
            </div>
          </article>
        `).join("")}
      </div>
    </section>
  `;
}

function renderNews() {
  view.className = "content news-view";
  const fallbackNews = [
    { name: "Issue 34", description: "November 19, 2024", file: "http://128.199.7.234/media/news_articles/Issue_No34_19th_Nov_2024_241119_184108.pdf" },
    { name: "Issue 39", description: "December 24, 2024", file: "http://128.199.7.234/media/news_articles/Issue_No.39_24th_December_2024.pdf" },
    { name: "Issue 01", description: "August 9, 2025", file: "http://128.199.7.234/media/news_articles/TSV_leaf_folder_2023.pdf" },
  ];
  const items = appData.liveNews?.length ? appData.liveNews : fallbackNews;
  view.innerHTML = `
    <section class="news-hero">
      <h2>Cotton News</h2>
      <p>Latest CICR cotton news and PDF bulletins.</p>
    </section>
    <section class="news-list">
      ${items.map((item) => `
        <a class="news-card" href="${item.file || "#"}" target="_blank" rel="noopener">
          <span class="news-issue">${item.name}</span>
          <span class="news-date">${item.description}</span>
          <span class="pdf-row"><strong>PDF</strong> Tap to view PDF</span>
        </a>
      `).join("")}
    </section>
  `;
}

function hydrateMobileDetails() {
  if (typeof mobileDetails === "undefined") return;
  mergeByName(appData.production, mobileDetails.production);
  mergeByName(appData.pests, mobileDetails.pests);
  mergeByName(appData.diseases, mobileDetails.diseases);
  mergeByName(appData.varieties, mobileDetails.varieties);
}

function mergeByName(items, details) {
  if (!details) return;
  items.forEach((item) => {
    const detail = details[detailKey(item.name)];
    if (detail) Object.assign(item, detail);
  });
}

function detailKey(value) {
  return String(value || "").toLowerCase().replace(/[^a-z0-9]+/g, "");
}

function renderDetailMarkup(item) {
  const title = item.detailTitle || item.name;
  const media = item.type === "galleryAlbum"
    ? renderGalleryAlbum(item.images, title)
    : item.image
      ? `<div class="detail-media-frame"><img class="detail-media" src="${assetPath(item.image)}" alt="${title}"></div>`
      : "";
  return `
    <article class="detail-shell">
      <div class="detail-hero${media ? "" : " no-media"}">
        ${media ? `<div class="detail-hero-media">${media}</div>` : ""}
        <div class="detail-hero-copy">
          <h2>${title}</h2>
          ${item.description ? `<p class="detail-intro">${item.description}</p>` : ""}
        </div>
      </div>
      ${item.details ? renderDetailsGrid(item.details) : ""}
      ${item.sections ? renderSections(item.sections) : ""}
      ${item.tabs ? renderTabs(item.tabs) : ""}
    </article>
  `;
}

const SECTION_ICON_PATHS = {
  leaf: '<path d="M4 16C4 8 9 4 17 3.5 16.5 11.5 12.5 16.5 4 16.5Z"/><path d="M4 16c3-3 6-6.5 12-12"/>',
  search: '<circle cx="9" cy="9" r="6"/><line x1="17" y1="17" x2="13.2" y2="13.2"/>',
  pin: '<path d="M10 17.5S16 12 16 8a6 6 0 0 0-12 0c0 4 6 9.5 6 9.5Z"/><circle cx="10" cy="8" r="2.2"/>',
  tag: '<path d="M10.5 3H4a1 1 0 0 0-1 1v6.5a1 1 0 0 0 .29.71l7.5 7.5a1 1 0 0 0 1.42 0l6.5-6.5a1 1 0 0 0 0-1.42l-7.5-7.5A1 1 0 0 0 10.5 3Z"/><circle cx="7.4" cy="7.4" r="1.15" fill="currentColor" stroke="none"/>',
  shield: '<path d="M10 2.5 16.5 5v5.2C16.5 14 13.7 17 10 17.9 6.3 17 3.5 14 3.5 10.2V5Z"/>',
  alert: '<path d="M10 3 2 17h16Z"/><line x1="10" y1="8.5" x2="10" y2="12"/><circle cx="10" cy="14.6" r="0.9" fill="currentColor" stroke="none"/>',
  target: '<circle cx="10" cy="10" r="7"/><circle cx="10" cy="10" r="3.5"/><circle cx="10" cy="10" r="0.9" fill="currentColor" stroke="none"/>',
  calendar: '<rect x="3" y="4.5" width="14" height="12.5" rx="2"/><line x1="3" y1="8.5" x2="17" y2="8.5"/><line x1="7" y1="2.5" x2="7" y2="6.5"/><line x1="13" y1="2.5" x2="13" y2="6.5"/>',
  wrench: '<path d="M14.7 3.3a4 4 0 0 0-5.4 4.8L3 14.4V17h2.6l6.3-6.3a4 4 0 0 0 4.8-5.4l-2.7 2.7-2-2Z"/>',
  info: '<circle cx="10" cy="10" r="7.5"/><line x1="10" y1="9" x2="10" y2="14"/><circle cx="10" cy="6.4" r="0.9" fill="currentColor" stroke="none"/>',
};

const SECTION_ICON_RULES = [
  [/scientific|causal|organism/i, "leaf"],
  [/identif/i, "search"],
  [/\bstatus\b/i, "shield"],
  [/\btype\b/i, "tag"],
  [/occurrence|period|\btime\b|\bzone\b/i, "pin"],
  [/damage|symptom/i, "alert"],
  [/^etl$/i, "target"],
  [/\d.*day|days/i, "calendar"],
  [/management|precaution/i, "wrench"],
];

function sectionIconName(title) {
  const text = String(title || "");
  const match = SECTION_ICON_RULES.find(([re]) => re.test(text));
  return match ? match[1] : "info";
}

function iconBadge(title, large = false) {
  const path = SECTION_ICON_PATHS[sectionIconName(title)];
  return `<span class="section-icon${large ? " large" : ""}"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${path}</svg></span>`;
}

function renderGalleryAlbum(images = [], title = "Gallery") {
  if (!images.length) return "";
  return `<div class="gallery-slider" data-current="0">
    <div class="gallery-slider-stage">
      <button class="gallery-slider-nav prev" data-slider="prev" aria-label="Previous image">&lt;</button>
      ${images.map((image, index) => `<img class="gallery-slide ${index === 0 ? "active" : ""}" src="${assetPath(image)}" alt="${title} photo ${index + 1}" data-slide="${index}">`).join("")}
      <button class="gallery-slider-nav next" data-slider="next" aria-label="Next image">&gt;</button>
    </div>
    <div class="gallery-slider-footer">
      <span class="gallery-slider-count">1 / ${images.length}</span>
      <div class="gallery-slider-dots">
        ${images.map((_, index) => `<button class="${index === 0 ? "active" : ""}" data-slide-dot="${index}" aria-label="Show image ${index + 1}"></button>`).join("")}
      </div>
    </div>
  </div>`;
}

function setupGallerySlider(container) {
  const slider = container.querySelector(".gallery-slider");
  if (!slider) return;
  const slides = [...slider.querySelectorAll(".gallery-slide")];
  const dots = [...slider.querySelectorAll("[data-slide-dot]")];
  const count = slider.querySelector(".gallery-slider-count");
  const show = (nextIndex) => {
    const total = slides.length;
    const index = (nextIndex + total) % total;
    slider.dataset.current = String(index);
    slides.forEach((slide, itemIndex) => slide.classList.toggle("active", itemIndex === index));
    dots.forEach((dot, itemIndex) => dot.classList.toggle("active", itemIndex === index));
    if (count) count.textContent = `${index + 1} / ${total}`;
  };

  slider.addEventListener("click", (event) => {
    const nav = event.target.closest("[data-slider]");
    const dot = event.target.closest("[data-slide-dot]");
    const current = Number(slider.dataset.current || 0);
    if (nav?.dataset.slider === "prev") show(current - 1);
    if (nav?.dataset.slider === "next") show(current + 1);
    if (dot) show(Number(dot.dataset.slideDot));
  });
}

function renderTabs(tabs) {
  return `<div class="detail-tabs">${tabs.map((tab) => `
    <section class="detail-tab">
      <div class="detail-tab-head">${iconBadge(tab.title, true)}<h3>${tab.title}</h3></div>
      ${renderSections(tab.sections || [])}
    </section>
  `).join("")}</div>`;
}

function sectionLayout(section) {
  if (/occurrence|period|\btime\b|\bzone\b|^etl$|days/i.test(String(section.title || ""))) return "feature";
  if (!section.images && !section.bullets) return "compact";
  return "wide";
}

function sectionBody(section) {
  return `
    ${section.text ? `<p>${section.text}</p>` : ""}
    ${section.details ? renderDetailsGrid(section.details) : ""}
    ${section.bullets ? `<ul>${section.bullets.map((line) => `<li>${line}</li>`).join("")}</ul>` : ""}
    ${section.images ? `<div class="detail-image-grid">${section.images.map((image) => `<img src="${assetPath(image)}" alt="${section.title}">`).join("")}</div>` : ""}
  `;
}

function renderSections(sections) {
  const withLayout = sections.map((section) => [section, sectionLayout(section)]);
  const compacts = withLayout.filter(([, layout]) => layout === "compact");
  const others = withLayout.filter(([, layout]) => layout !== "compact");
  const ordered = [...compacts, ...others];
  const cards = ordered.map(([section, computedLayout]) => {
    const layout = computedLayout === "compact" && compacts.length === 1 ? "wide" : computedLayout;
    if (layout === "feature") {
      return `
        <section class="detail-section detail-section--feature">
          ${iconBadge(section.title, true)}
          <div class="detail-section-body">
            <h3>${section.title}</h3>
            ${sectionBody(section)}
          </div>
        </section>
      `;
    }
    return `
      <section class="detail-section${layout === "compact" ? " detail-section--compact" : ""}">
        <div class="detail-section-head">${iconBadge(section.title)}<h3>${section.title}</h3></div>
        ${sectionBody(section)}
      </section>
    `;
  }).join("");
  return `<div class="detail-section-grid">${cards}</div>`;
}

function renderDetailsGrid(rows) {
  return `<dl class="detail-facts">${rows.map(([label, value]) => {
    const tone = /status/i.test(label) && /major/i.test(String(value)) ? " tone-warn" : "";
    return `<div class="fact-pill${tone}">${iconBadge(label)}<div><dt>${label}</dt><dd>${value}</dd></div></div>`;
  }).join("")}</dl>`;
}

function setupAccessibility() {
  const fab = document.querySelector("#accessibilityFab");
  const panel = document.querySelector("#a11yPanel");
  fab.addEventListener("click", () => panel.classList.toggle("open"));
  panel.addEventListener("click", (event) => {
    const action = event.target.dataset.a11y;
    if (!action) return;
    const root = document.documentElement;
    const current = Number.parseFloat(getComputedStyle(root).getPropertyValue("--font-scale")) || 1;
    if (action === "fontUp") root.style.setProperty("--font-scale", Math.min(current + .08, 1.4));
    if (action === "fontDown") root.style.setProperty("--font-scale", Math.max(current - .08, .85));
    if (action === "contrast") document.body.classList.toggle("high-contrast");
    if (action === "read") speechSynthesis.speak(new SpeechSynthesisUtterance(document.body.innerText.slice(0, 1200)));
  });
}

function setupImageLightbox() {
  const lightbox = document.querySelector("#imageLightbox");
  const lightboxImg = document.querySelector("#lightboxImg");
  const close = () => {
    lightbox.classList.remove("open");
    lightboxImg.src = "";
  };
  document.querySelector("#lightboxClose").addEventListener("click", close);
  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) close();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") close();
  });
  document.addEventListener("click", (event) => {
    const img = event.target.closest(".detail-media, .detail-image-grid img, .variety-detail-figure img");
    if (!img) return;
    lightboxImg.src = img.currentSrc || img.src;
    lightboxImg.alt = img.alt || "";
    lightbox.classList.add("open");
  });
}

hydrateMobileDetails();
init();
