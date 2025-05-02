import 'package:flutter/material.dart';
import 'package:pixelforge_site/theme/colors.dart';
import 'package:pixelforge_site/theme/text_styles.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class WhyPixelForgeSection extends StatelessWidget {
  const WhyPixelForgeSection({super.key});

  final List<Map<String, dynamic>> points = const [
    {
      'icon': FontAwesomeIcons.hammer, // Replaced Icon (Custom Crafted)
      'title': 'Custom Crafted',
      'description': 'כל אתר נבנה ידנית, פיקסל אחר פיקסל, בלי תבניות מוכנות.',
    },
    {
      'icon': FontAwesomeIcons.featherPointed, // Replaced Icon (Built on Flutter - lightweight/performant)
      'title': 'Built on Flutter',
      'description': 'ביצועים של אפליקציה, נראות של מותג-על, חווית משתמש חלקה.',
    },
    {
      'title': 'Design That Sells',
      'icon': FontAwesomeIcons.lightbulb, // Replaced Icon (Design that Sells)
      'description': 'עיצוב אסטרטגי ממוקד המרה שמניע את המשתמשים לפעולה.',
    },
    {
      'title': 'יחס אישי',
      'icon': FontAwesomeIcons.solidComments, // Replaced Icon (Personal Touch / Communication)
      'description': 'אתה מדבר ישירות עם הבונה, לא עם מערכת או בוט.',
    },
  ];

  @override
  Widget build(BuildContext context) {
    bool isLargeScreen = MediaQuery.of(context).size.width > 900;
    double horizontalPadding = isLargeScreen ? 100 : 20;

    return Container(
      padding: EdgeInsets.symmetric(horizontal: horizontalPadding, vertical: 80),
      color: kPrimaryBlue.withBlue(kPrimaryBlue.blue + 5), // Slightly different background
      child: Column(
        children: [
          Text(
            'למה PixelForge?',
            style: kHeadlineStyle.copyWith(fontSize: 36, color: kWhite),
            textAlign: TextAlign.center,
          )
              .animate()
              .fadeIn(delay: 200.ms, duration: 500.ms)
              .slideY(begin: 0.3, duration: 400.ms),
          const SizedBox(height: 50),
          // Use Wrap for responsiveness - items flow into next line if needed
          Wrap(
            spacing: 40, // Horizontal spacing between items
            runSpacing: 40, // Vertical spacing between lines
            alignment: WrapAlignment.center,
            children: List.generate(points.length, (index) {
              final point = points[index];
              // Calculate width for items - roughly half for large screens, full for small
              final itemWidth = isLargeScreen
                  ? (MediaQuery.of(context).size.width - horizontalPadding * 2 - 40) / 2.2 // Subtract padding and spacing
                  : double.infinity;

              return SizedBox(
                width: itemWidth,
                child: _buildPointItem(
                  icon: point['icon']! as IconData,
                  title: point['title']! as String,
                  description: point['description']! as String,
                  delay: (300 + index * 150).ms,
                ),
              );
            }),
          ),
        ],
      ),
    );
  }

  Widget _buildPointItem({
    required IconData icon,
    required String title,
    required String description,
    required Duration delay,
  }) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      textDirection: TextDirection.rtl,
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: kBodyStyle.copyWith(
                    fontWeight: FontWeight.bold, fontSize: 18, color: kWhite),
                textAlign: TextAlign.start,
              ),
              const SizedBox(height: 8),
              Text(
                description,
                style: kBodyStyle.copyWith(
                    fontSize: 15, color: kWhite.withOpacity(0.8), height: 1.4),
                textAlign: TextAlign.start,
              ),
            ],
          ),
        ),
        const SizedBox(width: 20),
        FaIcon(icon, size: 30, color: kAccentTurquoise),
      ],
    )
        .animate()
        .fadeIn(delay: delay, duration: 500.ms)
        .moveX(begin: 20, delay: delay, duration: 400.ms);
  }
} 