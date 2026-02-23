
!function(){try{var e="undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:{},n=(new Error).stack;n&&(e._sentryDebugIds=e._sentryDebugIds||{},e._sentryDebugIds[n]="729dc97f-112d-5f7b-b508-6492b0f692de")}catch(e){}}();
import{E as n}from"/chunks/chunk-N5WBF2BO.js";var f=e=>!i(e),i=e=>new Date(e.startTime).getTime()+e.duration-Date.now()>0;function c(e){let t=e.trim();try{return new URL(t)}catch{try{return new URL(`https://${t}`)}catch{}}}function w(e,t,o){return e.urls.some(r=>r.mode===n.Host?c(r.url)?.host===t:r.mode===n.Never?!1:e.urlToNakedDomains[r.url]===o)}export{f as a,i as b,w as c};

//# debugId=729dc97f-112d-5f7b-b508-6492b0f692de
