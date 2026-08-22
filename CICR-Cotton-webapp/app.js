const state = {
  view: "home",
  aboutTab: "app",
  techTab: "technologies",
  heroIndex: 0,
  historyReady: false,
  varietyZone: null,
  varietyItem: null,
  detailSlug: null,
  advisoryPage: 1,
  lang: readStoredLang(),
};

function readStoredLang() {
  try {
    const saved = localStorage.getItem("cicrCottonLang");
    return ["en", "hi", "gu"].includes(saved) ? saved : "en";
  } catch (e) {
    return "en";
  }
}

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
  ["cultivars", "sprout", "Cultivars of SAUs"],
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

const NAV_ICON_PATHS = {
  home: '<path d="M3 9.5 10 4l7 5.5"/><path d="M5 8.5V16a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V8.5"/><path d="M8 17v-4a2 2 0 0 1 4 0v4"/>',
  i: '<circle cx="10" cy="10" r="7.5"/><line x1="10" y1="9" x2="10" y2="14"/><circle cx="10" cy="6.4" r="0.9" fill="currentColor" stroke="none"/>',
  bell: '<path d="M6 8a4 4 0 0 1 8 0c0 3.2 1.2 4.6 1.8 5.2H4.2C4.8 12.6 6 11.2 6 8Z"/><path d="M8.3 15.5a1.8 1.8 0 0 0 3.4 0"/>',
  tel: '<path d="M6.6 3.5 8.8 6a1 1 0 0 1-.2 1.3L7.3 8.5c.9 1.8 2.4 3.3 4.2 4.2l1.2-1.3a1 1 0 0 1 1.3-.2l2.5 2.2c.4.4.5 1 .1 1.4l-1.2 1.4c-.4.5-1 .7-1.6.6-4-.9-7.5-4.4-8.4-8.4-.1-.6.1-1.2.6-1.6l1.4-1.2c.4-.4 1-.3 1.4.1Z"/>',
  cal: '<rect x="6" y="2.5" width="8" height="15" rx="1.6"/><line x1="9" y1="14.5" x2="11" y2="14.5"/>',
  leaf: '<path d="M4 16C4 8 9 4 17 3.5 16.5 11.5 12.5 16.5 4 16.5Z"/><path d="M4 16c3-3 6-6.5 12-12"/>',
  sprout: '<path d="M10 17V10"/><path d="M10 10C10 6 6.5 4 3.5 4.2 3.5 8 6 10 10 10Z"/><path d="M10 8c0-3 2.8-4.7 5.5-4.5C15.5 6.7 13.2 9 10 9Z"/>',
  tractor: '<circle cx="6.5" cy="15" r="2.2"/><circle cx="15" cy="15" r="1.6"/><path d="M3.5 15h1.6"/><path d="M8.3 15h4"/><path d="M4.5 12V7.5h3.5l2 3h2.2l1.3 2.5"/><path d="M12.3 12.5h1.8"/>',
  shield: '<path d="M10 2.5 16.5 5v5.2C16.5 14 13.7 17 10 17.9 6.3 17 3.5 14 3.5 10.2V5Z"/>',
  chart: '<line x1="4" y1="17" x2="16" y2="17"/><rect x="5" y="11" width="3" height="6"/><rect x="9" y="7" width="3" height="10"/><rect x="13" y="3" width="3" height="14"/>',
  image: '<rect x="3" y="4" width="14" height="12" rx="1.5"/><circle cx="7.5" cy="8.5" r="1.4"/><path d="M4 15l4-4 3 3 3-4 3 4"/>',
};

function icon(name) {
  const path = NAV_ICON_PATHS[name] || NAV_ICON_PATHS.i;
  return `<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${path}</svg>`;
}

