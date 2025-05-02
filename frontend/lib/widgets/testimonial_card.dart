import 'package:flutter/material.dart';
import 'package:pixelforge_site/theme/colors.dart';
import 'package:pixelforge_site/theme/text_styles.dart';
import 'package:url_launcher/url_launcher.dart'; // For opening links
import 'package:flutter_animate/flutter_animate.dart';

class TestimonialCard extends StatelessWidget {
  final String quote;
  final String author;
  final String? company;
  final String? imageUrl;
  final String? siteUrl;

  const TestimonialCard({
    super.key,
    required this.quote,
    required this.author,
    this.company,
    this.imageUrl,
    this.siteUrl,
  });

  Future<void> _launchUrl(String? urlString) async {
    if (urlString != null) {
      final Uri url = Uri.parse(urlString);
      if (!await launchUrl(url, mode: LaunchMode.externalApplication)) {
        // Could not launch the URL
        print('Could not launch $url');
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 30),
      constraints: const BoxConstraints(maxWidth: 700), // Limit width for readability
      decoration: BoxDecoration(
        color: kPrimaryBlue.withOpacity(0.5), // Semi-transparent background
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: kAccentTurquoise.withOpacity(0.3), width: 1),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (imageUrl != null)
            CircleAvatar(
              radius: 40,
              backgroundColor: kAccentTurquoise.withOpacity(0.2),
              backgroundImage: NetworkImage(imageUrl!),
              onBackgroundImageError: (exception, stackTrace) {
                print('Error loading testimonial image: $exception');
              },
            ).animate().scale(delay: 100.ms, duration: 300.ms),
          const SizedBox(height: 20),
          Text(
            quote,
            style: kBodyStyle.copyWith(
              fontSize: 18, // Larger quote text
              fontStyle: FontStyle.italic,
              color: kWhite.withOpacity(0.9),
              height: 1.5,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 25),
          Text(
            author,
            style: kBodyStyle.copyWith(
                fontWeight: FontWeight.bold, fontSize: 16, color: kWhite),
            textAlign: TextAlign.center,
          ),
          if (company != null || siteUrl != null)
            Padding(
              padding: const EdgeInsets.only(top: 5.0),
              child: InkWell(
                onTap: () => _launchUrl(siteUrl),
                hoverColor: kAccentTurquoise.withOpacity(0.1),
                borderRadius: BorderRadius.circular(4),
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 2.0),
                  child: Text(
                    company ?? 'Visit Website', // Show company or generic text
                    style: kBodyStyle.copyWith(
                      fontSize: 14,
                      color: kAccentTurquoise,
                      decoration: siteUrl != null ? TextDecoration.underline : null,
                      decorationColor: kAccentTurquoise,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
} 