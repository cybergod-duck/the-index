document
  .querySelector('#shortcuts')
  .addEventListener('click', () =>
    chrome.tabs.create({ url: 'chrome://extensions/configureCommands' })
  );

let allowedKeys = [
  'F2',
  'F4',
  'F8',
  'F9',
  'A',
  'B',
  'C',
  'D',
  'E',
  'F',
  'G',
  'H',
  'I',
  'J',
  'K',
  'L',
  'M',
  'N',
  'Ñ',
  'O',
  'P',
  'Q',
  'R',
  'S',
  'T',
  'U',
  'V',
  'W',
  'X',
  'Y',
  'Z',
  '0',
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '8',
  '9',
  '`',
  ',',
  '.',
  '/',
  '-',
  '=',
  '[',
  ']',
  ';',
  `'`,
  '*',
  '!',
  '@',
  '#',
  '$',
  '%',
  '^',
  '&',
  '(',
  ')',
  '_',
  '+',
  '{',
  '}',
  ':',
  '"',
  '<',
  '>',
  '~',
  '|',
];

chrome.storage.sync.get(null, results => {
  document.querySelectorAll('.key-input').forEach((input, i) => {
    let inputText = input.parentElement.firstElementChild.innerText;
    input.readOnly = true;
    input.value = results[inputText];
    if (!results[inputText]) input.value = '';
    input.addEventListener('focus', () => {
      input.style.border = '1px solid #ffffffa3';
    });
    input.addEventListener('focusout', () => {
      input.style.border = '1px solid #ffffff1f';
    });
    input.addEventListener('keydown', k => {
      k.preventDefault();
      if (allowedKeys.includes(k.key.toUpperCase())) {
        input.value = k.key.toUpperCase();
        input.style.border = '1px solid #ffffffa3';
        chrome.storage.sync.set({ [inputText]: k.key.toUpperCase() });
      } else if (
        k.key == 'Escape' ||
        k.key == 'Delete' ||
        k.key == 'Backspace'
      ) {
        input.value = '';
        input.style.border = '1px solid #ffffffa3';
        chrome.storage.sync.set({ [inputText]: '' });
      } else {
        input.value = '';
        input.style.border = '1px solid #ff0000a6';
        chrome.storage.sync.set({ [inputText]: '' });
      }
    });
  });
});