const TRANSLATIONS = {
  hi: {
    "Home": "होम",
    "About CICR": "सीआईसीआर के बारे में",
    "Contact Us": "संपर्क करें",
    "Advisory": "सलाह",
    "About App": "ऐप के बारे में",
    "Varieties and Hybrids": "किस्में और संकर",
    "Cultivars of SAUs": "कृषि विश्वविद्यालयों की किस्में",
    "Production Technology": "उत्पादन तकनीक",
    "Protection Technology": "सुरक्षा तकनीक",
    "Facts and Figures": "तथ्य और आंकड़े",
    "Gallery": "गैलरी",
    "Farmers Outreach": "किसान संपर्क कार्यक्रम",
    "Cotton Technology": "कपास तकनीक",
    "Cotton News": "कपास समाचार",
    "Research & Resources": "अनुसंधान और संसाधन",
    "Empowering Cotton Farming": "कपास खेती को सशक्त बनाना",
    "Through Research": "अनुसंधान के माध्यम से",
    "Your comprehensive guide to cotton farming": "कपास खेती के लिए आपकी संपूर्ण मार्गदर्शिका",
    "Explore Research": "अनुसंधान देखें",
    "Weekly Advisory": "साप्ताहिक सलाह",
    "Explore Cotton Research & Resources": "कपास अनुसंधान और संसाधन देखें",
    "Access our research, technologies and resources to enhance cotton productivity and sustainability.": "कपास उत्पादकता और स्थिरता बढ़ाने के लिए हमारे अनुसंधान, तकनीकों और संसाधनों तक पहुंचें।",
    "Explore improved cotton varieties and hybrids.": "उन्नत कपास किस्मों और संकरों को देखें।",
    "Cotton cultivars released by State Agricultural Universities.": "राज्य कृषि विश्वविद्यालयों द्वारा जारी कपास किस्में।",
    "Best practices for better production.": "बेहतर उत्पादन के लिए सर्वोत्तम प्रथाएं।",
    "Effective solutions for pest and disease management.": "कीट और रोग प्रबंधन के लिए प्रभावी समाधान।",
    "Timely advisory for better crop decisions.": "बेहतर फसल निर्णयों के लिए समय पर सलाह।",
    "Key statistics and important insights.": "मुख्य आंकड़े और महत्वपूर्ण जानकारी।",
    "Explore images and moments from the field.": "खेत की तस्वीरें और पल देखें।",
    "Programs and support for farmers.": "किसानों के लिए कार्यक्रम और सहायता।",
    "Innovations and technological advancements.": "नवाचार और तकनीकी प्रगति।",
    "Latest news and updates on cotton.": "कपास पर नवीनतम समाचार और अपडेट।",
    "Weekly Advisory For Cotton Cultivation": "कपास की खेती के लिए साप्ताहिक सलाह",
    "Select Your Cotton-Growing Zone": "अपना कपास उत्पादक क्षेत्र चुनें",
    "Choose a zone to view recommended cotton varieties and hybrids.": "अनुशंसित कपास किस्मों और संकरों को देखने के लिए एक क्षेत्र चुनें।",
    "North Zone": "उत्तर क्षेत्र",
    "Central Zone": "मध्य क्षेत्र",
    "South Zone": "दक्षिण क्षेत्र",
    "Punjab, Haryana, Rajasthan and nearby regions": "पंजाब, हरियाणा, राजस्थान और आसपास के क्षेत्र",
    "Maharashtra, Madhya Pradesh, Gujarat and nearby regions": "महाराष्ट्र, मध्य प्रदेश, गुजरात और आसपास के क्षेत्र",
    "Telangana, Andhra Pradesh, Karnataka, Tamil Nadu and nearby regions": "तेलंगाना, आंध्र प्रदेश, कर्नाटक, तमिलनाडु और आसपास के क्षेत्र",
    "North cotton belt": "उत्तरी कपास पट्टी",
    "Major cotton belt": "प्रमुख कपास पट्टी",
    "South cotton belt": "दक्षिणी कपास पट्टी",
    "Explore →": "देखें →",
    "varieties and hybrids": "किस्में और संकर",
    "varieties": "किस्में",
    "Overview": "अवलोकन",
    "Previous": "पिछला",
    "Next": "अगला",
    "Cotton cultivars released by State Agricultural Universities (SAUs) across India's cotton-growing zones.": "भारत के कपास उत्पादक क्षेत्रों में राज्य कृषि विश्वविद्यालयों (SAUs) द्वारा जारी कपास किस्में।",
    "About ICAR-CICR": "आईसीएआर-सीआईसीआर के बारे में",
    "Science. Innovation. Impact.": "विज्ञान। नवाचार। प्रभाव।",
    "The Institute": "संस्थान",
    "Know More About CICR": "सीआईसीआर के बारे में अधिक जानें",
    "Mission": "मिशन",
    "Mandate": "जनादेश",
    "Established at Nagpur": "नागपुर में स्थापित",
    "Regional Stations": "क्षेत्रीय केंद्र",
    "North and South India": "उत्तर और दक्षिण भारत",
    "Serving": "सेवारत",
    "Cotton research": "कपास अनुसंधान",
    "Science Led": "विज्ञान आधारित",
    "Impact Driven": "प्रभाव उन्मुख",
    "Innovations for farmers": "किसानों के लिए नवाचार",
    "ICAR-CICR Mobile Application": "आईसीएआर-सीआईसीआर मोबाइल एप्लिकेशन",
    "Your comprehensive guide to cotton farming, available anytime, anywhere.": "कपास खेती के लिए आपकी संपूर्ण मार्गदर्शिका, कभी भी, कहीं भी उपलब्ध।",
    "GET IT ON": "यहां से प्राप्त करें",
    "Download on the": "यहां से डाउनलोड करें",
    "About the App": "ऐप का विवरण",
    "User Friendly": "उपयोगकर्ता के अनुकूल",
    "Software tool developed to support the cotton stakeholders involved with cotton production.": "कपास उत्पादन से जुड़े हितधारकों की सहायता के लिए विकसित सॉफ्टवेयर टूल।",
    "Complete Cotton Information": "संपूर्ण कपास जानकारी",
    "Covers A to Z about cotton cultivation including crop improvement, crop production and crop protection.": "फसल सुधार, फसल उत्पादन और फसल सुरक्षा सहित कपास की खेती के बारे में संपूर्ण जानकारी।",
    "Offline Access": "ऑफ़लाइन पहुंच",
    "The user can refer to the information at any time in offline mode as well.": "उपयोगकर्ता ऑफ़लाइन मोड में भी किसी भी समय जानकारी देख सकता है।",
    "Lightweight": "हल्का",
    "The size of the app is 45 MB, allowing users to download it in no time.": "ऐप का आकार 45 एमबी है, जिससे उपयोगकर्ता इसे तुरंत डाउनलोड कर सकते हैं।",
    "Target Users": "लक्षित उपयोगकर्ता",
    "Targeted end users include Farmers, Students, Researchers, State Department personnel, Extension functionaries, KVK personnel and Policy makers.": "लक्षित उपयोगकर्ताओं में किसान, छात्र, शोधकर्ता, राज्य विभाग के कर्मी, विस्तार कार्यकर्ता, केवीके कर्मी और नीति निर्माता शामिल हैं।",
    "Privacy Policy": "गोपनीयता नीति",
    "About Developers": "डेवलपर्स के बारे में",
    "Published By": "प्रकाशक",
    "Lead Developer": "मुख्य डेवलपर",
    "Co-Developers": "सह-डेवलपर्स",
    "Hindi Translation": "हिंदी अनुवाद",
    "Software Providers": "सॉफ्टवेयर प्रदाता",
    "Contact ICAR-CICR": "आईसीएआर-सीआईसीआर से संपर्क करें",
    "We have multiple research centres across India to serve you better.": "आपकी बेहतर सेवा के लिए हमारे पूरे भारत में कई अनुसंधान केंद्र हैं।",
    "Reach out to any of our locations for inquiries, collaborations and support.": "पूछताछ, सहयोग और सहायता के लिए हमारे किसी भी केंद्र से संपर्क करें।",
    "Address": "पता",
    "Telephone": "टेलीफोन",
    "Fax": "फैक्स",
    "Website": "वेबसाइट",
    "Email": "ईमेल",
    "Have an Enquiry?": "कोई पूछताछ है?",
    "We're here to help! Reach out to any of our centres or email us for general queries.": "हम मदद के लिए यहां हैं! सामान्य प्रश्नों के लिए हमारे किसी भी केंद्र से संपर्क करें या हमें ईमेल करें।",
    "Send Enquiry": "पूछताछ भेजें",
    "Weekly Advisory for Cotton Cultivation": "कपास की खेती के लिए साप्ताहिक सलाह",
    "Timely, science-based advisories to help cotton growers make informed decisions for better crop management and higher productivity.": "कपास उत्पादकों को बेहतर फसल प्रबंधन और उच्च उत्पादकता के लिए सूचित निर्णय लेने में मदद करने हेतु समय पर, विज्ञान-आधारित सलाह।",
    "Month": "महीना",
    "Year": "वर्ष",
    "Search": "खोजें",
    "Language": "भाषा",
    "All Months": "सभी महीने",
    "All Years": "सभी वर्ष",
    "All Languages": "सभी भाषाएं",
    "English": "अंग्रेज़ी",
    "Hindi": "हिंदी",
    "Gujarati": "गुजराती",
    "Marathi": "मराठी",
    "Search by advisory title...": "सलाह के शीर्षक से खोजें...",
    "Reset": "रीसेट करें",
    "No advisories found": "कोई सलाह नहीं मिली",
    "Try changing the selected month, year, language or search term.": "चयनित महीना, वर्ष, भाषा या खोज शब्द बदलकर देखें।",
    "Available Languages": "उपलब्ध भाषाएं",
    "View Advisory": "सलाह देखें",
    "PDF Not Available": "पीडीएफ उपलब्ध नहीं है",
    "Starting Date:": "प्रारंभ तिथि:",
    "Month:": "महीना:",
    "Pest Management": "कीट प्रबंधन",
    "Disease Management": "रोग प्रबंधन",
    "Latest CICR cotton news and PDF bulletins.": "नवीनतम सीआईसीआर कपास समाचार और पीडीएफ बुलेटिन।",
    "No Cotton News available.": "कोई कपास समाचार उपलब्ध नहीं है।",
    "View PDF →": "पीडीएफ देखें →",
    "Cotton Technologies": "कपास तकनीकें",
    "International Patents": "अंतर्राष्ट्रीय पेटेंट",
    "National Patents": "राष्ट्रीय पेटेंट",
    "Readable technology particulars from the CICR Cotton mobile app content.": "सीआईसीआर कॉटन मोबाइल ऐप सामग्री से तकनीकी विवरण।",
    "No technologies available.": "कोई तकनीक उपलब्ध नहीं है।",
    "Year of invention": "आविष्कार का वर्ष",
    "Application No.": "आवेदन संख्या",
    "Grant Number": "अनुदान संख्या",
    "Inventors": "आविष्कारक",
    "Status": "स्थिति",
    "Remarks": "टिप्पणी",
    "Farmer Knowledge Portal": "किसान ज्ञान पोर्टल",
    "Cotton Research Portal": "कपास अनुसंधान पोर्टल",
    "Central Institute for Cotton Research (CICR) is committed to advance cotton research and support farmers with innovative solutions for sustainable agriculture.": "केंद्रीय कपास अनुसंधान संस्थान (सीआईसीआर) कपास अनुसंधान को आगे बढ़ाने और सतत कृषि के लिए नवीन समाधानों के साथ किसानों का समर्थन करने हेतु प्रतिबद्ध है।",
    "Quick Links": "त्वरित लिंक",
    "Resources": "संसाधन",
    "Varieties & Hybrids": "किस्में और संकर",
    "Publications": "प्रकाशन",
    "Research Reports": "अनुसंधान रिपोर्ट",
    "Circulars & Notifications": "परिपत्र और सूचनाएं",
    "FAQs": "सामान्य प्रश्न",
    "© 2025 CICR Cotton Research. All rights reserved.": "© 2025 सीआईसीआर कॉटन रिसर्च। सर्वाधिकार सुरक्षित।",
    "CICR Cotton Web App Developed By": "सीआईसीआर कॉटन वेब ऐप डेवलप किया गया",
    "Contrast": "कंट्रास्ट",
    "Read": "पढ़ें",
    "Back to": "वापस",
    "Back": "वापस",
    "list": "सूची",
    "Pin": "पिन",
    "Tel": "टेल",
    "Mail": "मेल",
    "Web": "वेब",
  },
  gu: {
    "Home": "હોમ",
    "About CICR": "સીઆઈસીઆર વિશે",
    "Contact Us": "અમારો સંપર્ક કરો",
    "Advisory": "સલાહ",
    "About App": "એપ વિશે",
    "Varieties and Hybrids": "જાતો અને સંકર",
    "Cultivars of SAUs": "કૃષિ યુનિવર્સિટીઓની જાતો",
    "Production Technology": "ઉત્પાદન ટેકનોલોજી",
    "Protection Technology": "સુરક્ષા ટેકનોલોજી",
    "Facts and Figures": "તથ્યો અને આંકડા",
    "Gallery": "ગેલેરી",
    "Farmers Outreach": "ખેડૂત સંપર્ક કાર્યક્રમ",
    "Cotton Technology": "કપાસ ટેકનોલોજી",
    "Cotton News": "કપાસ સમાચાર",
    "Research & Resources": "સંશોધન અને સંસાધનો",
    "Empowering Cotton Farming": "કપાસની ખેતીને સશક્ત બનાવવી",
    "Through Research": "સંશોધન દ્વારા",
    "Your comprehensive guide to cotton farming": "કપાસની ખેતી માટે તમારી સંપૂર્ણ માર્ગદર્શિકા",
    "Explore Research": "સંશોધન જુઓ",
    "Weekly Advisory": "સાપ્તાહિક સલાહ",
    "Explore Cotton Research & Resources": "કપાસ સંશોધન અને સંસાધનો જુઓ",
    "Access our research, technologies and resources to enhance cotton productivity and sustainability.": "કપાસની ઉત્પાદકતા અને ટકાઉપણું વધારવા માટે અમારા સંશોધન, ટેકનોલોજી અને સંસાધનોનો ઉપયોગ કરો.",
    "Explore improved cotton varieties and hybrids.": "સુધારેલી કપાસની જાતો અને સંકર જુઓ.",
    "Cotton cultivars released by State Agricultural Universities.": "રાજ્ય કૃષિ યુનિવર્સિટીઓ દ્વારા બહાર પાડવામાં આવેલી કપાસની જાતો.",
    "Best practices for better production.": "વધુ સારા ઉત્પાદન માટે શ્રેષ્ઠ પદ્ધતિઓ.",
    "Effective solutions for pest and disease management.": "જીવાત અને રોગ વ્યવસ્થાપન માટે અસરકારક ઉકેલો.",
    "Timely advisory for better crop decisions.": "વધુ સારા પાક નિર્ણયો માટે સમયસર સલાહ.",
    "Key statistics and important insights.": "મુખ્ય આંકડા અને મહત્વપૂર્ણ માહિતી.",
    "Explore images and moments from the field.": "ખેતરની તસવીરો અને ક્ષણો જુઓ.",
    "Programs and support for farmers.": "ખેડૂતો માટે કાર્યક્રમો અને સહાય.",
    "Innovations and technological advancements.": "નવીનતાઓ અને ટેકનોલોજીકલ પ્રગતિ.",
    "Latest news and updates on cotton.": "કપાસ પર નવીનતમ સમાચાર અને અપડેટ્સ.",
    "Weekly Advisory For Cotton Cultivation": "કપાસની ખેતી માટે સાપ્તાહિક સલાહ",
    "Select Your Cotton-Growing Zone": "તમારો કપાસ ઉગાડતો વિસ્તાર પસંદ કરો",
    "Choose a zone to view recommended cotton varieties and hybrids.": "ભલામણ કરેલ કપાસની જાતો અને સંકર જોવા માટે વિસ્તાર પસંદ કરો.",
    "North Zone": "ઉત્તર વિસ્તાર",
    "Central Zone": "મધ્ય વિસ્તાર",
    "South Zone": "દક્ષિણ વિસ્તાર",
    "Punjab, Haryana, Rajasthan and nearby regions": "પંજાબ, હરિયાણા, રાજસ્થાન અને આસપાસના વિસ્તારો",
    "Maharashtra, Madhya Pradesh, Gujarat and nearby regions": "મહારાષ્ટ્ર, મધ્ય પ્રદેશ, ગુજરાત અને આસપાસના વિસ્તારો",
    "Telangana, Andhra Pradesh, Karnataka, Tamil Nadu and nearby regions": "તેલંગાણા, આંધ્ર પ્રદેશ, કર્ણાટક, તમિલનાડુ અને આસપાસના વિસ્તારો",
    "North cotton belt": "ઉત્તર કપાસ પટ્ટો",
    "Major cotton belt": "મુખ્ય કપાસ પટ્ટો",
    "South cotton belt": "દક્ષિણ કપાસ પટ્ટો",
    "Explore →": "જુઓ →",
    "varieties and hybrids": "જાતો અને સંકર",
    "varieties": "જાતો",
    "Overview": "વિહંગાવલોકન",
    "Previous": "પાછલું",
    "Next": "આગળ",
    "Cotton cultivars released by State Agricultural Universities (SAUs) across India's cotton-growing zones.": "ભારતના કપાસ ઉગાડતા વિસ્તારોમાં રાજ્ય કૃષિ યુનિવર્સિટીઓ (SAUs) દ્વારા બહાર પાડવામાં આવેલી કપાસની જાતો.",
    "About ICAR-CICR": "આઈસીએઆર-સીઆઈસીઆર વિશે",
    "Science. Innovation. Impact.": "વિજ્ઞાન. નવીનતા. અસર.",
    "The Institute": "સંસ્થા",
    "Know More About CICR": "સીઆઈસીઆર વિશે વધુ જાણો",
    "Mission": "મિશન",
    "Mandate": "આદેશ",
    "Established at Nagpur": "નાગપુર ખાતે સ્થપાયેલ",
    "Regional Stations": "પ્રાદેશિક કેન્દ્રો",
    "North and South India": "ઉત્તર અને દક્ષિણ ભારત",
    "Serving": "સેવા આપતું",
    "Cotton research": "કપાસ સંશોધન",
    "Science Led": "વિજ્ઞાન આધારિત",
    "Impact Driven": "અસર લક્ષી",
    "Innovations for farmers": "ખેડૂતો માટે નવીનતાઓ",
    "ICAR-CICR Mobile Application": "આઈસીએઆર-સીઆઈસીઆર મોબાઇલ એપ્લિકેશન",
    "Your comprehensive guide to cotton farming, available anytime, anywhere.": "કપાસની ખેતી માટે તમારી સંપૂર્ણ માર્ગદર્શિકા, ગમે ત્યારે, ગમે ત્યાં ઉપલબ્ધ.",
    "GET IT ON": "અહીંથી મેળવો",
    "Download on the": "અહીંથી ડાઉનલોડ કરો",
    "About the App": "એપ વિશે વિગતો",
    "User Friendly": "વપરાશકર્તા મૈત્રીપૂર્ણ",
    "Software tool developed to support the cotton stakeholders involved with cotton production.": "કપાસ ઉત્પાદન સાથે સંકળાયેલા હિતધારકોને ટેકો આપવા વિકસાવવામાં આવેલ સોફ્ટવેર ટૂલ.",
    "Complete Cotton Information": "સંપૂર્ણ કપાસ માહિતી",
    "Covers A to Z about cotton cultivation including crop improvement, crop production and crop protection.": "પાક સુધારણા, પાક ઉત્પાદન અને પાક સુરક્ષા સહિત કપાસની ખેતી વિશે સંપૂર્ણ માહિતી.",
    "Offline Access": "ઓફલાઇન એક્સેસ",
    "The user can refer to the information at any time in offline mode as well.": "વપરાશકર્તા ઓફલાઇન મોડમાં પણ કોઈપણ સમયે માહિતી જોઈ શકે છે.",
    "Lightweight": "હલકું",
    "The size of the app is 45 MB, allowing users to download it in no time.": "એપનું કદ 45 એમબી છે, જેનાથી વપરાશકર્તાઓ તેને ઝડપથી ડાઉનલોડ કરી શકે છે.",
    "Target Users": "લક્ષ્ય વપરાશકર્તાઓ",
    "Targeted end users include Farmers, Students, Researchers, State Department personnel, Extension functionaries, KVK personnel and Policy makers.": "લક્ષ્ય વપરાશકર્તાઓમાં ખેડૂતો, વિદ્યાર્થીઓ, સંશોધકો, રાજ્ય વિભાગના કર્મચારીઓ, વિસ્તરણ કાર્યકરો, કેવીકે કર્મચારીઓ અને નીતિ ઘડનારાઓનો સમાવેશ થાય છે.",
    "Privacy Policy": "ગોપનીયતા નીતિ",
    "About Developers": "ડેવલપર્સ વિશે",
    "Published By": "પ્રકાશક",
    "Lead Developer": "મુખ્ય ડેવલપર",
    "Co-Developers": "સહ-ડેવલપર્સ",
    "Hindi Translation": "હિન્દી અનુવાદ",
    "Software Providers": "સોફ્ટવેર પ્રદાતા",
    "Contact ICAR-CICR": "આઈસીએઆર-સીઆઈસીઆરનો સંપર્ક કરો",
    "We have multiple research centres across India to serve you better.": "તમને વધુ સારી સેવા આપવા માટે અમારી પાસે સમગ્ર ભારતમાં અનેક સંશોધન કેન્દ્રો છે.",
    "Reach out to any of our locations for inquiries, collaborations and support.": "પૂછપરછ, સહયોગ અને સહાય માટે અમારા કોઈપણ સ્થળનો સંપર્ક કરો.",
    "Address": "સરનામું",
    "Telephone": "ટેલિફોન",
    "Fax": "ફેક્સ",
    "Website": "વેબસાઇટ",
    "Email": "ઈમેલ",
    "Have an Enquiry?": "કોઈ પૂછપરછ છે?",
    "We're here to help! Reach out to any of our centres or email us for general queries.": "અમે મદદ કરવા માટે અહીં છીએ! સામાન્ય પ્રશ્નો માટે અમારા કોઈપણ કેન્દ્રનો સંપર્ક કરો અથવા અમને ઈમેલ કરો.",
    "Send Enquiry": "પૂછપરછ મોકલો",
    "Weekly Advisory for Cotton Cultivation": "કપાસની ખેતી માટે સાપ્તાહિક સલાહ",
    "Timely, science-based advisories to help cotton growers make informed decisions for better crop management and higher productivity.": "કપાસ ઉગાડનારાઓને વધુ સારા પાક વ્યવસ્થાપન અને ઉચ્ચ ઉત્પાદકતા માટે માહિતગાર નિર્ણયો લેવામાં મદદ કરવા સમયસર, વિજ્ઞાન આધારિત સલાહ.",
    "Month": "મહિનો",
    "Year": "વર્ષ",
    "Search": "શોધો",
    "Language": "ભાષા",
    "All Months": "બધા મહિના",
    "All Years": "બધા વર્ષ",
    "All Languages": "બધી ભાષાઓ",
    "English": "અંગ્રેજી",
    "Hindi": "હિન્દી",
    "Gujarati": "ગુજરાતી",
    "Marathi": "મરાઠી",
    "Search by advisory title...": "સલાહના શીર્ષક દ્વારા શોધો...",
    "Reset": "રીસેટ કરો",
    "No advisories found": "કોઈ સલાહ મળી નથી",
    "Try changing the selected month, year, language or search term.": "પસંદ કરેલ મહિનો, વર્ષ, ભાષા અથવા શોધ શબ્દ બદલવાનો પ્રયાસ કરો.",
    "Available Languages": "ઉપલબ્ધ ભાષાઓ",
    "View Advisory": "સલાહ જુઓ",
    "PDF Not Available": "પીડીએફ ઉપલબ્ધ નથી",
    "Starting Date:": "શરૂઆતની તારીખ:",
    "Month:": "મહિનો:",
    "Pest Management": "જીવાત વ્યવસ્થાપન",
    "Disease Management": "રોગ વ્યવસ્થાપન",
    "Latest CICR cotton news and PDF bulletins.": "નવીનતમ સીઆઈસીઆર કપાસ સમાચાર અને પીડીએફ બુલેટિન.",
    "No Cotton News available.": "કોઈ કપાસ સમાચાર ઉપલબ્ધ નથી.",
    "View PDF →": "પીડીએફ જુઓ →",
    "Cotton Technologies": "કપાસ ટેકનોલોજી",
    "International Patents": "આંતરરાષ્ટ્રીય પેટન્ટ",
    "National Patents": "રાષ્ટ્રીય પેટન્ટ",
    "Readable technology particulars from the CICR Cotton mobile app content.": "સીઆઈસીઆર કોટન મોબાઇલ એપ સામગ્રીમાંથી ટેકનોલોજી વિગતો.",
    "No technologies available.": "કોઈ ટેકનોલોજી ઉપલબ્ધ નથી.",
    "Year of invention": "શોધનું વર્ષ",
    "Application No.": "અરજી નંબર",
    "Grant Number": "ગ્રાન્ટ નંબર",
    "Inventors": "શોધકો",
    "Status": "સ્થિતિ",
    "Remarks": "ટિપ્પણી",
    "Farmer Knowledge Portal": "ખેડૂત જ્ઞાન પોર્ટલ",
    "Cotton Research Portal": "કપાસ સંશોધન પોર્ટલ",
    "Central Institute for Cotton Research (CICR) is committed to advance cotton research and support farmers with innovative solutions for sustainable agriculture.": "કેન્દ્રીય કપાસ સંશોધન સંસ્થા (સીઆઈસીઆર) કપાસ સંશોધનને આગળ વધારવા અને ટકાઉ ખેતી માટે નવીન ઉકેલો સાથે ખેડૂતોને ટેકો આપવા પ્રતિબદ્ધ છે.",
    "Quick Links": "ઝડપી લિંક્સ",
    "Resources": "સંસાધનો",
    "Varieties & Hybrids": "જાતો અને સંકર",
    "Publications": "પ્રકાશનો",
    "Research Reports": "સંશોધન અહેવાલો",
    "Circulars & Notifications": "પરિપત્રો અને સૂચનાઓ",
    "FAQs": "વારંવાર પૂછાતા પ્રશ્નો",
    "© 2025 CICR Cotton Research. All rights reserved.": "© 2025 સીઆઈસીઆર કોટન રિસર્ચ. બધા હકો સુરક્ષિત.",
    "CICR Cotton Web App Developed By": "સીઆઈસીઆર કોટન વેબ એપ વિકસાવવામાં આવી",
    "Contrast": "કોન્ટ્રાસ્ટ",
    "Read": "વાંચો",
    "Back to": "પાછા",
    "Back": "પાછળ",
    "list": "યાદી",
    "Pin": "પિન",
    "Tel": "ટેલ",
    "Mail": "મેલ",
    "Web": "વેબ",
  },
};

