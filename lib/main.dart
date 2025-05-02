import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:pixelforge_site/pages/home_page.dart';
import 'package:pixelforge_site/theme/colors.dart';

void main() {
  runApp(const PixelForgeApp());
}

// GoRouter configuration
final _router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomePage(),
    ),
    // TODO: Add routes for other pages if needed (e.g., portfolio detail)
  ],
);

class PixelForgeApp extends StatelessWidget {
  const PixelForgeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'PixelForge - We forge pixels. You forge success.',
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: kPrimaryBlue,
        scaffoldBackgroundColor: kPrimaryBlue,
        colorScheme: const ColorScheme.dark(
          primary: kPrimaryBlue,
          secondary: kAccentTurquoise,
          surface: kPrimaryBlue, // Background for cards, dialogs etc.
          onPrimary: kWhite,
          onSecondary: kPrimaryBlue,
          onSurface: kWhite, // Text/icon color on surface
          error: Colors.redAccent, // Example error color
          onError: kWhite,
          brightness: Brightness.dark,
        ),
        // TODO: Integrate google_fonts text theme
        textTheme: Theme.of(context).textTheme.apply(bodyColor: kWhite, displayColor: kWhite),
        // TODO: Define button themes, card themes etc.
        useMaterial3: true,
      ),
      routerConfig: _router,
      debugShowCheckedModeBanner: false, // Optional: Remove debug banner
    );
  }
}
