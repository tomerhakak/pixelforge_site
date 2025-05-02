import 'package:flutter/material.dart';
import 'package:pixelforge_site/theme/colors.dart';
import 'package:pixelforge_site/theme/text_styles.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart'; // For potential icons

class AboutMeSection extends StatelessWidget {
  const AboutMeSection({super.key});

  @override
  Widget build(BuildContext context) {
    bool isLargeScreen = MediaQuery.of(context).size.width > 900;
    double horizontalPadding = isLargeScreen ? 100 : 20;
    double verticalPadding = 80;

    final Widget textContent = Column(
      crossAxisAlignment: CrossAxisAlignment.start, // Align text to start (right in RTL)
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        // Title
        Text(
          'מי אני?',
          style: kHeadlineStyle.copyWith(fontSize: 32, color: kWhite),
        )
            .animate()
            .fadeIn(delay: 200.ms, duration: 500.ms)
            .slideY(begin: 0.2, duration: 400.ms),
        const SizedBox(height: 25),

        // Introduction Text
        Text(
          'שמי תומר חקק, יזם, מפתח ומומחה בחוויית משתמש.\n'
          'אני בונה אתרים שמייצרים תוצאות – לא רק נראים טוב.\n\n'
          'אני בעל תואר ראשון במערכות מידע, עם התמחות בפיתוח תוכנה וניהול דאטה, '
          'ו־תואר שני במנהל עסקים עם התמחות בהשקעות וניהול בכיר.\n\n'
          'השילוב בין ידע טכנולוגי עמוק לבין חשיבה עסקית נותן לי יתרון ברור: '
          'אני לא רק מתכנת – אני מבין את הלקוח, את הקהל שלו, ואת איך אתר צריך להיראות כדי לייצר הכנסות.',
          style: kBodyStyle.copyWith(fontSize: 16, height: 1.6, color: kWhite.withOpacity(0.85)),
        )
            .animate()
            .fadeIn(delay: 300.ms, duration: 500.ms)
            .slideY(begin: 0.2, duration: 400.ms),

        const SizedBox(height: 40),

        // Why Flutter Section Title
        Text(
          'למה אני בונה אתרים דווקא ב־Flutter?',
          style: kHeadlineStyle.copyWith(fontSize: 24, color: kWhite), // Slightly smaller headline
        )
            .animate()
            .fadeIn(delay: 400.ms, duration: 500.ms)
            .slideY(begin: 0.2, duration: 400.ms),
        const SizedBox(height: 15),
        Text(
          'כי אני מאמין שאתר עסקי צריך להרגיש כמו אפליקציית פרימיום – לא כמו תבנית מוכנה.',
           style: kBodyStyle.copyWith(fontSize: 16, height: 1.6, color: kWhite.withOpacity(0.85)),
        )
            .animate()
            .fadeIn(delay: 500.ms, duration: 500.ms)
            .slideY(begin: 0.2, duration: 400.ms),
        const SizedBox(height: 25),

        // Flutter Benefits List
        _buildFlutterBenefitItem(
          icon: FontAwesomeIcons.mobileScreenButton,
          text: 'לבנות אתר רספונסיבי לחלוטין, שמתאים למחשב, טאבלט ונייד – בלי שברים.',
          delay: 600.ms,
        ),
        _buildFlutterBenefitItem(
          icon: FontAwesomeIcons.cubes,
          text: 'לשלוט עד רמת הפיקסל – מה שנותן לי חופש עיצוב מוחלט.',
          delay: 700.ms,
        ),
        _buildFlutterBenefitItem(
          icon: FontAwesomeIcons.wandMagicSparkles,
          text: 'ליצור אנימציות וחוויית משתמש כמו באפליקציות, לא כמו באתרי Wix/WordPress.',
          delay: 800.ms,
        ),
         _buildFlutterBenefitItem(
          icon: FontAwesomeIcons.gaugeSimpleHigh,
          text: 'מהירות פיתוח גבוהה – כך שאתה מקבל אתר מדויק בזמן קצר.',
          delay: 900.ms,
        ),
         _buildFlutterBenefitItem(
          icon: FontAwesomeIcons.codeBranch,
          text: 'מוכנות להפוך את האתר שלך בעתיד לאפליקציה – בלי לבנות מחדש.',
          delay: 1000.ms,
        ),
      ],
    );

    return Container(
      padding: EdgeInsets.symmetric(horizontal: horizontalPadding, vertical: verticalPadding),
      color: kPrimaryBlue.withBlue(kPrimaryBlue.blue - 5), // Slightly different background
      // Removed the Row/Column split based on screen size, now just centering the text content
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800), // Limit text width for readability
          child: textContent,
        ),
      ),
    );
  }

  // Helper widget for Flutter benefit items
  Widget _buildFlutterBenefitItem({required IconData icon, required String text, required Duration delay}) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 15.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          FaIcon(icon, size: 18, color: kAccentTurquoise.withOpacity(0.8)),
          const SizedBox(width: 15),
          Expanded(
            child: Text(
              text,
              style: kBodyStyle.copyWith(fontSize: 15, height: 1.5, color: kWhite.withOpacity(0.8)),
            ),
          ),
        ],
      ),
    ).animate().fadeIn(delay: delay, duration: 400.ms).slideX(begin: 0.1, duration: 300.ms);
  }
} 