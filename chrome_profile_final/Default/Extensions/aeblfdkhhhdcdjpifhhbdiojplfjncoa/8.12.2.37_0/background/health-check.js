"use strict";
!function(){try{var e="undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:{},n=(new Error).stack;n&&(e._sentryDebugIds=e._sentryDebugIds||{},e._sentryDebugIds[n]="bd034bbc-5a47-547f-a442-c94d3798a6c7")}catch(e){}}();

(() => {
chrome.runtime.onMessage.addListener((a,e,r)=>{a.name==="health-check-request"&&(console.info("[Background]","HealthCheck: received request from tab "+e.tab?.id)||logger.report(["HealthCheck: received request from tab "+e.tab?.id],{severity:"info",fileName:"js/b5x/background/src/background/health-check.ts",lineNumber:18,prefix:"[Background]",highlight:!1}),r({name:"health-check-response",data:"alive"}))});
})();

//# debugId=bd034bbc-5a47-547f-a442-c94d3798a6c7
