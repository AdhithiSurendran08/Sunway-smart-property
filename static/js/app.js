document.addEventListener('DOMContentLoaded', function () {

  // ---- gentle lift on property cards ----
  document.querySelectorAll('.property-card').forEach(function (card) {
    card.addEventListener('mouseenter', function () {
      card.style.transition = '0.15s';
      card.style.transform = 'translateY(-3px)';
    });
    card.addEventListener('mouseleave', function () {
      card.style.transform = 'translateY(0)';
    });
  });

});

// ---- Property Assistant ----

function appendMessage(html, fromUser) {
  const chat = document.getElementById('chat');
  if (!chat) return;
  const div = document.createElement('div');
  div.className = 'property-card' + (fromUser ? ' from-user' : '');
  div.innerHTML = html;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function renderAssistantReply(data, rawMessage) {
  const u = data.understood || {};
  const bits = [];
  if (u.budget) bits.push('budget around RM' + Math.round(u.budget).toLocaleString());
  if (u.wanted_type) bits.push(u.wanted_type.toLowerCase());
  if (u.wants_transport) bits.push('near public transport');
  if (u.wants_green) bits.push('with sustainability features');

  let intro = bits.length
    ? 'Looking for something ' + bits.join(', ') + ' — here\'s what matches:'
    : "Here's what I found — try adding a budget or a priority like \"near LRT\" for a sharper match:";

  if (!data.results || data.results.length === 0) {
    appendMessage('🤖 ' + intro + '<br><br>I couldn\'t find a close match yet. Try a higher budget, or fewer filters.');
    return;
  }

  let list = data.results.map(function (r) {
    const price = r.price ? 'RM ' + Math.round(r.price).toLocaleString() : 'Price on request';
    return '<div class="info" style="margin-top:10px">' +
      '<strong>' + r.name + '</strong> — ' + r.location + ' · ' + r.property_type +
      '<div class="meta">' + price + ' · Match ' + r.score + '%</div>' +
      '<a href="' + r.url + '" class="button ghost" style="margin-top:8px;padding:8px 16px;font-size:13px">View property →</a>' +
      '</div>';
  }).join('');

  appendMessage('🤖 ' + intro + list);
}

function askChip(text) {
  document.getElementById('message').value = text;
  sendMessage();
}

function sendMessage() {
  const input = document.getElementById('message');
  if (!input) return;
  const message = input.value.trim();
  if (!message) return;

  appendMessage(message, true);
  input.value = '';

  fetch('/api/assistant-query/?q=' + encodeURIComponent(message))
    .then(function (res) { return res.json(); })
    .then(function (data) { renderAssistantReply(data, message); })
    .catch(function () {
      appendMessage("🤖 Sorry, I couldn't reach the property database just now. Please try again.");
    });
}
