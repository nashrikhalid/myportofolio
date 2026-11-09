async function skillRequest(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: { Accept: 'application/json', ...options.headers },
    });
    if (response.status === 204) return null;
    if (!response.ok) {
        const errors = await response.json().catch(() => ({}));
        throw new Error(Object.values(errors).flat().join(' ') || `HTTP ${response.status}`);
    }
    return response.json();
}

function renderSkill(skill, template) {
    const card = template.content.firstElementChild.cloneNode(true);
    const placeholder = '00000000-0000-0000-0000-000000000000';
    for (const element of card.querySelectorAll('*')) {
        for (const attr of element.attributes) {
            if (attr.value.includes(placeholder)) {
                attr.value = attr.value.replaceAll(placeholder, skill.id);
            }
        }
    }
    const icon = card.querySelector('.skill');
    icon.title = skill.name;
    icon.setAttribute('aria-label', skill.name);
    icon.querySelector('span').className = skill.logo;
    const edit = card.querySelector('a');
    if (edit) edit.setAttribute('aria-label', `Edit ${skill.name}`);
    const remove = card.querySelector('.skill-delete-button');
    if (remove) {
        remove.setAttribute('aria-label', `Hapus ${skill.name}`);
        card.querySelector('strong').textContent = skill.name;
    }
    return card;
}

function initSkillList(section) {
    const search = section.querySelector('[data-skill-search]');
    const input = search.elements.name;
    const grid = section.querySelector('.skills-wrapper');
    const template = section.querySelector('template');
    let controller;
    let timer;
    async function refresh() {
        controller?.abort();
        controller = new AbortController();
        const url = new URL(section.dataset.api, location.origin);
        if (input.value.trim()) url.searchParams.set('name', input.value.trim());
        try {
            const skills = await skillRequest(url, { signal: controller.signal });
            grid.replaceChildren(...skills.map(skill => renderSkill(skill, template)));
            if (!skills.length) grid.textContent = 'Tidak ada skill yang ditemukan.';
        } catch (error) {
            if (error.name !== 'AbortError') showToast('Gagal memuat skill', error.message, 'error');
        }
    }
    search.addEventListener('submit', event => {
        event.preventDefault();
        clearTimeout(timer);
        refresh();
    });
    input.addEventListener('input', () => {
        clearTimeout(timer);
        timer = setTimeout(refresh, 300);
    });
    grid.addEventListener('submit', async event => {
        const form = event.target;
        if (!form.dataset.deleteUrl) return;
        event.preventDefault();
        const button = form.querySelector('[type=submit]');
        if (button.disabled) return;
        button.disabled = true;
        try {
            await skillRequest(form.dataset.deleteUrl, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': form.elements.csrfmiddlewaretoken.value },
            });
            form.closest('.skill-item').remove();
            showToast('Berhasil', 'Skill berhasil dihapus.', 'success');
            await refresh();
        } catch (error) {
            showToast('Gagal menghapus skill', error.message, 'error');
        } finally {
            button.disabled = false;
        }
    });
    refresh();
}

function initSkillForm(form) {
    form.addEventListener('submit', async event => {
        event.preventDefault();
        const button = form.querySelector('[type=submit]');
        if (button.disabled) return;
        button.disabled = true;
        try {
            const fields = new FormData(form);
            await skillRequest(form.dataset.api, {
                method: form.dataset.method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': fields.get('csrfmiddlewaretoken'),
                },
                body: JSON.stringify({ name: fields.get('name'), logo: fields.get('logo') }),
            });
            location.assign(form.dataset.successUrl);
        } catch (error) {
            showToast('Gagal menyimpan skill', error.message, 'error');
            button.disabled = false;
        }
    });
}

const skillSection = document.querySelector('#skills[data-api]');
if (skillSection) initSkillList(skillSection);
const skillForm = document.querySelector('#skill-form');
if (skillForm) initSkillForm(skillForm);
