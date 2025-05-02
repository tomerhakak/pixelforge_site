import 'package:flutter/material.dart';

class ServiceCard extends StatelessWidget {
  final String title;
  final String description; // Add more parameters as needed

  const ServiceCard({super.key, required this.title, required this.description});

  @override
  Widget build(BuildContext context) {
    // TODO: Implement Service Card layout and hover effect
    return Card(
      child: ListTile(
        title: Text(title),
        subtitle: Text(description),
      ),
    );
  }
} 