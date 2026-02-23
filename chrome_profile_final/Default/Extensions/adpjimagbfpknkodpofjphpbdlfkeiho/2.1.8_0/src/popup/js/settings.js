chrome.storage.sync.get(null, settings => {
  const persistenceMode = document.querySelector('#persistenceMode');
  persistenceMode.innerText = settings.persistenceMode;
  persistenceMode.addEventListener('click', () => {
    if (persistenceMode.innerText == 'Off') {
      chrome.storage.sync.set({ persistenceMode: 'Session' });
      persistenceMode.innerText = 'Session';
    } else {
      chrome.storage.sync.set({ persistenceMode: 'Off' });
      persistenceMode.innerText = 'Off';
    }
  });

  const playerButtonAR = document.querySelector('#playerButtonAR');
  playerButtonAR.innerText = settings.playerButtonAR;
  const AR = ['Off', '16:9', '18:9', '21:9', '32:9'];
  let i1 = AR.indexOf(playerButtonAR.innerText);
  playerButtonAR.addEventListener('click', () => {
    if (i1 == 4) i1 = -1;
    chrome.storage.sync.set({ playerButtonAR: AR[i1 + 1] });
    playerButtonAR.innerText = AR[i1 + 1];
    i1++;
  });

  const transitionSpeed = document.querySelector('#transitionSpeed');
  transitionSpeed.innerText = settings.transitionSpeed;
  let speed = ['0ms', '150ms', '300ms', '600ms', '1000ms'];
  let i2 = speed.indexOf(transitionSpeed.innerText);
  transitionSpeed.addEventListener('click', () => {
    if (i2 == 4) i2 = -1;
    chrome.storage.sync.set({ transitionSpeed: speed[i2 + 1] });
    transitionSpeed.innerText = speed[i2 + 1];
    i2++;
  });
});
