import 'package:flutter/material.dart';
import 'package:animated_text_kit/animated_text_kit.dart';
import 'package:pixelforge_site/theme/colors.dart';
import 'package:pixelforge_site/theme/text_styles.dart';
import 'package:flutter_animate/flutter_animate.dart'; // Import flutter_animate

class HeroSection extends StatelessWidget {
  const HeroSection({super.key});

  @override
  Widget build(BuildContext context) {
    double horizontalPadding = MediaQuery.of(context).size.width > 800 ? 100 : 30; // Slightly more padding on small screens

    return Container(
      height: MediaQuery.of(context).size.height * 0.95, // Increased height multiplier
      padding: EdgeInsets.symmetric(horizontal: horizontalPadding, vertical: 50),
      alignment: Alignment.center,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          // Animated Title with Orbitron, Glow, and Typewriter effect
          DefaultTextStyle(
            style: kHeroTitleStyle, // Use the new style with Orbitron and glow
            textAlign: TextAlign.center,
            child: AnimatedTextKit(
              animatedTexts: [
                TypewriterAnimatedText(
                  'PixelForge',
                  speed: const Duration(milliseconds: 150), // Adjust speed
                  cursor: '_', // Optional: add a cursor
                ),
              ],
              isRepeatingAnimation: false,
              pause: const Duration(milliseconds: 1000), // Pause before next animation if repeating
            ),
          ).animate().fadeIn(duration: 300.ms).slideY(begin: 0.1, end: 0),

          const SizedBox(height: 15), // Reduced space

          // Subtitle Text
          Text(
            "צורפות דיגיטלית פוגשת Flutter עוצמתי.\nכל פיקסל בנוי ב-Flutter, לחוויה שממירה.", // Emphasizing Flutter build
            textAlign: TextAlign.center,
            style: kBodyStyle, // Use the updated kBodyStyle
          ).animate().fadeIn(delay: 1200.ms, duration: 600.ms).slideY(begin: 0.2, end: 0), // Delayed further

          const SizedBox(height: 50), // Increased space

          // Main Button
          ElevatedButton(
            onPressed: () {
              // TODO: Implement button action (e.g., scroll to contact form)
              print("Button Pressed!");
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: kAccentTurquoise,
              padding: const EdgeInsets.symmetric(horizontal: 45, vertical: 22), // Slightly larger padding
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10), // Slightly more rounded
              ),
              elevation: 5, // Add subtle elevation
            ),
            child: Text(
              "בוא נבנה לך אתר מנצח", // Updated Text
              style: kButtonStyle, // Use updated kButtonStyle
            ),
          ).animate().fadeIn(delay: 1500.ms, duration: 600.ms).slideY(begin: 0.3, end: 0), // Delayed further
        ],
      ),
    );
  }
} 