import 'package:flutter/material.dart';
import 'package:pixelforge_site/theme/colors.dart';
import 'package:pixelforge_site/theme/text_styles.dart';
import 'package:pixelforge_site/widgets/portfolio_item_card.dart'; // Will be created next
import 'package:flutter_animate/flutter_animate.dart';

class PortfolioSection extends StatelessWidget {
  const PortfolioSection({super.key});

  // Placeholder data for portfolio items
  final List<Map<String, String>> portfolioItems = const [
    {
      'title': 'פרויקט אלפא',
      'imageUrl': 'https://via.placeholder.com/600x400/1C1F2B/00E5FF?text=Project+Alpha',
      'tooltip': 'נבנה ב-Flutter תוך 7 ימים'
    },
    {
      'title': 'פרויקט בטא',
      'imageUrl': 'https://via.placeholder.com/600x400/333333/FFFFFF?text=Project+Beta',
      'tooltip': 'דף נחיתה ממיר'
    },
    {
      'title': 'פרויקט גמא',
      'imageUrl': 'https://via.placeholder.com/600x400/00E5FF/1C1F2B?text=Project+Gamma',
      'tooltip': 'חנות Flutter Web'
    },
    // Add more items as needed
  ];

  @override
  Widget build(BuildContext context) {
    bool isLargeScreen = MediaQuery.of(context).size.width > 800;
    double horizontalPadding = isLargeScreen ? 100 : 20;

    return Container(
      padding: EdgeInsets.symmetric(horizontal: horizontalPadding, vertical: 80),
      color: kPrimaryBlue, // Match the main background
      child: Column(
        children: [
          Text(
            'תיק עבודות נבחרות',
            style: kHeadlineStyle.copyWith(fontSize: 36, color: kWhite),
            textAlign: TextAlign.center,
          )
              .animate()
              .fadeIn(delay: 200.ms, duration: 500.ms)
              .slideY(begin: 0.3, duration: 400.ms),
          const SizedBox(height: 50),
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: isLargeScreen ? 3 : 1, // Adjust columns based on screen size
              crossAxisSpacing: 30,
              mainAxisSpacing: 30,
              childAspectRatio: 1.2, // Adjust aspect ratio for image cards
            ),
            itemCount: portfolioItems.length,
            itemBuilder: (context, index) {
              final item = portfolioItems[index];
              return PortfolioItemCard(
                title: item['title']!,
                imageUrl: item['imageUrl']!,
                tooltipMessage: item['tooltip']!,
              )
                  .animate()
                  .fadeIn(delay: (300 + index * 150).ms, duration: 400.ms)
                  .slideY(delay: (300 + index * 150).ms, begin: 0.2, duration: 300.ms);
            },
          ),
          // TODO: Add a button to view full portfolio if needed
        ],
      ),
    );
  }
} 