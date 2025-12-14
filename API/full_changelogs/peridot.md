# 14-Dec-2025

- Latest QPR1 source changes
- Dec security patch
- Kernel: Switched to Glacium-2.3 (NonRooted)
- Updated blobs from OS2.0.206.0.VNPMIXM
- Updated some Camera blobs from aurora for better processing
- Implement haptics xiaomi effects
- Implement idle manager for better idle(Enable toggle battery/Idle manager)
- Dropped parts:Refresh rate impl (use rom per app refresh rate-better)
- Dropped parts:Saturation impl (use rom impl settings/display/colors)
- Rework boost freq implementation with seperate implementation
- Rework fastcharge implementation (custom implementation in slow and superfast mode)
- Tuned dev-frq boost implementation
- powertools: Updated CPU Sets defaults
- Powertools: Implement custom configuration and backup functionality
- Implement Displayfeature color service
- Updated Dolby Implementation
- Implement miui proved color modes
- Bring back bypass charging feature (fake)
- Use night_charging node for lineage charge control (only works above 80%)
- Added PSI-based LMKD configuration
- Updated HintManager for better CPU scheduling
- Force enable volte , vonr for unsupported carrier
- Implment QCOM custom doze
- Tuned powerhint for balanced profile
- Tuned boost freq implementation for better CPU scheduling
- lmkd optimize scheduling
- Fix SCREEN_BRIGHTNESS inconsistency issue before and after reboot
- updated BCR to 1.87
- Misc Other Changes


# 23-Nov-2025

- Initial ASCP build
- Based on latest qpr1 spurce
- kernel: Nitron-2.6 (non rooted)
