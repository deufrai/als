(function () {
    'use strict';
    console.log('Language detection script executed');
    var userLang = navigator.language || navigator.userLanguage;
    console.log('Detected language:', userLang);
    userLang = userLang.substring(0, 2); // Get the first two characters (e.g., 'en', 'fr')
    var supportedLangs = ['en', 'fr'];
    if (supportedLangs.indexOf(userLang) === -1) {
        userLang = 'en'; // Default to English if the user's language is not supported
    }
    console.log('Using language:', userLang);
    // Check if the current URL already contains a language prefix
    if (!window.location.pathname.startsWith('/' + userLang + '/') && !sessionStorage.getItem('redirected')) {
        sessionStorage.setItem('redirected', 'true');
        console.log('Redirecting to:', '/' + userLang + window.location.pathname);
        window.location.href = '/' + userLang + window.location.pathname;
    }
})();