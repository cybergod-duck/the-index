document.querySelectorAll('#zoom').forEach(button => {
  button.addEventListener('click', () => zoomMessage(button.innerText));
});

document.querySelector('#increase').addEventListener('mousedown', () => {
  zoomActionMessage('+');
});
document.querySelector('#decrease').addEventListener('mousedown', () => {
  zoomActionMessage('-');
});
document.querySelector('#increase').addEventListener('mouseleave', stop);
document.querySelector('#decrease').addEventListener('mouseleave', stop);
document.querySelector('#increase').addEventListener('mouseup', stop);
document.querySelector('#decrease').addEventListener('mouseup', stop);

document.querySelector('.button-wrap').addEventListener('wheel', event => {
  event.preventDefault();
  if (event.deltaY < 0) zoomMessage('+');
  if (event.deltaY > 0) zoomMessage('-');
});

document.querySelector('#monAR').innerText = aspectRatio(
  screen.width,
  screen.height
);

zoomMessage('info');

function zoomMessage(scale) {
  chrome.tabs.query({ currentWindow: true, active: true }, tabs => {
    chrome.tabs.sendMessage(tabs[0].id, { message: scale }, res => {
      if (!chrome.runtime.lastError && res !== undefined)
        handleResponse(res.message);
    });
  });
}

let intervalId;
function zoomActionMessage(action) {
  intervalId = setInterval(() => {
    chrome.tabs.query({ currentWindow: true, active: true }, tabs => {
      chrome.tabs.sendMessage(tabs[0].id, { message: action }, res => {
        if (!chrome.runtime.lastError) handleResponse(res.message);
      });
    });
  }, 50);
}

function handleResponse(res) {
  let num = (Math.round(res[0] * 100) / 100).toFixed(2);
  document.querySelector('#scale').innerText = 'x' + num;
  if (res[1] !== 0 && res[2] !== 0) {
    document.querySelector('#vidAR').innerText = aspectRatio(res[1], res[2]);
  }
}

function stop() {
  clearInterval(intervalId);
}

// Aspect ratio
function aspectRatio(width, height) {
  let AR = reduce(width, height);
  switch (AR) {
    case '64:27':
    case '43:18':
    case '12:5':
    case '7:3':
      return '21:9';
    case '2:1':
      return '18:9';
    case '18:5':
    case '16:5':
      return '32:9';
    case '16:9':
      return '16:9';
    case '16:10':
      return '16:10';
    case '41:30':
    case '4:3':
      return '4:3';
    default:
      return width + 'x' + height;
  }
}

function reduce(numerator, denominator) {
  var gcd = function gcd(a, b) {
    return b ? gcd(b, a % b) : a;
  };
  gcd = gcd(numerator, denominator);
  var result = [numerator / gcd, denominator / gcd];
  return result[0].toString() + ':' + result[1].toString();
}
