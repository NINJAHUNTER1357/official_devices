# 12-Mar-2026
- Lowered default screen density
- Switch to QTI Vibrator service
- Switch to AOSP NXP authsecret service
- Switch to AOSP NXP keymint service
- Switch to libperfmgr
- Drop more unused blobs and fw
- Re-implemented Dolby Atmos support(thanks to @unmoved21)
- Update blobs & fingerprint from OS3.0.6.0.WOLMIXM
- Update parts

# 28-Dec-2025
- Add props to improve battery backup
- Optimize auto brightness adjustment
- Tune ambient display burn-in protection

# 16-Dec-2025
- Synced with latest qpr1 source
- enabled the 1k nits brightness by default
- Some mics changes in boosts
- Disable Lift to check by default
- Partially import parts from sm8350-common:
* Thermals
* Per-app refresh rate
* Clear speaker
* Doze
- Force enable volte and wifi calling
- Fixed USSD dial issue
- Enabled 120Hz Keyguard
- Optimize SurfaceFlinger properties for graphics performance(This should improve graphics performance, smoothness, and screen responsiveness)
- Add Gcam by default
