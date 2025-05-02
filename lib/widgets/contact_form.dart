import 'package:flutter/material.dart';

class ContactForm extends StatefulWidget {
  const ContactForm({super.key});

  @override
  State<ContactForm> createState() => _ContactFormState();
}

class _ContactFormState extends State<ContactForm> {
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    // TODO: Implement Contact Form layout, Glassmorphism, and submit animation
    return Form(
      key: _formKey,
      child: Column(
        children: [
          TextFormField(decoration: const InputDecoration(labelText: 'Name')),
          TextFormField(decoration: const InputDecoration(labelText: 'Email')),
          TextFormField(decoration: const InputDecoration(labelText: 'Message'), maxLines: 3),
          const SizedBox(height: 20),
          ElevatedButton(onPressed: () {}, child: const Text('Submit')),
        ],
      ),
    );
  }
} 