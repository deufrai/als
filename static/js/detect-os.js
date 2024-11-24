document.addEventListener("DOMContentLoaded", function() {
    var downloadButton = document.getElementById("downloadButton");
    var userOS = detectOS();
    var downloadLink;

    if (userOS === "Linux-AMD64") {
        downloadLink = "/downloads/als.run";
    } else if (userOS === "Linux-ARM64") {
        downloadLink = "/downloads/als.tgz";
    } else if (userOS === "Mac-Intel") {
        downloadLink = "/downloads/als-amd64.dmg";
    } else if (userOS === "Mac-AppleSilicon") {
        downloadLink = "/downloads/als-arm64.dmg";
    } else if (userOS === "Windows") {
        downloadLink = "/downloads/als.exe";
    } else {
        downloadLink = "/downloads/ALS.zip"; // Fallback option
    }

    downloadButton.onclick = function() {
        window.location.href = downloadLink;
    };
});

function detectOS() {
    var platform = window.navigator.platform,
        macosIntelPlatforms = ['Macintosh', 'MacIntel'],
        macosArmPlatforms = ['MacPPC', 'Mac68K'],
        windowsPlatforms = ['Win32', 'Win64', 'Windows', 'WinCE'],
        linuxAMD64Platforms = ['Linux x86_64'],
        linuxARM64Platforms = ['Linux aarch64'],
        os = null;

    if (macosIntelPlatforms.indexOf(platform) !== -1) {
        os = 'Mac-Intel';
    } else if (macosArmPlatforms.indexOf(platform) !== -1) {
        os = 'Mac-AppleSilicon';
    } else if (windowsPlatforms.indexOf(platform) !== -1) {
        os = 'Windows';
    } else if (linuxAMD64Platforms.indexOf(platform) !== -1) {
        os = 'Linux-AMD64';
    } else if (linuxARM64Platforms.indexOf(platform) !== -1) {
        os = 'Linux-ARM64';
    } else if (!os && /Linux/.test(platform)) {
        os = 'Linux-AMD64'; // Default to Linux AMD64
    }

    return os;
}
