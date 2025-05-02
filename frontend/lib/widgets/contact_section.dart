import 'package:flutter/material.dart';
import 'package:pixelforge_site/theme/colors.dart';
import 'package:pixelforge_site/theme/text_styles.dart';
import 'package:pixelforge_site/widgets/contact_form.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:url_launcher/url_launcher.dart'; // For social links
import 'package:font_awesome_flutter/font_awesome_flutter.dart'; // Import FontAwesome

class ContactSection extends StatelessWidget {
  const ContactSection({super.key});

  Future<void> _launchUrl(String urlString) async {
    final Uri url = Uri.parse(urlString);
    if (!await launchUrl(url, mode: LaunchMode.externalApplication)) {
      print('Could not launch $url');
    }
  }

  @override
  Widget build(BuildContext context) {
    bool isLargeScreen = MediaQuery.of(context).size.width > 900;
    double horizontalPadding = isLargeScreen ? 100 : 20;

    // TODO: Replace with actual links
    const String whatsappUrl = 'https://wa.me/YOUR_NUMBER_HERE'; // Replace with your WhatsApp number link
    const String instagramUrl = 'https://instagram.com/YOUR_PROFILE';
    const String linkedinUrl = 'https://linkedin.com/in/YOUR_PROFILE';

    return Container(
      padding: EdgeInsets.symmetric(horizontal: horizontalPadding, vertical: 80),
      color: kPrimaryBlue, // Match main background
      // TODO: Consider adding a subtle background image/gradient here?
      child: Column(
        children: [
          Text(
            'רוצה אתר כזה?',
            style: kHeadlineStyle.copyWith(fontSize: 36, color: kWhite),
            textAlign: TextAlign.center,
          )
              .animate()
              .fadeIn(delay: 200.ms, duration: 500.ms)
              .slideY(begin: 0.3, duration: 400.ms),
          const SizedBox(height: 15),
          Text(
            'תן לפיקסלים שלי להתחיל לעבוד עליך.',
            style: kBodyStyle.copyWith(color: kWhite.withOpacity(0.8), fontSize: 18),
            textAlign: TextAlign.center,
          )
              .animate()
              .fadeIn(delay: 300.ms, duration: 500.ms)
              .slideY(begin: 0.3, duration: 400.ms),
          const SizedBox(height: 50),

          // Constrain the width of the form
          ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 600),
            child: const ContactForm(), // The form widget
          )
              .animate()
              .fadeIn(delay: 400.ms, duration: 500.ms)
              .slideY(begin: 0.3, duration: 400.ms),

          const SizedBox(height: 40),

          // Social Media Icons
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _buildSocialButton(FontAwesomeIcons.whatsapp, () => _launchUrl(whatsappUrl)), // Replaced Icon
              const SizedBox(width: 25),
              _buildSocialButton(FontAwesomeIcons.instagram, () => _launchUrl(instagramUrl)), // Replaced Icon
              const SizedBox(width: 25),
              _buildSocialButton(FontAwesomeIcons.linkedinIn, () => _launchUrl(linkedinUrl)), // Replaced Icon
            ],
          )
              .animate()
              .fadeIn(delay: 500.ms, duration: 500.ms)
              .slideY(begin: 0.3, duration: 400.ms),
        ],
      ),
    );
  }

  Widget _buildSocialButton(IconData icon, VoidCallback onPressed) {
    // Use FaIcon for FontAwesome icons
    return IconButton(
      icon: FaIcon(icon, color: kAccentTurquoise, size: 28),
      onPressed: onPressed,
      tooltip: 'Connect with us', // Generic tooltip
      splashRadius: 25,
      hoverColor: kAccentTurquoise.withOpacity(0.1),
    );
  }
} 