function normalizeI18nKey(text) {
  return String(text || "").replace(/\s+/g, " ").trim();
}

function t(key) {
  const dict = TRANSLATIONS[state.lang];
  const normalized = normalizeI18nKey(key);
  return (dict && dict[normalized]) || key;
}

const I18N_SKIP_SELECTOR = "script, style, #languageSelect, #desktopLanguageSelect, input, textarea";

function translateTextNode(node) {
  if (node.__i18nOriginal === undefined) node.__i18nOriginal = node.nodeValue;
  const original = node.__i18nOriginal;
  if (state.lang === "en") {
    node.nodeValue = original;
    return;
  }
  const match = original.match(/^(\s*)([\s\S]*?)(\s*)$/);
  const lead = match[1];
  const core = match[2];
  const trail = match[3];
  const dict = TRANSLATIONS[state.lang];
  const translated = dict && dict[normalizeI18nKey(core)];
  node.nodeValue = translated ? `${lead}${translated}${trail}` : original;
}

function applyTranslations(root = document.body) {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      if (!node.nodeValue || !normalizeI18nKey(node.nodeValue)) return NodeFilter.FILTER_REJECT;
      const parent = node.parentElement;
      if (!parent || parent.closest(I18N_SKIP_SELECTOR)) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    },
  });
  const nodes = [];
  let current = walker.nextNode();
  while (current) {
    nodes.push(current);
    current = walker.nextNode();
  }
  nodes.forEach(translateTextNode);

  root.querySelectorAll("[placeholder]").forEach((el) => {
    if (el.dataset.i18nPlaceholder === undefined) el.dataset.i18nPlaceholder = el.getAttribute("placeholder");
    const dict = TRANSLATIONS[state.lang];
    const translated = state.lang !== "en" && dict && dict[normalizeI18nKey(el.dataset.i18nPlaceholder)];
    el.setAttribute("placeholder", translated || el.dataset.i18nPlaceholder);
  });
}

