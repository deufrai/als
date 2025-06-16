(function() {
  'use strict';
  document.addEventListener("DOMContentLoaded", function() {
    console.log('Cookies library check initiated');

    if (typeof window.Cookies !== 'undefined') {
      const cookieconsent = document.querySelector('.cookieconsent');
      console.log('Cookie consent element:', cookieconsent ? 'found' : 'not found');

      if (!cookieconsent) {
        console.log('Cookie consent element not found');
        return;
      }

      // Check if consent is already given
      const consent = window.Cookies.get('cookieconsent');
      console.log('Cookie consent status:', consent);

      if (consent === undefined) {
        cookieconsent.classList.add('js-cookieconsent-open');
        cookieconsent.removeAttribute('js-cookieconsent-hidden');
        console.log('Cookie consent popup displayed');
      } else {
        console.log('Consent already given, no popup');
        if (cookieconsent) {
          cookieconsent.setAttribute('js-cookieconsent-hidden', true); // Hide if consent already given
        }
      }

      const cookie_buttons = Array.prototype.slice.call(document.querySelectorAll('button[data-consent]'));
      console.log('Found cookie buttons:', cookie_buttons.length);
      const sitedomain = window.location.hostname.split('.').slice(-2).join('.');
      const cookiedomain = sitedomain;
      let cookie_options = {
        domain: cookiedomain,
        path: '/', // Ensure it applies site-wide
        sameSite: 'strict',
        expires: 365
      };

      // Set the cookie based on user consent
      cookie_buttons.forEach(button => {
        button.addEventListener('click', function() {
          window.Cookies.set('cookieconsent', this.dataset.consent, cookie_options);
          console.log('Cookie consent given:', this.dataset.consent);
          // Hide consent banner after selection
          cookieconsent.classList.remove('js-cookieconsent-open');
          setTimeout(function() {
            if (cookieconsent) {
              cookieconsent.setAttribute('js-cookieconsent-hidden', true);
            }
          }, 200); // Adjust timeout as needed
        });
      });
    } else {
      console.error('Cookies library is not loaded.');
    }
  });
})();
