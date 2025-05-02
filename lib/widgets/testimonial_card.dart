import 'package:flutter/material.dart';

class TestimonialCard extends StatelessWidget {
  final String quote;
  final String author;
  final String? imageUrl;
  final String? siteUrl;

  const TestimonialCard({
    super.key,
    required this.quote,
    required this.author,
    this.imageUrl,
    this.siteUrl,
  });

  @override
  Widget build(BuildContext context) {
    // TODO: Implement Testimonial Card layout
    return Card(
      child: ListTile(
        leading: imageUrl != null ? CircleAvatar(backgroundImage: NetworkImage(imageUrl!)) : null,
        title: Text(quote),
        subtitle: Text(author),
      ),
    );
  }
} 