function setLanguage(lang) {
  const nextLang = ["en", "hi", "gu"].includes(lang) ? lang : "en";
  state.lang = nextLang;
  try {
    localStorage.setItem("cicrCottonLang", nextLang);
  } catch (e) {
    // localStorage unavailable; language will reset next visit
  }
  const mobileSelect = document.querySelector("#languageSelect");
  const desktopSelect = document.querySelector("#desktopLanguageSelect");
  if (mobileSelect) mobileSelect.value = nextLang;
  if (desktopSelect) desktopSelect.value = nextLang;
  render();
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
  drawerNav.innerHTML = navItems.map(drawerButton).join("")
    + `<div class="drawer-section-label">Research &amp; Resources</div>`
    + drawerItems.slice(navItems.length).map(drawerButton).join("");
  document.querySelector("#desktopNav").innerHTML = desktopNavItems.map(([id, label]) => `<button data-view="${id}">${label}</button>`).join("");

  bottomNav.addEventListener("click", onNavClick);
  drawerNav.addEventListener("click", onNavClick);
  pageFooter.addEventListener("click", onNavClick);
  document.querySelector("#desktopNav").addEventListener("click", onNavClick);
  document.querySelector(".desktop-brand").addEventListener("click", onNavClick);
  document.querySelector("#menuBtn").addEventListener("click", openDrawer);
  drawerScrim.addEventListener("click", closeDrawer);
  document.querySelector("#desktopA11y").addEventListener("click", () => document.querySelector("#a11yPanel").classList.toggle("open"));
  document.querySelector("#languageSelect").value = state.lang;
  document.querySelector("#desktopLanguageSelect").value = state.lang;
  document.querySelector("#languageSelect").addEventListener("change", (event) => setLanguage(event.target.value));
  document.querySelector("#desktopLanguageSelect").addEventListener("change", (event) => setLanguage(event.target.value));
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
    scrollToTop();
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
  return `<button data-view="${id}"><span class="drawer-icon">${icon(iconName)}</span><span class="drawer-label">${label}</span></button>`;
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
  scrollToTop();
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
  document.body.style.overflow = "hidden";
}

