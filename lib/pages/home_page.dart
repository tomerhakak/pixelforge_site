import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    // TODO: Replace with actual section widgets
    return Scaffold(
      body: ListView(
        children: const [
          Placeholder(fallbackHeight: 600, child: Center(child: Text('Hero Section'))), // Hero Section
          Placeholder(fallbackHeight: 400, child: Center(child: Text('Services'))), // Services
          Placeholder(fallbackHeight: 300, child: Center(child: Text('Why PixelForge?'))), // Why PixelForge?
          Placeholder(fallbackHeight: 500, child: Center(child: Text('Portfolio'))), // Portfolio
          Placeholder(fallbackHeight: 300, child: Center(child: Text('Testimonials'))), // Testimonials
          Placeholder(fallbackHeight: 400, child: Center(child: Text('Contact'))), // Contact
        ],
      ),
    );
  }
} 