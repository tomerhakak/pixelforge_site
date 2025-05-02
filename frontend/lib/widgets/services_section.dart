import 'package:flutter/material.dart';
import 'package:pixelforge_site/theme/colors.dart';
import 'package:pixelforge_site/theme/text_styles.dart';
import 'package:pixelforge_site/widgets/service_card.dart';
import 'package:flutter_animate/flutter_animate.dart'; // Ensure flutter_animate is imported
import 'package:font_awesome_flutter/font_awesome_flutter.dart'; // Import FontAwesome

class ServicesSection extends StatelessWidget {
  const ServicesSection({super.key});

  // Updated service data structure with more details
  final List<Map<String, dynamic>> services = const [
    {
      'icon': FontAwesomeIcons.desktop,
      'title': 'בניית אתרי תדמית פרימיום',
      'openingSentence': 'נוכחות דיגיטלית מרשימה שמציבה אותך מעל המתחרים.',
      'includes': [
        'עיצוב מותאם אישית – לא תבניות מוכנות',
        'אתר מהיר, חד וקל לניווט',
        'התאמה מלאה לנייד, טאבלט ומחשב',
        'מיתוג ויזואלי שמדבר בשפה שלך'
      ],
      'suitableFor': 'לעסקים, יועצים, נותני שירותים, בעלי מקצוע, אמנים ומרצים'
    },
    {
      'icon': FontAwesomeIcons.bullseye,
      'title': 'דפי נחיתה ממירים',
      'openingSentence': 'הכלי היעיל ביותר להפוך מתעניינים ללקוחות משלמים.',
      'includes': [
        'בניית דף ממוקד מטרה – מכירה, הרשמה או לידים',
        'טקסטים שיווקיים מותאמים למסר שלך',
        'אינטגרציה לטפסים, וואטסאפ, מיילים ועוד',
        'ניתוח חוויית משתמש (UX) להמרה גבוהה'
      ],
      'whyStrong': 'הדרך המהירה והממוקדת ביותר להביא לקוחות ממודעות וקמפיינים'
    },
    {
      'icon': FontAwesomeIcons.cartShopping,
      'title': 'בניית חנויות דיגיטליות (Flutter Web)',
      'openingSentence': 'חווית קנייה ייחודית שלא מרגישה כמו עוד חנות גנרית.',
      'includes': [
        'חנות מעוצבת וממוקדת מכירה',
        'ניהול מלאי, סליקה מאובטחת, עמודי מוצר',
        'חוויית משתמש חלקה ומהירה כמו באפליקציה',
        'פיתוח פיצ\'רים מותאמים אישית מאחורי הקלעים'
      ],
    },
    {
      'icon': FontAwesomeIcons.penRuler,
      'title': 'עיצוב UX/UI חכם לאתרים',
      'openingSentence': 'עיצוב שמכוון למטרות העסק שלך, לא רק שיהיה יפה.',
      'includes': [
        'תכנון חוויית משתמש ברמה הגבוהה ביותר',
        'בניית מסכים, מבנה ניווט ומיקרו־אינטראקציות',
        'התאמה מושלמת למיתוג ולקהל היעד',
        'יישום עקרונות פסיכולוגיית משתמשים'
      ]
    },
     {
      'icon': FontAwesomeIcons.networkWired,
      'title': 'חיבור לכלים חכמים (AI, CRM, אוטומציה)',
      'openingSentence': 'לרתום את הטכנולוגיה לעבוד בשבילך, לא ההפך.',
      'includes': [
        'שילוב כלים כמו ChatGPT, Google Sheets, סקרים ועוד',
        'בניית CRM מותאם אישית לניהול לקוחות ולידים',
        'אוטומציות של טפסים, תהליכים ודיווחים',
        'פיתוח לוגיקת Backend (כמו Django) לפי הצורך'
      ]
    },
    {
      'icon': FontAwesomeIcons.comments,
      'title': 'ייעוץ וליווי דיגיטלי אישי',
      'openingSentence': 'ליווי צמוד מהרעיון ועד שהאתר שלך באוויר ומצליח.',
      'includes': [
        'אפיון מעמיק של העסק והצרכים הדיגיטליים',
        'בניית תוכנית אסטרטגית לאתר/מותג',
        'בחירת הטכנולוגיות והכלים הנכונים',
        'ליווי טכני ושיווקי לאורך הדרך'
      ]
    },
  ];

  @override
  Widget build(BuildContext context) {
    bool isLargeScreen = MediaQuery.of(context).size.width > 800;
    double horizontalPadding = isLargeScreen ? 100 : 20;

    return Container(
      padding: EdgeInsets.symmetric(horizontal: horizontalPadding, vertical: 80),
      color: kPrimaryBlue,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Text(
            'השירותים של PixelForge', // Updated Title
            style: kHeadlineStyle.copyWith(fontSize: 36, color: kWhite),
            textAlign: TextAlign.center,
          ).animate().fadeIn(delay: 200.ms).slideY(begin: 0.2, duration: 400.ms),
          const SizedBox(height: 20),
          Text(
             // Added new opening sentence for the section
             'כל עסק צריך נוכחות דיגיטלית – אבל לא כל נוכחות מביאה תוצאות.\n'
             'אני בונה עבורך אתרים שעובדים – מבחינה ויזואלית, שיווקית וטכנולוגית.',
            style: kBodyStyle.copyWith(color: kWhite.withOpacity(0.85), fontSize: 18),
            textAlign: TextAlign.center,
          ).animate().fadeIn(delay: 300.ms).slideY(begin: 0.2, duration: 400.ms),
          const SizedBox(height: 60),
          LayoutBuilder(
            builder: (context, constraints) {
              int crossAxisCount = 1;
              if (constraints.maxWidth >= 1400) {
                crossAxisCount = 3; // Reduced columns for richer content
              } else if (constraints.maxWidth >= 900) {
                crossAxisCount = 2; // 2 columns for large/medium screens
              }

              final cardDelay = 150.ms; // Slightly increase stagger
              final iconCircleRadius = 35.0;

              return GridView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: crossAxisCount,
                  crossAxisSpacing: 40,
                  mainAxisSpacing: 40 + iconCircleRadius + 20,
                  // Adjust aspect ratio for the INITIAL (smaller) card size
                  childAspectRatio: crossAxisCount == 1 ? 1.0 : 1.4, // Wider than tall
                ),
                itemCount: services.length,
                itemBuilder: (context, index) {
                  final service = services[index];
                  return ServiceCard(
                    // Pass the whole map for now, card will handle extraction
                    serviceData: service,
                  )
                      .animate()
                      .fadeIn(
                        delay: cardDelay * index,
                        duration: 500.ms,
                      )
                      .slideY(
                        delay: cardDelay * index,
                        begin: 0.1,
                        duration: 400.ms,
                      );
                },
              );
            },
          ),
        ],
      ),
    );
  }
} 