import re

with open("static/js/app.js", "r") as f:
    content = f.read()

badge_replacement = """// Score Badges rendering
function renderBadge(key, score, isNull = false, isModified = false) {
  const container = document.getElementById(`badge-container-${key}`);
  if (!container) return;

  const inputEl = document.getElementById(`input-${key}`);

  if (isNull) {
    container.innerHTML = `
      <div class="inline-flex items-center space-x-1 px-2.5 py-1 bg-rose-500/10 text-rose-400 border border-rose-500/20 rounded-lg text-xs font-semibold select-none pulse-danger">
        <span class="w-1.5 h-1.5 rounded-full bg-rose-500 animate-ping"></span>
        <span>%0 (Okunamadı)</span>
      </div>
    `;
    if (inputEl) {
      inputEl.classList.remove('border-slate-800', 'focus:border-indigo-500');
      inputEl.classList.add('border-rose-900/80', 'focus:border-rose-500', 'focus:ring-rose-500/20');
    }
  } else if (isModified) {
    container.innerHTML = `
      <div class="inline-flex items-center space-x-1 px-2.5 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-lg text-xs font-semibold select-none">
        <span class="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
        <span>Manuel</span>
      </div>
    `;
    if (inputEl) {
      inputEl.classList.remove('border-rose-900/80', 'border-rose-500', 'ring-2', 'ring-rose-500/20', 'bg-rose-500/5', 'pulse-danger');
      inputEl.classList.remove('border-orange-900/80', 'focus:border-orange-500', 'focus:ring-orange-500/20');
      inputEl.classList.add('border-slate-800', 'focus:border-indigo-500');
    }
  } else {
    const isGood = score >= 80;
    const isWarning = score > 0 && score < 80;
    
    let colorClass, iconClass, textClass;
    
    if (isGood) {
      colorClass = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
      iconClass = 'bg-emerald-400';
    } else if (isWarning) {
      colorClass = 'bg-orange-500/10 text-orange-400 border-orange-500/20';
      iconClass = 'bg-orange-400';
    } else {
      colorClass = 'bg-rose-500/10 text-rose-400 border-rose-500/20 pulse-danger';
      iconClass = 'bg-rose-500 animate-ping';
    }
    
    container.innerHTML = `
      <div class="inline-flex items-center space-x-1 px-2.5 py-1 ${colorClass} border rounded-lg text-xs font-semibold select-none">
        <span class="w-1.5 h-1.5 rounded-full ${iconClass}"></span>
        <span>%${score}</span>
      </div>
    `;

    if (inputEl) {
      if (isGood) {
        inputEl.classList.remove('border-rose-900/80', 'focus:border-rose-500', 'focus:ring-rose-500/20', 'border-orange-900/80', 'focus:border-orange-500', 'focus:ring-orange-500/20');
        inputEl.classList.add('border-slate-800', 'focus:border-indigo-500');
      } else if (isWarning) {
        inputEl.classList.remove('border-slate-800', 'focus:border-indigo-500', 'border-rose-900/80', 'focus:border-rose-500', 'focus:ring-rose-500/20');
        inputEl.classList.add('border-orange-900/80', 'focus:border-orange-500', 'focus:ring-orange-500/20');
      } else {
        inputEl.classList.remove('border-slate-800', 'focus:border-indigo-500', 'border-orange-900/80', 'focus:border-orange-500', 'focus:ring-orange-500/20');
        inputEl.classList.add('border-rose-900/80', 'focus:border-rose-500', 'focus:ring-rose-500/20');
      }
    }
  }
}"""

content = re.sub(r'// Score Badges rendering.*?// User inputs values', badge_replacement + "\n\n// User inputs values", content, flags=re.DOTALL)

with open("static/js/app.js", "w") as f:
    f.write(content)

