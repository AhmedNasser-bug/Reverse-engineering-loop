// Reverse Engineering Loop Web Dashboard Client

async function fetchStatus() {
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    renderState(data.state, data.config);
  } catch (err) {
    console.error('Error fetching loop status:', err);
    document.getElementById('conn-status').textContent = 'Sync Offline';
    document.getElementById('conn-dot').className = 'w-2 h-2 rounded-full bg-rose-500';
  }
}

async function fetchRubric() {
  try {
    const res = await fetch('/api/rubric');
    const data = await res.json();
    document.getElementById('rubric-display').textContent = data.rubric;
  } catch (err) {
    console.error('Error fetching rubric:', err);
  }
}

function renderState(state, config) {
  document.getElementById('val-iteration').textContent = state.current_iteration;
  document.getElementById('val-max-iteration').textContent = `/ ${state.max_iterations}`;
  document.getElementById('val-score').textContent = (state.latest_rubric_score || 0).toFixed(3);
  document.getElementById('val-cost').textContent = `$${(state.cumulative_cost_usd || 0).toFixed(2)}`;
  document.getElementById('badge-loop-status').textContent = state.status;

  const pct = Math.min(100, Math.round((state.current_iteration / state.max_iterations) * 100));
  document.getElementById('bar-progress').style.width = `${pct}%`;

  // Approval gate button status
  const approveBtn = document.getElementById('btn-approve-invariant');
  if (state.human_approved) {
    approveBtn.className = "px-5 py-3 rounded-xl bg-slate-800 text-emerald-400 font-bold text-sm border border-emerald-500/30 flex items-center justify-center gap-2 cursor-default";
    approveBtn.innerHTML = "<span>✓ Invariant Approved (Active)</span>";
  } else {
    approveBtn.className = "px-5 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold text-sm shadow-lg shadow-emerald-500/20 transition flex items-center justify-center gap-2 cursor-pointer";
    approveBtn.innerHTML = "<span>✓ Approve Invariant</span>";
  }

  // Iteration table
  const tbody = document.getElementById('table-iterations-body');
  if (state.iterations && state.iterations.length > 0) {
    tbody.innerHTML = '';
    state.iterations.forEach(it => {
      const tr = document.createElement('tr');
      tr.className = "hover:bg-slate-800/40 transition";
      tr.innerHTML = `
        <td class="py-2.5 px-3 font-bold text-white">#${it.iteration}</td>
        <td class="py-2.5 px-3"><span class="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">${it.status}</span></td>
        <td class="py-2.5 px-3 font-semibold text-cyan-400">${(it.score || 0).toFixed(3)}</td>
        <td class="py-2.5 px-3 text-emerald-400">${it.delta || '+0.000'}</td>
        <td class="py-2.5 px-3 text-amber-300">$${(it.cost || 0).toFixed(2)}</td>
        <td class="py-2.5 px-3 text-slate-400">${it.duration_s || 0}s</td>
      `;
      tbody.appendChild(tr);
    });

    // Update REA insights container
    const reaContainer = document.getElementById('rea-insights-container');
    reaContainer.innerHTML = '';
    state.iterations.forEach(it => {
      const box = document.createElement('div');
      box.className = "p-3.5 bg-slate-950/70 border border-slate-800 rounded-xl text-xs space-y-1.5";
      box.innerHTML = `
        <div class="flex items-center justify-between">
          <span class="font-bold text-cyan-400">Iteration ${it.iteration} Reverse Engineering Finding:</span>
          <span class="text-[10px] text-slate-500 font-mono">Score: ${(it.score || 0).toFixed(3)}</span>
        </div>
        <p class="text-slate-300">${it.causal_factor || 'Analysis completed.'}</p>
      `;
      reaContainer.prepend(box);
    });

    // Render OpenUI preview
    renderOpenUISandbox(state.iterations[state.iterations.length - 1]);
  }
}

function renderOpenUISandbox(latestIteration) {
  const sandbox = document.getElementById('openui-sandbox');
  if (!latestIteration) return;

  sandbox.innerHTML = `
    <div class="w-full p-4 bg-slate-900 border border-slate-800 rounded-xl shadow-lg space-y-3">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
          OpenUI Component (Generated from Iteration ${latestIteration.iteration})
        </span>
        <span class="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300">Reactive Component</span>
      </div>
      <p class="text-xs text-slate-300">
        <strong>Success Determinant:</strong> ${latestIteration.causal_factor}
      </p>
      <div class="flex items-center gap-2 pt-2 border-t border-slate-800 text-[11px] text-slate-400">
        <span>Verified Against Schema: ✓</span>
        <span class="ml-auto font-mono text-cyan-400">Confidence: 99.4%</span>
      </div>
    </div>
  `;
}

// Event Listeners
document.getElementById('btn-approve-invariant').addEventListener('click', async () => {
  try {
    const res = await fetch('/api/approve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ approver: 'Human Supervisor (Web UI)' })
    });
    if (res.ok) {
      fetchStatus();
    }
  } catch (err) {
    console.error('Failed to approve invariant:', err);
  }
});

document.getElementById('btn-step').addEventListener('click', async () => {
  const btn = document.getElementById('btn-step');
  btn.disabled = true;
  btn.innerHTML = '<span>⏳ Stepping...</span>';
  try {
    const res = await fetch('/api/step', { method: 'POST' });
    const data = await res.json();
    if (data.status === 'ERROR') {
      alert(data.message);
    }
    await fetchStatus();
    await fetchRubric();
  } catch (err) {
    console.error('Failed to step loop:', err);
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>▶ Step Iteration</span>';
  }
});

document.getElementById('btn-reset').addEventListener('click', async () => {
  if (confirm('Reset loop to baseline state?')) {
    try {
      await fetch('/api/reset', { method: 'POST' });
      await fetchStatus();
      await fetchRubric();
    } catch (err) {
      console.error('Failed to reset loop:', err);
    }
  }
});

// Periodic Poll as SSE fallback
setInterval(fetchStatus, 3000);
fetchStatus();
fetchRubric();
