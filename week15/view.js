function parseHash() {
  const p = new URLSearchParams(location.hash.slice(1));
  return {
    sido: p.get("sido") || "",
    domain: p.get("domain") || "",
    region: p.get("region") || ""
  };
}

function makeHash(sido, domain) {
  const parts = [];
  if (sido) parts.push("sido=" + encodeURIComponent(sido));
  if (domain) parts.push("domain=" + encodeURIComponent(domain));
  return "#" + parts.join("&");
}

function paint(view, domain) {
  view.querySelectorAll("svg a").forEach(a => {
    const key = decodeURIComponent(a.getAttribute("href").replace("#region=", ""));
    a.querySelector("path").setAttribute("fill", SITE.colors[key][domain]);
  });
  const info = SITE.legends[domain];
  let legendHtml = "";
  for (const [color, text] of info.legend) {
    legendHtml += `<span><span class="dot" style="background-color: ${color};"></span>${text}</span>`;
  }
  view.querySelector(".legend").innerHTML = legendHtml;
  view.querySelector(".legend + p").textContent = info.note;
  const back = view.querySelector('.btn-row a[href="#"]');
  if (back) back.setAttribute("href", makeHash("", domain));
}

function render() {
  const state = parseHash();
  const view = document.getElementById("view");
  window.scrollTo(0, 0);
  if (state.region !== "") {
    if (state.region in SITE.regions) {
      view.innerHTML = SITE.regions[state.region];
      loadSummary(state.region);
    } else {
      view.innerHTML = SITE.missing;
    }
    return;
  }
  const known = state.sido in SITE.home;
  const domain = state.domain in SITE.legends ? state.domain : "";
  view.innerHTML = SITE.home[known ? state.sido : ""];
  if (!known) {
    view.querySelector(".filters + p").textContent = "등록된 지역 정보가 없습니다";
  }
  const form = view.querySelector("form");
  form.sido.value = known ? state.sido : "";
  form.domain.value = domain;
  form.onsubmit = (e) => {
    e.preventDefault();
    location.hash = makeHash(form.sido.value, form.domain.value);
  };
  paint(view, domain);
}

window.addEventListener("hashchange", render);
render();