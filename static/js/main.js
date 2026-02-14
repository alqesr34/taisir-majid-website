document.getElementById('contactForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const form = e.target;
  const data = new FormData(form);
  const resp = await fetch('/contact', { method: 'POST', body: data });
  const json = await resp.json();
  const result = document.getElementById('contactResult');
  if (json.status === 'success') {
    result.innerText = json.message;
    form.reset();
  } else {
    result.innerText = 'حدث خطأ. حاول لاحقاً.';
  }
});