function closeDrawer() {
  drawer.classList.remove("open");
  drawerScrim.classList.remove("open");
  document.body.style.overflow = "";
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: "auto" });
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
  applyTranslations();
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
}

function renderHome() {
  view.className = "landing-view";
  view.innerHTML = `
    <section class="landing-hero">
      <div class="landing-copy">
        <h2>Empowering Cotton Farming<br>Through Research</h2>
        <p>Your comprehensive guide to cotton farming</p>
        <div class="landing-buttons">
          <button class="landing-primary" data-view="varieties">Explore Research <span>→</span></button>
          <button class="landing-secondary" data-view="advisory">Weekly Advisory <span>→</span></button>
        </div>
      </div>
      <div class="landing-hero-media">
        <img src="${assetPath(appData.banners[state.heroIndex])}" alt="Cotton research field visit">
      </div>
    </section>
    <section class="landing-resources">
      <h2>Explore Cotton Research &amp; Resources</h2>
      <p>Access our research, technologies and resources to enhance cotton productivity and sustainability.</p>
      <div class="resource-grid">
      ${featureCards.map(([target, iconName, title, color]) => `
        <article class="resource-card" data-view="${target}" style="--accent:${color};--soft:${soft(color)}">
          <span class="resource-icon">${featureIcon(target, iconName)}</span>
          <div>
            <h3>${title}</h3>
            <p>${resourceDescription(target)}</p>
          </div>
          <span class="resource-arrow">→</span>
        </article>`).join("")}
      </div>
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
      <div class="vr-zone-section">
        <div class="vr-zone-section-head">
          <h3>Select Your Cotton-Growing Zone</h3>
          <p>Choose a zone to view recommended cotton varieties and hybrids.</p>
        </div>
        <div class="zone-grid">
          ${zones.map((zone) => `
            <button class="zone-card" data-zone="${zone.name}" style="--zone:${zone.accent}">
              <div class="zone-card-top">
                <span class="zone-icon"></span>
                <div class="zone-card-copy">
                  <strong>${zone.name}</strong>
                  <small>${zone.region}</small>
                </div>
              </div>
              <div class="zone-card-foot">
                <em>${appData.varieties.filter((item) => item.category === zone.name).length}+ ${t("varieties")}</em>
                <span class="zone-card-cta">${t("Explore \u2192")}</span>
              </div>
            </button>
          `).join("")}
        </div>
      </div>
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
    <div class="vr-listing-header">
      <button class="vr-back-btn" id="zoneBack"><span class="btn-arrow" aria-hidden="true">←</span> Varieties and Hybrids</button>
      <div class="vr-listing-meta">
        <h2>${state.varietyZone}</h2>
        <span class="vr-listing-count">${items.length} ${t("varieties and hybrids")}</span>
      </div>
    </div>
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
  scrollToTop();
}

function openVarietyDetail(itemOrSlug) {
  const slug = typeof itemOrSlug === "string" ? itemOrSlug : itemSlug(itemOrSlug);
  state.view = "varieties";
  state.varietyItem = slug;
  if (state.historyReady) {
    history.pushState({ view: "varieties", varietyZone: state.varietyZone, varietyItem: slug, detailSlug: null }, "", pathForState("varieties", state.varietyZone, slug));
  }
  render();
  scrollToTop();
}

function openDetail(viewId, item) {
  if (!item) return;
  state.view = viewId;
  state.detailSlug = itemSlug(item);
  if (state.historyReady) {
    history.pushState({ view: viewId, varietyZone: null, varietyItem: null, detailSlug: state.detailSlug }, "", pathForState(viewId, null, null, state.detailSlug));
  }
  render();
  scrollToTop();
}

function closeDetail(viewId) {
  state.view = viewId;
  state.detailSlug = null;
  if (state.historyReady) {
    history.pushState({ view: viewId, varietyZone: null, varietyItem: null, detailSlug: null }, "", pathForState(viewId, null, null, null));
  }
  render();
  scrollToTop();
}

function renderVarietyDetail(item, items) {
  const title = item.detailTitle || item.name;
  const currentIndex = Math.max(0, items.findIndex((entry) => itemSlug(entry) === itemSlug(item)));
  const previous = items[(currentIndex - 1 + items.length) % items.length];
  const next = items[(currentIndex + 1) % items.length];
  view.className = "content wide variety-detail-page";
  view.innerHTML = `
    <div class="variety-detail-panel">
      <div class="variety-detail-copy">
        <button class="vr-back-btn" id="zoneBack"><span class="btn-arrow" aria-hidden="true">←</span> ${state.varietyZone}</button>
        <span class="vr-zone-badge">${state.varietyZone}</span>
        <h2>${title}</h2>
        <p>${item.description || "Cotton variety or hybrid available in CICR Cotton mobile app assets."}</p>
        ${renderVarietyPointList(item)}
      </div>
      ${item.image ? `
        <figure class="variety-detail-figure">
          <img src="${assetPath(item.image)}" alt="${title}" loading="lazy">
          <figcaption>${title}</figcaption>
        </figure>
      ` : `<div class="variety-detail-figure variety-no-image"><span>No image available</span></div>`}
    </div>
    ${item.sections ? renderSections(item.sections) : ""}
    <nav class="variety-detail-actions" aria-label="Variety navigation">
      <button class="outline-link" type="button" data-variety-link="${itemSlug(previous)}">
        <small><span class="btn-arrow" aria-hidden="true">←</span> ${t("Previous")}</small>
        <span>${previous.name}</span>
      </button>
      <button class="solid-link" type="button" data-variety-link="${itemSlug(next)}">
        <small>${t("Next")} <span class="btn-arrow" aria-hidden="true">→</span></small>
        <span>${next.name}</span>
      </button>
    </nav>
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
        <li class="spec-row">
          <span class="point-check" aria-hidden="true">&#10003;</span>
          <div class="spec-content">
            <span class="spec-label">${label}</span>
            <span class="spec-value">${value}</span>
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
    <section class="about-cicr-hero">
      <div class="about-cicr-hero-bg" style="background-image: url('${assetPath("assets/banner/bann1.JPG")}');"></div>
      <div class="about-cicr-hero-content">
        <h2>About ICAR-CICR</h2>
        <p>Science. Innovation. Impact.</p>
      </div>
    </section>
    
    <section class="about-cicr-institute">
      <article class="institute-content">
        <span class="section-kicker">The Institute</span>
        <p>ICAR-Central Institute for Cotton Research (ICAR-CICR) was established at Nagpur, in 1976. The main goal of providing scientific leadership in cotton research. It has two regional stations located at Sirsa, Haryana and Coimbatore, Tamil Nadu. These centres cater to the needs of north and south India, respectively.</p>
        <button class="btn-secondary-outline" data-view="contact">Know More About CICR <span class="cta-arrow">&rarr;</span></button>
      </article>
      <div class="institute-image">
        <img src="${assetPath("assets/banner/bann2.JPG")}" alt="ICAR CICR building">
      </div>
    </section>
    
    <section class="mission-mandate-grid">
      <article class="mission-card">
        <div class="card-header">
          <span class="card-badge">M</span>
          <h3>Mission</h3>
        </div>
        <div class="card-body">
          <p>To accelerate growth in national cotton productivity and minimize yield gaps by developing farm technologies for the different agro-ecoregions and to provide products and services to various stakeholders.</p>
        </div>
      </article>
      
      <article class="mission-card">
        <div class="card-header">
          <span class="card-badge">R</span>
          <h3>Mandate</h3>
        </div>
        <div class="card-body">
          <ul>
            <li>Basic, strategic and adaptive research on cotton production, protection, fibre quality and value addition.</li>
            <li>Technology assessment, refinement and frontline demonstrations.</li>
            <li>Capacity building and human resource development.</li>
          </ul>
        </div>
      </article>
    </section>
    
    <section class="facts-strip">
      <div class="fact-item">
        <strong>1976</strong>
        <span>Established at Nagpur</span>
      </div>
      <div class="fact-item">
        <strong>2</strong>
        <span>Regional Stations</span>
      </div>
      <div class="fact-item">
        <strong>Serving</strong>
        <span>North and South India</span>
      </div>
      <div class="fact-item">
        <strong>Science Led</strong>
        <span>Cotton research</span>
      </div>
      <div class="fact-item">
        <strong>Impact Driven</strong>
        <span>Innovations for farmers</span>
      </div>
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
      <section class="vr-page-hero about-app-hero">
        <div class="about-hero-text">
          <span class="vr-page-eyebrow">ICAR-CICR Mobile Application</span>
          <h2 class="vr-page-title">About Developers</h2>
          <p class="vr-page-desc">Meet the team behind the CICR Cotton mobile app and web portal.</p>
        </div>
      </section>

      <section class="developer-section">
        <h3 class="developer-heading">About Developers</h3>
        <div class="developer-grid">
          ${developerBox("Published By", "<strong>Dr. Vijay N. Waghmare</strong><br>Director, ICAR-CICR, Nagpur")}
          ${developerBox("Lead Developer", "<strong>Dr. V. S. Nagrare</strong>")}
          ${developerBox("Co-Developers", "Dr. S. Manickam<br>Dr. Rahul Fuke<br>Dr. Babasaheb B. Fand<br>Dr. Dipak Nagrale<br>Dr. G.I. Ramakrushna<br>Dr. Amarpreet Singh<br>Dr. K. Velmourougane<br>Dr. K Rameash")}
          ${developerBox("Hindi Translation", "Dr. Rachna Pande<br>Dr. Pooja Verma")}
          ${developerBox("Software Providers", "<strong>Zappkode Solutions</strong><br>Nagpur")}
        </div>
      </section>
    `;
    return;
  }

  view.innerHTML = `
    <section class="vr-page-hero about-app-hero">
      <div class="about-hero-text">
        <span class="vr-page-eyebrow">ICAR-CICR Mobile Application</span>
        <h2 class="vr-page-title">About App</h2>
        <p class="vr-page-desc">Your comprehensive guide to cotton farming, available anytime, anywhere.</p>
      </div>

      <div class="store-buttons">
        <a href="https://play.google.com/store/apps/details?id=cicr.com.cicr.cicrcottonapp" class="btn-store" target="_blank" rel="noopener">
          <svg viewBox="0 0 512 512" fill="currentColor"><path d="M325.3 234.3L104.6 13l280.8 161.2-60.1 60.1zM47 0C34 6.8 25.3 19.2 25.3 35.3v441.3c0 16.1 8.7 28.5 21.7 35.3l256.6-256L47 0zm425.2 225.6l-58.9-34.1-65.7 64.5 65.7 64.5 60.1-34.1c18-14.3 18-46.5-1.2-60.8zM104.6 499l280.8-161.2-60.1-60.1L104.6 499z"/></svg>
          <div class="btn-store-text">
            <span>GET IT ON</span>
            <strong>Google Play</strong>
          </div>
        </a>
        <a href="https://apps.apple.com/in/app/cicr-cotton/id6755037932" class="btn-store" target="_blank" rel="noopener">
          <svg viewBox="0 0 384 512" fill="currentColor"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>
          <div class="btn-store-text">
            <span>Download on the</span>
            <strong>App Store</strong>
          </div>
        </a>
      </div>
    </section>

    <section class="about-app-grid">
      <article class="about-info-card">
        <div class="about-info-header">
          <h3>About the App</h3>
        </div>
        <div class="about-info-list">
          <div class="info-block">
            <span class="info-block-icon">✓</span>
            <div class="info-block-content">
              <strong>User Friendly</strong>
              <p>Software tool developed to support the cotton stakeholders involved with cotton production.</p>
            </div>
          </div>
          <div class="info-block">
            <span class="info-block-icon">✓</span>
            <div class="info-block-content">
              <strong>Complete Cotton Information</strong>
              <p>Covers A to Z about cotton cultivation including crop improvement, crop production and crop protection.</p>
            </div>
          </div>
          <div class="info-block">
            <span class="info-block-icon">✓</span>
            <div class="info-block-content">
              <strong>Offline Access</strong>
              <p>The user can refer to the information at any time in offline mode as well.</p>
            </div>
          </div>
          <div class="info-block">
            <span class="info-block-icon">✓</span>
            <div class="info-block-content">
              <strong>Lightweight</strong>
              <p>The size of the app is 45 MB, allowing users to download it in no time.</p>
            </div>
          </div>
          <div class="info-block">
            <span class="info-block-icon">✓</span>
            <div class="info-block-content">
              <strong>Target Users</strong>
              <p>Targeted end users include Farmers, Students, Researchers, State Department personnel, Extension functionaries, KVK personnel and Policy makers.</p>
            </div>
          </div>
        </div>
        <a class="privacy-link" href="https://cicr.org.in/privacypolicy/" target="_blank" rel="noopener">Privacy Policy <span class="cta-arrow">&rarr;</span></a>
      </article>

      <article class="app-showcase">
        <div class="app-showcase-bg"></div>
        <img class="app-phone-image" src="${assetPath("assets/images/mobilepng.png")}" alt="Cotton Knowledge App Preview">
      </article>
    </section>
  `;
}

function developerBox(title, body) {
  return `<article class="developer-box"><span class="dev-role">${title}</span><p class="dev-names">${body}</p></article>`;
}

const CONTACT_ICON_PATHS = {
  pin: '<path d="M10 17.5S16 12 16 8a6 6 0 0 0-12 0c0 4 6 9.5 6 9.5Z"/><circle cx="10" cy="8" r="2.2"/>',
  phone: '<path d="M6.6 3.5 8.8 6a1 1 0 0 1-.2 1.3L7.3 8.5c.9 1.8 2.4 3.3 4.2 4.2l1.2-1.3a1 1 0 0 1 1.3-.2l2.5 2.2c.4.4.5 1 .1 1.4l-1.2 1.4c-.4.5-1 .7-1.6.6-4-.9-7.5-4.4-8.4-8.4-.1-.6.1-1.2.6-1.6l1.4-1.2c.4-.4 1-.3 1.4.1Z"/>',
  fax: '<rect x="4" y="7.5" width="12" height="8.5" rx="1.4"/><path d="M6 7.5V4.5a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v3"/><line x1="7" y1="11" x2="13" y2="11"/>',
  mail: '<rect x="3" y="5" width="14" height="10" rx="1.5"/><path d="M3.5 6 10 11l6.5-5"/>',
  web: '<circle cx="10" cy="10" r="7"/><path d="M3.2 10h13.6M10 3.2c2 2 2 11.6 0 13.6M10 3.2c-2 2-2 11.6 0 13.6"/>',
};

function contactIcon(key) {
  const path = CONTACT_ICON_PATHS[key] || CONTACT_ICON_PATHS.pin;
  return `<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${path}</svg>`;
}

const CONTACT_LABELS = {
  pin: "Address",
  phone: "Telephone",
  fax: "Fax",
  web: "Website",
  mail: "Email",
};

function renderContact() {
  view.className = "content contact-view";
  const offices = [
    { name: "ICAR- Central Institute for Cotton Research (Nagpur)", rows: [["pin", "Post Bag No. 2, Shankar Nagar PO, Nagpur, Maharashtra, India, Pincode-440010"], ["phone", "07103-275536/37/38/39"], ["fax", "07103-275529"], ["web", "http://www.cicr.org.in"], ["mail", "cicrnagpur@gmail.com"]] },
    { name: "ICAR- Central Institute For Cotton Research (Coimbatore)", rows: [["pin", "Coimbatore (Tamil Nadu), Pincode-641003"], ["phone", "0422-2430045"], ["fax", "0422-2454021"], ["web", "http://www.cicr.org.in"], ["mail", "cicrcbe@gmail.com"]] },
    { name: "ICAR- Central Institute for Cotton Research (Sirsa)", rows: [["pin", "Sirsa (Haryana), Pincode- 125055"], ["phone", "01666-220428"], ["fax", "01666-230271"], ["web", "http://www.cicr.org.in"], ["mail", "cicrsirsa@yahoo.co.in"]] },
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
      <div>${contactIcon("pin")}<strong>Nagpur</strong><small>Maharashtra</small></div>
      <div>${contactIcon("pin")}<strong>Coimbatore</strong><small>Tamil Nadu</small></div>
      <div>${contactIcon("pin")}<strong>Sirsa</strong><small>Haryana</small></div>
    </section>
    <section class="enquiry-strip">
      <div class="enquiry-icon">${contactIcon("mail")}</div>
      <div>
        <h3>Have an Enquiry?</h3>
        <p>We're here to help! Reach out to any of our centres or email us for general queries.</p>
      </div>
      <a href="mailto:cicrnagpur@gmail.com">Send Enquiry <span class="cta-arrow">&rarr;</span></a>
    </section>
  `;
  view.querySelectorAll("[data-view]").forEach((el) => el.addEventListener("click", onNavClick));
}

