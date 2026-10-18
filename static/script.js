(() => {
  'use strict';

  const CONFIG = {
    minAge: 15,
    maxAge: 60,
    maxAddressLength: 300,
  };

  const FACULTY_DEPARTMENTS = {
    'Natural and Applied Science': ['Microbiology'],
    'Computing': ['Software Engineering', 'Computer Science'],
    'Engineering': ['Computer Engineering'],
    'Social Sciences': ['Education Management', 'Mass Communication'],
    'Law': ['Law'],
    'Management Science': ['Accounting'],
    'Medicine': ['Nursing'],
  };

  const NAME_RE   = /^[A-Za-z\u00C0-\u024F][A-Za-z\u00C0-\u024F '\-]*$/;
  const EMAIL_RE  = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  const MATRIC_RE = /^VUG\/[A-Z]{2,4}\/\d{2}\/\d{4,6}$/;

  const required = (v, label) => (v ? '' : `${label} is required.`);

  const validators = {
    first(v) {
      return required(v, 'First name')
        || (v.length < 2 ? 'First name is too short.' : '')
        || (v.length > 50 ? 'First name is too long.' : '')
        || (!NAME_RE.test(v) ? 'Use letters, spaces, hyphens or apostrophes only.' : '');
    },

    last(v) {
      return required(v, 'Last name')
        || (v.length < 2 ? 'Last name is too short.' : '')
        || (v.length > 50 ? 'Last name is too long.' : '')
        || (!NAME_RE.test(v) ? 'Use letters, spaces, hyphens or apostrophes only.' : '');
    },

    dob(v) {
      if (!v) return 'Date of birth is required.';
      const dob = new Date(`${v}T00:00:00`);
      if (Number.isNaN(dob.getTime())) return 'Enter a valid date.';
      const today = new Date();
      if (dob > today) return 'Date of birth cannot be in the future.';
      let age = today.getFullYear() - dob.getFullYear();
      const hadBirthday =
        today.getMonth() > dob.getMonth() ||
        (today.getMonth() === dob.getMonth() && today.getDate() >= dob.getDate());
      if (!hadBirthday) age -= 1;
      if (age < CONFIG.minAge) return `You must be at least ${CONFIG.minAge} years old.`;
      if (age > CONFIG.maxAge) return 'Please check the date of birth.';
      return '';
    },

    gender(v) {
      return v ? '' : 'Please select a gender.';
    },

    email(v) {
      return required(v, 'Email')
        || (v.length > 254 ? 'Email is too long.' : '')
        || (!EMAIL_RE.test(v) ? 'Enter a valid email address.' : '');
    },

    phone(v) {
      if (!v) return 'Phone number is required.';
      if (!/^[+\d][\d\s\-()]*$/.test(v)) return 'Use digits only (a leading + is allowed).';
      const digits = v.replace(/\D/g, '');
      if (digits.length < 10 || digits.length > 15) return 'Enter a valid phone number (10 to 15 digits).';
      return '';
    },

    address(v) {
      return (v?.length ?? 0) > CONFIG.maxAddressLength
        ? `Address must be ${CONFIG.maxAddressLength} characters or fewer.`
        : '';
    },

    matric(v) {
      if (!v) return 'Matric number is required.';
      if (!MATRIC_RE.test(v))
        return 'Enter a valid matric number (e.g. VUG/SEN/24/12276).';
      return '';
    },

    level(v)   { return required(v, 'Level'); },
    faculty(v) { return required(v, 'Faculty'); },
    dept(v)    { return required(v, 'Department'); },
  };

  const form = document.getElementById('bio');
  if (!form) return;

  form.setAttribute('novalidate', '');

  const touched = new Set();

  const status = document.createElement('div');
  status.className = 'form-status';
  status.setAttribute('role', 'status');
  status.setAttribute('aria-live', 'polite');
  status.hidden = true;
  form.querySelector('.actions').before(status);

  function showStatus(message, type) {
    status.textContent = message;
    status.dataset.type = type;
    status.hidden = !message;
  }

  function getValue(name) {
    const fields = form.elements[name];
    if (!fields) return '';
    if (fields instanceof RadioNodeList) return fields.value;
    return fields.value.trim();
  }

  function getControls(name) {
    const field = form.elements[name];
    if (!field) return [];
    return field instanceof RadioNodeList ? Array.from(field) : [field];
  }

  function getAnchorEl(name) {
    const controls = getControls(name);
    if (!controls.length) return null;
    const first = controls[0];
    if (first.type === 'radio')    return first.closest('.radios') ?? first;
    if (first.tagName === 'SELECT' || first.tagName === 'TEXTAREA') {
      return first.closest('div') ?? first;
    }
    return first;
  }

  function getErrorEl(name) {
    const id = `${name}-error`;
    let el = document.getElementById(id);
    if (el) return el;

    el = document.createElement('p');
    el.id        = id;
    el.className = 'error-message';
    const anchor = getAnchorEl(name);
    if (anchor) anchor.after(el);
    return el;
  }

  function setError(name, message) {
    const el = getErrorEl(name);
    el.textContent = message;
    getControls(name).forEach((c) => {
      c.classList.toggle('invalid', Boolean(message));
      if (message) {
        c.setAttribute('aria-invalid', 'true');
        c.setAttribute('aria-describedby', el.id);
      } else {
        c.removeAttribute('aria-invalid');
        c.removeAttribute('aria-describedby');
      }
    });
  }

  function validateField(name) {
    const message = validators[name] ? validators[name](getValue(name)) : '';
    setError(name, message);
    return !message;
  }

  function validateAll() {
    let firstInvalid = null;
    Object.keys(validators).forEach((name) => {
      touched.add(name);
      if (!validateField(name) && !firstInvalid) firstInvalid = name;
    });
    return firstInvalid;
  }

  function focusField(name) {
    const controls = getControls(name);
    if (controls.length) controls[0].focus({ preventScroll: false });
  }

  const dobInput = form.elements.dob;
  const toISO = (d) => {
    const pad = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  };
  dobInput.max = toISO(new Date());

  form.elements.matric.addEventListener('input', (e) => {
    const start = e.target.selectionStart;
    const end   = e.target.selectionEnd;
    e.target.value = e.target.value.toUpperCase();
    try {
      if (start !== null && end !== null) {
        e.target.setSelectionRange(start, end);
      }
    } catch (_) { /* non-text input types throw — ignore */ }
  });

  form.elements.phone.addEventListener('input', (e) => {
    e.target.value = e.target.value.replace(/[^\d+\s\-()]/g, '');
  });

  const address = form.elements.address;
  address.maxLength = CONFIG.maxAddressLength + 50;

  const faculty = form.elements.faculty;
  const dept    = form.elements.dept;

  const allDeptOptions = Array.from(dept.options).map((o) => ({
    value:       o.value,
    label:       o.textContent.trim(),
    placeholder: o.getAttribute('value') === '',
  }));

  function renderDepartments() {
    const allowed  = FACULTY_DEPARTMENTS[faculty.value];
    const previous = dept.value;
    dept.innerHTML = '';

    allDeptOptions.forEach(({ value, label, placeholder }) => {
      if (!placeholder && allowed && !allowed.includes(label)) return;
      dept.add(new Option(label, value));
    });

    dept.value = Array.from(dept.options).some((o) => o.value === previous) ? previous : '';
    if (touched.has('dept')) validateField('dept');
  }

  faculty.addEventListener('change', renderDepartments);
  renderDepartments();

  Object.keys(validators).forEach((name) => {
    getControls(name).forEach((control) => {
      control.addEventListener('blur', () => {
        touched.add(name);
        validateField(name);
      });
      const live = () => { if (touched.has(name)) validateField(name); };
      control.addEventListener('input', live);
      control.addEventListener('change', () => {
        touched.add(name);
        validateField(name);
      });
    });
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    showStatus('', '');

    const firstInvalid = validateAll();
    if (firstInvalid) {
      showStatus('Please fix the highlighted fields and try again.', 'error');
      focusField(firstInvalid);
      return;
    }

    showStatus('Form validated successfully.', 'success');
  });

  form.addEventListener('reset', () => {
    touched.clear();
    showStatus('', '');
    Object.keys(validators).forEach((name) => setError(name, ''));
    setTimeout(renderDepartments, 0);
  });
})();