/**
 * Honcho Memory Persistence Client for Node.js / ESM
 * Provides dialectic context, cross-iteration memory, and reverse engineering logs.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export class HonchoMemoryManager {
  constructor(sessionId = 'default-loop-session', storageDir = null) {
    this.sessionId = sessionId;
    this.storageDir = storageDir || path.join(__dirname, 'storage');
    if (!fs.existsSync(this.storageDir)) {
      fs.mkdirSync(this.storageDir, { recursive: true });
    }
    this.sessionFile = path.join(this.storageDir, `${this.sessionId}_session.json`);
    this.learningsFile = path.join(this.storageDir, `${this.sessionId}_learnings.jsonl`);
    this.state = this._loadSession();
  }

  _loadSession() {
    if (fs.existsSync(this.sessionFile)) {
      try {
        const raw = fs.readFileSync(this.sessionFile, 'utf-8');
        return JSON.parse(raw);
      } catch (err) {
        console.error('Failed to parse existing session, creating new:', err.message);
      }
    }
    return {
      session_id: this.sessionId,
      created_at: Date.now(),
      updated_at: Date.now(),
      user_profile: {
        preferred_invariants: [],
        stop_condition_sensitivity: 'strict',
        budget_ceiling_usd: 10.0
      },
      loop_goal: null,
      active_invariant: null,
      messages: [],
      learnings: []
    };
  }

  _saveSession() {
    this.state.updated_at = Date.now();
    fs.writeFileSync(this.sessionFile, JSON.stringify(this.state, null, 2), 'utf-8');
  }

  setLoopAgreement(goal, invariant, stopConditions = {}) {
    this.state.loop_goal = goal;
    this.state.active_invariant = invariant;
    this.state.stop_conditions = stopConditions;
    this.addMessage('system', `Loop Goal Agreed: ${goal}`);
    this.addMessage('system', `Loop Invariant Established: ${invariant}`);
    this._saveSession();
  }

  addMessage(role, content, metadata = {}) {
    const msg = {
      role,
      content,
      timestamp: Date.now(),
      metadata
    };
    this.state.messages.push(msg);
    this._saveSession();
  }

  recordLearning(iteration, finding, causalFactor, rubricDelta = null) {
    const entry = {
      iteration,
      finding,
      causal_factor: causalFactor,
      rubric_delta: rubricDelta,
      timestamp: Date.now()
    };
    this.state.learnings.push(entry);
    this._saveSession();
    fs.appendFileSync(this.learningsFile, JSON.stringify(entry) + '\n', 'utf-8');
  }

  getContextForPrompt(maxMessages = 10) {
    const lines = [];
    if (this.state.loop_goal) {
      lines.push(`### CURRENT LOOP GOAL:\n${this.state.loop_goal}\n`);
    }
    if (this.state.active_invariant) {
      lines.push(`### MANDATORY LOOP INVARIANT:\n${this.state.active_invariant}\n`);
    }

    const learnings = this.state.learnings || [];
    if (learnings.length > 0) {
      lines.push('### REVERSE-ENGINEERED SUCCESS FACTORS (PREVIOUS ITERATIONS):');
      for (const item of learnings.slice(-5)) {
        lines.push(`- [Iter ${item.iteration}] ${item.finding} (Cause: ${item.causal_factor})`);
      }
      lines.push('');
    }

    const recentMsgs = (this.state.messages || []).slice(-maxMessages);
    if (recentMsgs.length > 0) {
      lines.push('### RECENT DIALECTIC HISTORY:');
      for (const m of recentMsgs) {
        lines.push(`${m.role.toUpperCase()}: ${m.content}`);
      }
    }

    return lines.join('\n');
  }
}
