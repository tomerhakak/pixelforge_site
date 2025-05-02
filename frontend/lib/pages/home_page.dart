import 'package:flutter/material.dart';
import 'package:pixelforge_site/widgets/about_me_section.dart'; // Import AboutMeSection
import 'package:pixelforge_site/widgets/hero_section.dart'; // Import HeroSection
import 'package:pixelforge_site/widgets/services_section.dart'; // Import ServicesSection
import 'package:pixelforge_site/widgets/why_pixelforge_section.dart'; // Import WhyPixelForgeSection
import 'package:pixelforge_site/widgets/portfolio_section.dart'; // Import PortfolioSection
import 'package:pixelforge_site/widgets/testimonials_section.dart'; // Import TestimonialsSection
import 'package:pixelforge_site/widgets/contact_section.dart'; // Import ContactSection
import 'package:pixelforge_site/theme/colors.dart'; // Import colors

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent, // Make scaffold transparent to see container background
      body: Container(
        // Apply background gradient to the whole page container
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              kPrimaryBlue.withBlue(kPrimaryBlue.blue - 5), // Slightly darker top
              kPrimaryBlue,
              kPrimaryBlue.withBlue(kPrimaryBlue.blue + 5), // Slightly lighter bottom
            ],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: ListView(
          children: const [
            HeroSection(), // Use the actual HeroSection widget
            SizedBox(height: 60), // Adjusted spacing after Hero
            AboutMeSection(), // Add the new section
            SizedBox(height: 60), // Added spacing before Services
            ServicesSection(), // Use the actual ServicesSection widget
            WhyPixelForgeSection(), // Use the actual WhyPixelForgeSection widget
            PortfolioSection(), // Use the actual PortfolioSection widget
            // TestimonialsSection(), // Temporarily commented out
            ContactSection(), // Use the actual ContactSection widget
            SizedBox(height: 50), // Add some padding at the bottom
          ],
        ),
      ),
    );
  }
} 