function contactCard(office) {
  return `<article class="contact-card"><h2>${office.name}</h2>
    ${office.rows.map(([iconName, text]) => `
      <div class="contact-row">
        <span class="contact-icon">${contactIcon(iconName)}</span>
        <span class="contact-field">
          <span class="contact-label">${CONTACT_LABELS[iconName] || ""}</span>
          <span class="contact-value">${text}</span>
        </span>
      </div>
    `).join("")}
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
      <span class="advisory-eyebrow">Advisory</span>
      <h2>Weekly Advisory for Cotton Cultivation</h2>
      <p>Timely, science-based advisories to help cotton growers make informed decisions for better crop management and higher productivity.</p>
    </section>
    <section class="advisory-filters">
      <label>Month<select><option>All Months</option><option>August</option><option>July</option></select></label>
      <label>Year<select><option>All Years</option><option>2026</option><option>2024</option></select></label>
      <label>Search<span class="search-wrap"><input type="search" placeholder="Search by advisory title..."><button aria-label="Search">${searchIcon()}</button></span></label>
      <label>Language<select><option>All Languages</option><option>English</option><option>Hindi</option><option>Marathi</option></select></label>
      <button class="reset-filter">Reset</button>
    </section>
    ${visibleCards.length ? `
      <section class="advisory-grid">
        ${visibleCards.map(advisoryCard).join("")}
      </section>
      ${renderPagination(state.advisoryPage, totalPages)}
    ` : `
      <section class="advisory-empty">
        <h3>No advisories found</h3>
        <p>Try changing the selected month, year, language or search term.</p>
      </section>
    `}
  `;
  bindAdvisoryPagination(totalPages);
}

