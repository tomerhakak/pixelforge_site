import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'colors.dart';

// Headline style for Hero section with Orbitron font and glow
TextStyle get kHeroTitleStyle => GoogleFonts.orbitron(
      fontSize: 64, // Increased size
      fontWeight: FontWeight.bold,
      color: kAccentTurquoise,
      shadows: [
        // Create the glow effect
        const Shadow(
          blurRadius: 10.0,
          color: kAccentTurquoise,
          offset: Offset(0, 0),
        ),
        const Shadow(
          blurRadius: 20.0,
          color: kAccentTurquoise,
          offset: Offset(0, 0),
        ),
      ],
    );

// TODO: Define specific text styles based on design

TextStyle get kHeadlineStyle => GoogleFonts.lato(
      fontSize: 48, // Example size - might not be used directly now
      fontWeight: FontWeight.bold,
      color: kWhite,
    );

TextStyle get kBodyStyle => GoogleFonts.lato(
      fontSize: 18, // Slightly smaller based on image
      color: kWhite.withOpacity(0.9), // Slightly more opaque
      height: 1.5, // Improve line spacing
    );

TextStyle get kButtonStyle => GoogleFonts.lato(
      fontSize: 16, // Seems okay
      fontWeight: FontWeight.bold,
      color: kPrimaryBlue,
    ); 