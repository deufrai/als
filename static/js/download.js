function downloadAndOpenInstructions(platform) {
    var urls = {
        'windows': {
            'download': 'https://github.com/deufrai/als/releases/download/v0.7-beta6/als-v0.7-beta6.exe',
            'instructions': window.location.pathname.includes('/en/') ? '/en/docs/v0.7/installation/windows-install/' : '/docs/v0.7/installation/windows-install/'
        },
        'mac-intel': {
            'download': 'https://github.com/deufrai/als/releases/download/v0.7-beta6/ALS-v0.7-beta6-amd64.dmg',
            'instructions': window.location.pathname.includes('/en/') ? '/en/docs/v0.7/installation/mac-intel-install/' : '/docs/v0.7/installation/mac-intel-install/'
        },
        'mac-arm': {
            'download': 'https://github.com/deufrai/als/releases/download/v0.7-beta6/ALS-v0.7-beta6-arm64.dmg',
            'instructions': window.location.pathname.includes('/en/') ? '/en/docs/v0.7/installation/mac-arm-install/' : '/docs/v0.7/installation/mac-arm-install/'
        },
        'linux': {
            'download': 'https://github.com/deufrai/als/releases/download/v0.7-beta6/als-v0.7-beta6.run',
            'instructions': window.location.pathname.includes('/en/') ? '/en/docs/v0.7/installation/linux-install/' : '/docs/v0.7/installation/linux-install/'
        },
        'raspberry-pi': {
            'download': 'https://github.com/deufrai/als/releases/download/v0.7-beta6/als-v0.7-beta6.tgz',
            'instructions': window.location.pathname.includes('/en/') ? '/en/docs/v0.7/installation/raspberry-pi-install/' : '/docs/v0.7/installation/raspberry-pi-install/'
        }
    };

    var platformInfo = urls[platform];

    // Open instructions in a new tab
    window.open(platformInfo.instructions, '_blank');

    // Start the download
    window.location.href = platformInfo.download;
}