function searchIcon() {
  return `<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="9" r="6"/><line x1="17" y1="17" x2="13.2" y2="13.2"/></svg>`;
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
    <button class="pagination-nav" data-page="prev" ${currentPage === 1 ? "disabled" : ""}><span class="btn-arrow" aria-hidden="true">←</span> ${t("Previous")}</button>
    ${pages.map((page) => `<button data-page="${page}" class="${page === currentPage ? "active" : ""}">${page}</button>`).join("")}
    <button class="pagination-nav" data-page="next" ${currentPage === totalPages ? "disabled" : ""}>${t("Next")} <span class="btn-arrow" aria-hidden="true">→</span></button>
  </nav>`;
}

function bindAdvisoryPagination(totalPages) {
  view.querySelector(".advisory-pagination")?.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-page]");
    if (!button || button.disabled) return;
    const page = button.dataset.page;
    if (page === "prev") state.advisoryPage = Math.max(1, state.advisoryPage - 1);
    else if (page === "next") state.advisoryPage = Math.min(totalPages, state.advisoryPage + 1);
    else state.advisoryPage = Number(page);
    renderAdvisory();
    applyTranslations();
    scrollToTop();
  });
}

function advisoryCard(item) {
  return `<article class="advisory-card">
    <div class="advisory-card-top">
      <span class="week-badge">${item.week}</span>
      <span class="advisory-kind">Advisory</span>
    </div>
    <h2>${item.title}</h2>
    <p><span class="field-label">${t("Starting Date:")}</span> ${item.date}<br><span class="field-label">${t("Month:")}</span> ${item.month}</p>
    <p class="available-label">Available Languages</p>
    <div class="chips">${item.languages.map(([lang, file]) => file ? `<a href="${file}" target="_blank" rel="noopener">${lang}</a>` : `<span>${lang}</span>`).join("")}</div>
    ${item.file ? `<a class="view-advisory" href="${item.file}" target="_blank" rel="noopener">View Advisory <span class="cta-arrow">&rarr;</span></a>` : `<button class="view-advisory" disabled>PDF Not Available</button>`}
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
  const imagePosition = viewId === "facts" ? "top" : undefined;
  view.innerHTML = `<h2>${pageTitles[viewId]}</h2><div class="collection-grid">${items.map((item, index) => dataCard(item, index, imagePosition)).join("")}</div>`;
  bindDataCards(items, (item) => openDetail(viewId, item));
}

