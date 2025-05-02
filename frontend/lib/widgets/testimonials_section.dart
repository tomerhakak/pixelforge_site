import 'dart:async';

import 'package:flutter/material.dart';
import 'package:pixelforge_site/theme/colors.dart';
import 'package:pixelforge_site/theme/text_styles.dart';
import 'package:pixelforge_site/widgets/testimonial_card.dart';
import 'package:flutter_animate/flutter_animate.dart';

class TestimonialsSection extends StatefulWidget {
  const TestimonialsSection({super.key});

  @override
  State<TestimonialsSection> createState() => _TestimonialsSectionState();
}

class _TestimonialsSectionState extends State<TestimonialsSection> {
  int _currentIndex = 0;
  Timer? _timer;

  // Placeholder data for testimonials
  final List<Map<String, String?>> testimonials = const [
    {
      'quote': '"וואו! האתר החדש נראה מדהים ועובד חלק כמו אפליקציה. ממליץ בחום על PixelForge!"',
      'author': 'דוד כהן',
      'company': 'אלפא פתרונות בע"מ',
      'imageUrl': 'https://via.placeholder.com/150/00E5FF/1C1F2B?text=DK',
      'siteUrl': '#', // Replace with actual URL
    },
    {
      'quote': '"תהליך העבודה היה מקצועי ומהיר, והתוצאה הסופית עלתה על כל הציפיות. תודה!"',
      'author': 'יעל לוי',
      'company': 'סטודיו בטא לעיצוב',
      'imageUrl': 'https://via.placeholder.com/150/1C1F2B/FFFFFF?text=YL',
      'siteUrl': '#',
    },
    {
      'quote': '"היכולת לבנות אתר כזה ב-Flutter היא גיים צ\'יינג\'ר. הביצועים מדהימים."',
      'author': 'משה ישראלי',
      'company': 'גמא טכנולוגיות',
      'imageUrl': 'https://via.placeholder.com/150/333333/FFFFFF?text=MY',
      'siteUrl': '#',
    },
  ];

  @override
  void initState() {
    super.initState();
    // Start the timer to switch testimonials
    _timer = Timer.periodic(const Duration(seconds: 7), (timer) {
      if (mounted) { // Check if the widget is still in the tree
        setState(() {
          _currentIndex = (_currentIndex + 1) % testimonials.length;
        });
      }
    });
  }

  @override
  void dispose() {
    _timer?.cancel(); // Cancel the timer when the widget is disposed
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    bool isLargeScreen = MediaQuery.of(context).size.width > 800;
    double horizontalPadding = isLargeScreen ? 100 : 20;

    return Container(
      padding: EdgeInsets.symmetric(horizontal: horizontalPadding, vertical: 80),
      color: kPrimaryBlue.withBlue(kPrimaryBlue.blue + 10), // Slightly different background
      child: Column(
        children: [
          Text(
            'הלקוחות שלנו מספרים',
            style: kHeadlineStyle.copyWith(fontSize: 36, color: kWhite),
            textAlign: TextAlign.center,
          )
              .animate()
              .fadeIn(delay: 200.ms, duration: 500.ms)
              .slideY(begin: 0.3, duration: 400.ms),
          const SizedBox(height: 50),
          AnimatedSwitcher(
            duration: const Duration(milliseconds: 500), // Switch animation duration
            transitionBuilder: (Widget child, Animation<double> animation) {
              // Fade transition between testimonials
              return FadeTransition(opacity: animation, child: child);
            },
            child: TestimonialCard(
              // Use key to ensure AnimatedSwitcher updates correctly
              key: ValueKey<int>(_currentIndex),
              quote: testimonials[_currentIndex]['quote']!,
              author: testimonials[_currentIndex]['author']!,
              company: testimonials[_currentIndex]['company'],
              imageUrl: testimonials[_currentIndex]['imageUrl'],
              siteUrl: testimonials[_currentIndex]['siteUrl'],
            ),
          ),
        ],
      ),
    );
  }
} 