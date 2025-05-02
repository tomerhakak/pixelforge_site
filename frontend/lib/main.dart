import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:pixelforge_site/pages/home_page.dart';
import 'package:pixelforge_site/theme/colors.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

void main() {
  runApp(const PixelForgeApp());
}

// GoRouter configuration
final _router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      pageBuilder: (context, state) {
        return CustomTransitionPage(
          key: state.pageKey,
          child: const HomePage(),
          transitionsBuilder: (context, animation, secondaryAnimation, child) {
            return FadeTransition(
              opacity: CurveTween(curve: Curves.easeInOutCirc).animate(animation),
              child: SlideTransition(
                position: Tween<Offset>(
                  begin: const Offset(0.0, 0.1),
                  end: Offset.zero,
                ).animate(animation),
                child: child,
              ),
            );
          },
          transitionDuration: const Duration(milliseconds: 400),
        );
      },
    ),
    // TODO: Add routes for other pages if needed (e.g., portfolio detail)
  ],
);

class PixelForgeApp extends StatelessWidget {
  const PixelForgeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [
        Locale('he', ''),
        Locale('en', ''),
      ],
      locale: const Locale('he', ''),

      title: 'PixelForge - We forge pixels. You forge success.',
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: kPrimaryBlue,
        scaffoldBackgroundColor: kPrimaryBlue,
        fontFamily: GoogleFonts.lato().fontFamily,
        colorScheme: const ColorScheme.dark(
          primary: kPrimaryBlue,
          secondary: kAccentTurquoise,
          surface: kPrimaryBlue,
          onPrimary: kWhite,
          onSecondary: kPrimaryBlue,
          onSurface: kWhite,
          error: Colors.redAccent,
          onError: kWhite,
          brightness: Brightness.dark,
        ),
        textTheme: Theme.of(context).textTheme.apply(
              bodyColor: kWhite.withOpacity(0.9),
              displayColor: kWhite,
              fontFamily: GoogleFonts.lato().fontFamily,
            ),
        useMaterial3: true,
      ),
      routerConfig: _router,
      debugShowCheckedModeBanner: false,
    );
  }
}
