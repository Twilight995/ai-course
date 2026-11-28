async function ask(prompt, imageUrl) {
  const content = [{ type: "text", text: prompt }];
  if (imageUrl) content.push({ type: "image_url", image_url: { url: imageUrl } });
  const r = await fetch("https://krchoi.com/gemma4/v1/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ model: "gemma4", messages: [{ role: "user", content: content }] })
  });
  const data = await r.json();
  return data.choices[0].message.content;
}

function checkSummary(text, info) {
  if (typeof text !== "string") return false;
  if (text.trim() === "") return false;
  if (text.length > 200) return false;
  const numbers = text.match(/\d+(?:\.\d+)?/g) || [];
  if (numbers.some(num => !info.allowed.includes(num))) return false;
  if (info.banned.some(banned => text.includes(banned))) return false;
  if (!numbers.includes("7")) return false;
  if (info.count > 0 && !numbers.includes(String(info.count))) return false;
  return true;
}

function showSummary(label, text) {
  const box = document.getElementById("summary");
  if (!box) return;
  const strong = box.querySelector("strong");
  const p = box.querySelector("p");
  if (strong) strong.textContent = label;
  if (p) p.textContent = text;
}

async function loadSummary(key) {
  const info = SITE.summary[key];
  let label = info.saved_label;
  let text = info.saved;
  showSummary("요약", "AI 요약을 받는 중입니다");
  try {
    const timeoutPromise = new Promise((_, reject) => setTimeout(() => reject(), 6000));
    const answer = await Promise.race([ask(info.prompt), timeoutPromise]);
    if (checkSummary(answer, info)) {
      label = "AI 요약";
      text = answer.trim();
    }
  } catch (e) {}
  if (new URLSearchParams(location.hash.slice(1)).get("region") === key) {
    showSummary(label, text);
  }
}