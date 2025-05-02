import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'colors.dart';

// TODO: Define specific text styles based on design

TextStyle get kHeadlineStyle => GoogleFonts.lato(
      fontSize: 48, // Example size
      fontWeight: FontWeight.bold,
      color: kWhite,
    );

TextStyle get kBodyStyle => GoogleFonts.lato(
      fontSize: 16, // Example size
      color: kWhite.withOpacity(0.8),
    );

TextStyle get kButtonStyle => GoogleFonts.lato(
      fontSize: 18, // Example size
      fontWeight: FontWeight.bold,
      color: kPrimaryBlue,
    ); 