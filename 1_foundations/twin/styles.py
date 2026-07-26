"""Styling constants for the digital twin Gradio app."""

GOLD = "#2d6cdf"
BLUE = "#2d6cdf"
PURPLE = "#2d6cdf"

EXAMPLES = [
    "Tell me about your background and experience.",
    "What kinds of projects are you working on now?",
    "What are your strongest technical skills?",
    "How can I get in touch with you?",
]

CSS = """
:root {
  --twin-gold: #2d6cdf;
  --twin-blue: #2d6cdf;
  --twin-purple: #2d6cdf;
  --twin-bg: #f7f9fc;
  --twin-surface: #ffffff;
  --twin-surface-2: #f4f8ff;
  --twin-border: #e2e8f0;
  --twin-border-strong: #c9d3e3;
  --twin-text: #0f172a;
  --twin-muted: #64748b;
}

footer, .built-with, .show-api, .api-docs { display: none !important; }

html, body, gradio-app {
  background: #f7f9fc !important;
  color: var(--twin-text) !important;
}

/* ---------- Stable layout ---------- */
.gradio-container {
  background: var(--twin-surface) !important;
  color: var(--twin-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
  width: 100% !important;
  max-width: 920px !important;
  min-width: 0 !important;
  margin: 0 auto !important;
  padding: 28px 20px 48px !important;
}
.gradio-container .main, .gradio-container .contain, .gradio-container .wrap {
  width: 100% !important;
  max-width: 100% !important;
  min-width: 0 !important;
}
.gradio-container * { min-width: 0; }

/* ---------- Title ---------- */
.gradio-container h1 {
  color: var(--twin-text) !important;
  font-size: 28px !important;
  font-weight: 700 !important;
  letter-spacing: -0.03em !important;
  border-left: 3px solid var(--twin-blue) !important;
  padding-left: 12px !important;
  margin: 4px 0 10px !important;
  text-align: left !important;
}

/* Make the ChatInterface description visible and match the title color */
.gradio-container .description,
.gradio-container .lead,
.gradio-container > p {
  color: var(--twin-text) !important;
  opacity: 0.95 !important;
  font-size: 15px !important;
  margin-top: 6px !important;
}

/* ---------- Rounded structural pieces ---------- */
.chatbot, .chatbot *, .block, .form,
button, input, textarea,
.examples button {
  border-radius: 14px !important;
}

/* ---------- Block surfaces ---------- */
.block, .form { background: transparent !important; box-shadow: none !important; }

/* ---------- Hide the Chatbot label / header strip ---------- */
.chatbot > .block-label,
.chatbot > label,
.chatbot .label-wrap,
.chatbot .block-label,
.chatbot > .label-container {
  display: none !important;
}

/* ---------- Chatbot frame ---------- */
.chatbot, .chatbot.block {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  min-height: 500px !important;
  box-shadow: 0 16px 42px rgba(23, 33, 43, 0.06) !important;
}

/* Make the outer container visually match the chat block for consistency */
.gradio-container {
  border: 1px solid var(--twin-border) !important;
  box-shadow: 0 16px 42px rgba(23, 33, 43, 0.04) !important;
}
.chatbot .placeholder, .chatbot .placeholder * { color: var(--twin-muted) !important; }

/* ---------- Message rows: strip parent backgrounds ---------- */
.message-row,
.message-row > div,
.message-row .role,
.message-wrap, .bubble-wrap {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}

/* ---------- Reset borders on every bubble variant first ---------- */
.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  border: 0 !important;
  box-shadow: none !important;
  padding: 6px 10px !important;
}

/* ---------- Bubble backgrounds (broad to cover Gradio variants) ---------- */
.message-row.user-row .message,
.message-row.user-row .message-bubble,
.message-row.user-row .bubble,
.message-row[data-role="user"] .message,
.message-row[data-role="user"] .message-bubble {
  background: linear-gradient(135deg, var(--twin-blue) 0%, #4f83ea 100%) !important;
  color: #ffffff !important;
}

.message-row.bot-row .message,
.message-row.bot-row .message-bubble,
.message-row.bot-row .bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .message-bubble {
  background: var(--twin-surface-2) !important;
  color: var(--twin-text) !important;
  border-left: 2px solid var(--twin-blue) !important;
}

/* ---------- Purple stripe ----------
   Apply to every common bubble class for assistant rows (we don't know which
   one the running Gradio uses), then suppress on any *nested* instance so the
   stripe lands on the outermost matching element only — exactly one stripe. */
.message-row.bot-row .message,
.message-row.bot-row .bubble,
.message-row.bot-row .message-bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .bubble,
.message-row[data-role="assistant"] .message-bubble {
  border-left: 2px solid var(--twin-purple) !important;
}

.message-row.bot-row .message .message,
.message-row.bot-row .message .bubble,
.message-row.bot-row .message .message-bubble,
.message-row.bot-row .bubble .message,
.message-row.bot-row .bubble .bubble,
.message-row.bot-row .bubble .message-bubble,
.message-row.bot-row .message-bubble .message,
.message-row.bot-row .message-bubble .bubble,
.message-row.bot-row .message-bubble .message-bubble,
.message-row[data-role="assistant"] .message .message,
.message-row[data-role="assistant"] .message .bubble,
.message-row[data-role="assistant"] .message .message-bubble,
.message-row[data-role="assistant"] .bubble .message,
.message-row[data-role="assistant"] .bubble .bubble,
.message-row[data-role="assistant"] .bubble .message-bubble,
.message-row[data-role="assistant"] .message-bubble .message,
.message-row[data-role="assistant"] .message-bubble .bubble,
.message-row[data-role="assistant"] .message-bubble .message-bubble {
  border-left: 0 !important;
}

/* ---------- Uniform font size in bubbles ----------
   The "first paragraph different size" was caused by a leaky `.prose p:first-of-type`
   selector. Force every paragraph in a bubble to the same size. */
.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  font-size: 14px !important;
  line-height: 1.55 !important;
}
.message-row .message p,
.message-row .message-bubble p,
.message-row .bubble p,
.message-row .prose p {
  font-size: 14px !important;
  line-height: 1.55 !important;
  margin: 0 0 8px !important;
  color: inherit !important;
}
.message-row .message p:last-child,
.message-row .message-bubble p:last-child,
.message-row .bubble p:last-child,
.message-row .prose p:last-child { margin-bottom: 0 !important; }

/* Strip stray internal borders/backgrounds from anything inside a bubble */
.message-row .message *,
.message-row .message-bubble *,
.message-row .bubble * {
  background: transparent !important;
  border-color: transparent !important;
  box-shadow: none !important;
  color: inherit !important;
}
.message-row .message a,
.message-row .message-bubble a {
  color: var(--twin-blue) !important;
  text-decoration: underline;
}

/* ---------- Input row alignment ---------- */
.input-row,
.gr-input-row,
.chat-input-row,
form[class*="input"] {
  align-items: stretch !important;
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  padding: 0 !important;
}

.gradio-container .form,
.gradio-container .gr-form,
.gradio-container .block.form {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}

textarea, input[type="text"] {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  color: var(--twin-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 14px !important;
  padding: 12px 14px !important;
  line-height: 1.45 !important;
  min-height: 48px !important;
  box-shadow: inset 0 1px 2px rgba(23, 33, 43, 0.03) !important;
}
textarea:focus, input[type="text"]:focus {
  border-color: var(--twin-blue) !important;
  outline: none !important;
  box-shadow: 0 0 0 2px rgba(45, 108, 223, 0.14) !important;
}
textarea::placeholder, input::placeholder { color: var(--twin-muted) !important; }

/* ---------- Buttons ---------- */
button {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  letter-spacing: 0.04em !important;
  text-transform: uppercase !important;
  border: 1px solid var(--twin-border) !important;
  background: var(--twin-surface) !important;
  color: var(--twin-text) !important;
  padding: 0 16px !important;
  min-height: 46px !important;
  align-self: stretch !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer;
  transition: border-color 0.15s ease, color 0.15s ease, transform 0.15s ease;
}
button:hover {
  border-color: var(--twin-blue) !important;
  color: var(--twin-blue) !important;
  transform: translateY(-1px);
}

button.primary,
button[variant="primary"],
button.submit,
button.submit-button,
.submit-button,
button.lg.primary {
  background: var(--twin-blue) !important;
  border: 1px solid var(--twin-blue) !important;
  color: #ffffff !important;
  min-height: 46px !important;
  align-self: stretch !important;
  padding: 0 14px !important;
}
button.primary:hover,
button.submit:hover,
.submit-button:hover,
button.lg.primary:hover {
  background: #245fc0 !important;
  border-color: #245fc0 !important;
  color: #ffffff !important;
}

/* ---------- Submit-button icon: center vertically and size correctly ---------- */
button.submit svg,
button.submit-button svg,
.submit-button svg,
button.primary svg,
button[variant="primary"] svg {
  width: 18px !important;
  height: 18px !important;
  margin: 0 auto !important;
  display: block !important;
  align-self: center !important;
  color: #111111 !important;
  fill: currentColor !important;
  stroke: currentColor !important;
}

/* ---------- Examples ---------- */
.examples, .examples-holder, [data-testid="examples"] {
  background: transparent !important;
  padding: 0 !important;
  margin-top: 14px !important;
}
.examples table, .examples-table { background: transparent !important; border: 0 !important; }
.examples button, .example, .examples td button, [data-testid="examples"] button {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  color: var(--twin-text) !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 13px !important;
  font-weight: 400 !important;
  padding: 10px 14px !important;
  text-align: left !important;
  min-height: 0 !important;
  align-self: auto !important;
  display: inline-block !important;
}
.examples button:hover, .example:hover, [data-testid="examples"] button:hover {
  border-color: var(--twin-blue) !important;
  color: var(--twin-blue) !important;
  background: var(--twin-surface) !important;
}

/* ---------- Icon buttons (clear, retry, copy) ---------- */
.icon-button, .chatbot .icon-button {
  color: var(--twin-muted) !important;
  background: transparent !important;
  border: 0 !important;
  min-height: 0 !important;
  align-self: auto !important;
  padding: 4px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.icon-button:hover, .chatbot .icon-button:hover { color: var(--twin-blue) !important; }

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--twin-bg); }
::-webkit-scrollbar-thumb { background: var(--twin-border-strong); }
::-webkit-scrollbar-thumb:hover { background: var(--twin-blue); }

/* ---------- Selection ---------- */
::selection { background: var(--twin-blue); color: #ffffff; }

/* ---------- Mobile ---------- */
@media (max-width: 640px) {
  .gradio-container { padding: 20px 14px 32px !important; }
  .gradio-container h1 { font-size: 24px !important; }
}

/* ---------- Force light input toolbar ---------- */
.gradio-container .input-row,
.gradio-container .chat-input-row,
.gradio-container .gr-input-row,
.gradio-container form[class*="input"],
.gradio-container .chatbot .input-row,
.gradio-container .chatbot .chat-input-row,
.gradio-container .chatbot .footer,
.gradio-container .chatbot .chat-input,
.gradio-container .gradio-footer,
.gradio-container .input-area {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  padding: 0 !important;
}

.gradio-container .input-row > div,
.gradio-container .chat-input-row > div,
.gradio-container .input-area > div {
  background: transparent !important;
  border: 0 !important;
}

.gradio-container .submit-button,
.gradio-container button[variant="primary"] {
  box-shadow: none !important;
}

/* ---------- Explicit overrides for Gradio / Svelte wrappers ---------- */
/* Gradio sometimes emits generic .wrap/.styler/.gr-group elements with Svelte classes
   that carry dark backgrounds; force them to the light surface. */
/* Generic wrappers: use light surface but avoid adding extra borders here (we'll
   specifically remove nested borders around inputs below). */
.wrap,
.wrap.center,
.wrap.default,
.wrap.full,
.gr-group,
.styler,
.styler * {
  background: var(--twin-surface) !important;
  color: var(--twin-text) !important;
  border: 0 !important;
  box-shadow: none !important;
}

/* Status tracker / hidden wrappers that still carry a dark fill */
[data-testid="status-tracker"],
.wrap.hide {
  background: transparent !important;
}

/* Remove nested borders around the input area so only the textarea shows a single box. */
.gradio-container .styler .row,
.gradio-container .styler .row .form,
.gradio-container .styler .row .form .block,
.gradio-container .styler .row .form .block .container,
.gradio-container .styler .row .form .block .container .input-container,
.gradio-container .input-row .block,
.gradio-container .input-row .form {
  border: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
  padding: 0 !important;
  margin: 0 !important;
}

/* Box the input area so it doesn't stretch edge-to-edge */
.gradio-container .chat-input-row,
.gradio-container .input-row,
.gradio-container .gr-input-row,
.gradio-container .chatbot .chat-input-row {
  max-width: 860px !important;
  margin: 14px auto 0 !important;
  border-radius: 12px !important;
  padding: 8px !important;
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
}

.gradio-container textarea,
.gradio-container input[type="text"] {
  width: 100% !important;
  box-sizing: border-box !important;
}

/* If Gradio renders different wrapper classes, style the `.styler .row` that holds the input
   so a single boxed container appears around the textbox. */
.gradio-container .styler .row {
  max-width: 860px !important;
  margin: 14px auto 0 !important;
  padding: 8px !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 12px !important;
  background: var(--twin-surface) !important;
}

/* Ensure the visible textarea retains the single bordered input look */
.gradio-container textarea,
.gradio-container input[type="text"] {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  box-shadow: none !important;
}

/* High-specificity fallback for Gradio's textarea class to override any other rules */
.gradio-container textarea.svelte-1hguek3.no-label,
.gradio-container textarea.no-label,
.gradio-container textarea.svelte-1hguek3 {
  border: 1px solid var(--twin-border) !important;
  background: var(--twin-surface) !important;
}

/* Force Markdown/prose content (title/description) to our text color */
.gradio-container .prose,
.gradio-container .prose *,
.gradio-container .md,
.gradio-container .md * {
  color: var(--twin-text) !important;
  opacity: 1 !important;
}

/* Additional light-mode overrides to remove remaining dark areas */
/* Make sure header/description text is fully visible */
.gradio-container .lead,
.gradio-container .description,
.gradio-container .gr-text,
.gradio-container header p,
.gradio-container .header p,
.gradio-container > p {
  color: var(--twin-text) !important;
  opacity: 1 !important;
}

/* Replace dark input toolbar with a light surface and subtle border */
.gradio-container .chat-input-row,
.gradio-container .input-row,
.gradio-container .gr-input-row,
.gradio-container .chatbot .input-row,
.gradio-container .chatbot .chat-input-row,
.gradio-container .gradio-footer,
.gradio-container .chatbot .footer,
.gradio-container .footer,
.gradio-container .block.footer {
  background: var(--twin-surface) !important;
  background-color: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  box-shadow: none !important;
  padding: 10px 12px !important;
}

/* Ensure inner wrapper is transparent so textbox styling shows through */
.gradio-container .chat-input-row > div,
.gradio-container .input-row > div,
.gradio-container .input-area > div {
  background: transparent !important;
  border: 0 !important;
}

/* Keep submit button accent blue */
.gradio-container .submit-button, .gradio-container button[variant="primary"] {
  background: var(--twin-blue) !important;
  border-color: var(--twin-blue) !important;
  color: #ffffff !important;
}

/* Force a black border around the message input */
.gradio-container textarea,
.gradio-container textarea.svelte-1hguek3.no-label,
.gradio-container textarea.no-label {
  border: 2px solid #000000 !important;
}

/* Ensure the send/submit icon button is filled with the blue accent */
.gradio-container .submit-button,
.gradio-container button[data-testid="submit-button"],
.gradio-container button[aria-label="send"],
.gradio-container .submit {
  background: var(--twin-blue) !important;
  border: 1px solid var(--twin-blue) !important;
  color: #ffffff !important;
  padding: 8px !important;
}
.gradio-container .submit-button svg,
.gradio-container button[data-testid="submit-button"] svg,
.gradio-container button[aria-label="send"] svg {
  fill: #ffffff !important;
  color: #ffffff !important;
}

"""

