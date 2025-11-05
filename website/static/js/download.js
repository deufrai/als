function downloadAndOpenInstructions(platform) {
    var urls = {
        'windows': {
            'download': 'https://github.com/deufrai/als/releases/download/v1.0/als-v1.0_Setup.exe',
            'instructions': window.location.pathname.includes('/fr/') ? '/fr/docs/v1.0/installation/windows-install/' : '/docs/v1.0/installation/windows-install/'
        },
        'mac-intel': {
            'download': 'https://github.com/deufrai/als/releases/download/v1.0/ALS-v1.0-amd64.dmg',
            'instructions': window.location.pathname.includes('/fr/') ? '/fr/docs/v1.0/installation/mac-intel-install/' : '/docs/v1.0/installation/mac-intel-install/'
        },
        'mac-arm': {
            'download': 'https://github.com/deufrai/als/releases/download/v1.0/ALS-v1.0-arm64.dmg',
            'instructions': window.location.pathname.includes('/fr/') ? '/fr/docs/v1.0/installation/mac-arm-install/' : '/docs/v1.0/installation/mac-arm-install/'
        },
        'linux': {
            'download': 'https://github.com/deufrai/als/releases/download/v1.0/als-v1.0.run',
            'instructions': window.location.pathname.includes('/fr/') ? '/fr/docs/v1.0/installation/linux-install/' : '/docs/v1.0/installation/linux-install/'
        },
        'raspberry-pi': {
            'download': 'https://github.com/deufrai/als/releases/download/v1.0/als-v1.0.tgz',
            'instructions': window.location.pathname.includes('/fr/') ? '/fr/docs/v1.0/installation/raspberry-pi-install/' : '/docs/v1.0/installation/raspberry-pi-install/'
        }
    };

    var platformInfo = urls[platform];

    // Track the download in Matomo
    if (typeof _paq !== 'undefined') {
        _paq.push(['trackLink', platformInfo.download, 'download']);
    }

    // Open instructions in a new tab
    window.open(platformInfo.instructions, '_blank');

    // Start the download
    window.location.href = platformInfo.download;
}