function dataCard(item, index, imagePosition) {
  const positionStyle = imagePosition ? ` style="object-position:${imagePosition}"` : "";
  return `<article class="data-card" data-index="${index}" role="button" tabindex="0">
    <div class="data-card-img-wrap">
      <img src="${assetPath(item.image)}" alt="${item.name}" loading="lazy"${positionStyle}>
    </div>
    <div class="data-card-body">
      <h3>${item.name}</h3>
      <p>${item.description || ""}</p>
      <span class="data-card-cta">→</span>
    </div>
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
  view.innerHTML = `<h2>Farmers Outreach</h2><div class="collection-grid collection-grid--spread">${items.map(dataCard).join("")}</div>`;
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
      <button class="inline-back" id="detailBack">${t("Back to")} ${t(pageTitles[viewId] || "list")}</button>
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

function techCard(item) {
  const paddedNo = String(item.slNo || "").padStart(2, "0");
  return `
    <article class="tech-card">
      <div class="tech-badge">${paddedNo}</div>
      <div class="tech-card-content">
        <h3 class="tech-title">${item.name}</h3>
        <div class="tech-meta">
          ${item.year ? `<div class="tech-meta-row"><span class="tech-meta-label">Year of invention</span><span class="tech-meta-value">${item.year}</span></div>` : ""}
          ${item.applicationNo ? `<div class="tech-meta-row"><span class="tech-meta-label">Application No.</span><span class="tech-meta-value">${item.applicationNo}</span></div>` : ""}
          ${item.grantNumber ? `<div class="tech-meta-row"><span class="tech-meta-label">Grant Number</span><span class="tech-meta-value">${item.grantNumber}</span></div>` : ""}
          ${item.inventors ? `<div class="tech-meta-row"><span class="tech-meta-label">Inventors</span><span class="tech-meta-value">${item.inventors}</span></div>` : ""}
          ${item.status ? `<div class="tech-meta-row"><span class="tech-meta-label">Status</span><span class="tech-meta-value">${item.status}</span></div>` : ""}
          ${item.remarks ? `<div class="tech-meta-row"><span class="tech-meta-label">Remarks</span><span class="tech-meta-value">${item.remarks}</span></div>` : ""}
        </div>
      </div>
    </article>
  `;
}

const TECH_TABS = [
  ["technologies", "Cotton Technologies"],
  ["international", "International Patents"],
  ["national", "National Patents"],
];

function renderCottonTech() {
  const datasets = {
    technologies: mobileDetails.cottonTechnologies || [],
    international: mobileDetails.internationalPatents || [],
    national: mobileDetails.nationalPatents || [],
  };
  const totalCount = Object.values(datasets).reduce((sum, list) => sum + list.length, 0);

  view.className = "content tech-view";

  if (!totalCount) {
    view.innerHTML = `
      <section class="tech-hero">
        <h2>Cotton Technologies</h2>
        <p>Readable technology particulars from the CICR Cotton mobile app content.</p>
      </section>
      <div class="tech-empty-state">
        <p>No technologies available.</p>
      </div>
    `;
    return;
  }

  const activeItems = datasets[state.techTab] || [];
  view.innerHTML = `
    <section class="tech-hero">
      <h2>Cotton Technologies</h2>
      <p>Readable technology particulars from the CICR Cotton mobile app content.</p>
    </section>
    <div class="tech-tabs">
      ${TECH_TABS.map(([id, label]) => `<button class="tech-tab${state.techTab === id ? " active" : ""}" data-tech-tab="${id}">${label}</button>`).join("")}
    </div>
    <div class="tech-list">${activeItems.map(techCard).join("")}</div>
  `;
  view.querySelectorAll("[data-tech-tab]").forEach((button) => {
    button.addEventListener("click", () => {
      state.techTab = button.dataset.techTab;
      renderCottonTech();
      applyTranslations();
      scrollToTop();
    });
  });
}

function renderNews() {
  view.className = "content news-view";
  const fallbackNews = [
    { name: "Issue 34", description: "November 19, 2024", file: "http://128.199.7.234/media/news_articles/Issue_No34_19th_Nov_2024_241119_184108.pdf" },
    { name: "Issue 39", description: "December 24, 2024", file: "http://128.199.7.234/media/news_articles/Issue_No.39_24th_December_2024.pdf" },
    { name: "Issue 01", description: "August 9, 2025", file: "http://128.199.7.234/media/news_articles/TSV_leaf_folder_2023.pdf" },
  ];
  const items = appData.liveNews?.length ? appData.liveNews : fallbackNews;
  
  if (!items.length) {
    view.innerHTML = `
      <section class="news-hero">
        <h2>Cotton News</h2>
        <p>Latest CICR cotton news and PDF bulletins.</p>
      </section>
      <div class="news-empty-state">
        <p>No Cotton News available.</p>
      </div>
    `;
    return;
  }
  
  view.innerHTML = `
    <section class="news-hero">
      <h2>Cotton News</h2>
      <p>Latest CICR cotton news and PDF bulletins.</p>
    </section>
    <section class="news-list">
      ${items.map((item) => `
        <a class="news-card" href="${item.file || "#"}" target="_blank" rel="noopener">
          <div class="news-card-content">
            <div class="news-header">
              <span class="news-issue">${item.name}</span>
              <span class="news-date">${item.description}</span>
            </div>
          </div>
          <div class="news-action">
            <span class="pdf-badge">PDF</span>
            <span class="view-pdf-text">View PDF &rarr;</span>
          </div>
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
      ? `<div class="detail-media-frame"><img class="detail-media lightbox-trigger" src="${assetPath(item.image)}" alt="${title}"></div>`
      : "";
  return `
    <article class="detail-shell">
      <div class="detail-hero${media ? "" : " no-media"}">
        <div class="detail-hero-copy">
          <h2>${title}</h2>
          ${item.description ? `<p class="detail-intro">${item.description}</p>` : ""}
        </div>
        ${media ? `<div class="detail-hero-media">${media}</div>` : ""}
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

let a11yZoom = 1;

function setupAccessibility() {
  const fab = document.querySelector("#accessibilityFab");
  const panel = document.querySelector("#a11yPanel");
  fab.addEventListener("click", () => panel.classList.toggle("open"));
  panel.addEventListener("click", (event) => {
    const button = event.target.closest("[data-a11y]");
    const action = button?.dataset.a11y;
    if (!action) return;
    if (action === "fontUp") {
      a11yZoom = Math.min(a11yZoom + 0.1, 1.6);
      document.body.style.zoom = a11yZoom;
    }
    if (action === "fontDown") {
      a11yZoom = Math.max(a11yZoom - 0.1, 0.7);
      document.body.style.zoom = a11yZoom;
    }
    if (action === "contrast") document.body.classList.toggle("high-contrast");
    if (action === "read") toggleReadAloud(button);
  });
}

function toggleReadAloud(button) {
  if (speechSynthesis.speaking) {
    speechSynthesis.cancel();
    button?.classList.remove("active");
    return;
  }
  const utterance = new SpeechSynthesisUtterance(document.body.innerText.slice(0, 1200));
  utterance.onend = () => button?.classList.remove("active");
  utterance.onerror = () => button?.classList.remove("active");
  speechSynthesis.speak(utterance);
  button?.classList.add("active");
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