JS = """
() => {
  document.title = 'Digital Twin';

  const focusInput = () => {
    const areas = document.querySelectorAll('textarea');
    if (areas.length) areas[areas.length - 1].focus();
  };
  setTimeout(focusInput, 300);

  const enforceStyle = (area) => {
    try {
      const root = getComputedStyle(document.documentElement);
      const twinBorder = root.getPropertyValue('--twin-border') || '#e2e8f0';
      const twinSurface = root.getPropertyValue('--twin-surface') || '#ffffff';
      area.style.border = `1px solid ${twinBorder.trim()}`;
      area.style.background = twinSurface.trim();
      area.style.boxShadow = 'none';
      // Find the nearest row/styler ancestor and give it a single box so the
      // input appears inside one container (override any competing CSS).
      let el = area.parentElement;
      while (el && el !== document.body) {
        const cls = el.className || '';
        if (cls.includes('row') || cls.includes('styler') || cls.includes('input-row') || cls.includes('container')) {
          el.style.maxWidth = '860px';
          el.style.margin = '14px auto 0';
          el.style.padding = '8px';
          el.style.border = `1px solid ${twinBorder.trim()}`;
          el.style.borderRadius = '12px';
          el.style.background = twinSurface.trim();
          break;
        }
        el = el.parentElement;
      }
    } catch (e) {}
  };

  // Re-focus the message field whenever Gradio re-enables it and enforce style.
  const watchTextarea = (area) => {
    if (area.dataset.twinWatched) return;
    area.dataset.twinWatched = '1';
    enforceStyle(area);
    let wasDisabled = area.disabled || area.readOnly;
    new MutationObserver(() => {
      const isDisabled = area.disabled || area.readOnly;
      if (wasDisabled && !isDisabled) area.focus();
      wasDisabled = isDisabled;
      enforceStyle(area);
    }).observe(area, { attributes: true, attributeFilter: ['disabled', 'readonly'] });
  };

  const scan = () => document.querySelectorAll('textarea').forEach(watchTextarea);
  setTimeout(scan, 500);
  new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
}
"""

