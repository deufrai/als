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
    var platform = window.navigator.platform;
    var userAgent = navigator.userAgent.toLowerCase();
    var os = null;

    if (platform.includes('MacIntel') && !userAgent.includes('arm64')) {
        os = 'Mac-Intel';
    } else if (platform.includes('Mac') && userAgent.includes('arm64')) {
        os = 'Mac-AppleSilicon';
    } else if (platform.includes('Win')) {
        os = 'Windows';
    } else if (platform.includes('Linux') && userAgent.includes('x86_64')) {
        os = 'Linux-AMD64';
    } else if (platform.includes('Linux') && userAgent.includes('aarch64')) {
        os = 'Linux-ARM64';
    } else if (!os && /Linux/.test(platform)) {
        os = 'Linux-AMD64'; // Default to Linux AMD64
    }

    return os;
}
