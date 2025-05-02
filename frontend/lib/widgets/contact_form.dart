import 'dart:ui'; // For ImageFilter
import 'dart:convert'; // For jsonEncode

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http; // Import http package
import 'package:pixelforge_site/theme/colors.dart';
import 'package:pixelforge_site/theme/text_styles.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart'; // Import FontAwesome

class ContactForm extends StatefulWidget {
  const ContactForm({super.key});

  @override
  State<ContactForm> createState() => _ContactFormState();
}

class _ContactFormState extends State<ContactForm> {
  final _formKey = GlobalKey<FormState>();
  bool _isSubmitting = false; // For submit animation state

  // Add TextEditingControllers
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _messageController = TextEditingController();

  @override
  void dispose() {
    // Dispose controllers
    _nameController.dispose();
    _emailController.dispose();
    _messageController.dispose();
    super.dispose();
  }

  // Updated form submission logic
  Future<void> _submitForm() async {
    if (_formKey.currentState!.validate()) {
      setState(() => _isSubmitting = true);

      // !!! REPLACE WITH YOUR ACTUAL DJANGO API ENDPOINT URL !!!
      const String apiUrl = 'YOUR_DJANGO_API_ENDPOINT_HERE'; 
      // Example: 'https://yourdomain.com/api/leads/'

      if (apiUrl == 'YOUR_DJANGO_API_ENDPOINT_HERE') {
         print("!!! Please replace YOUR_DJANGO_API_ENDPOINT_HERE in contact_form.dart !!!");
         // Simulate delay and reset form for demo purposes
         await Future.delayed(const Duration(seconds: 2));
         ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('הודעה נשלחה בהצלחה (סימולציה)'), backgroundColor: Colors.green),
         );
         if (mounted) {
             setState(() => _isSubmitting = false);
            _formKey.currentState!.reset();
            _nameController.clear();
            _emailController.clear();
            _messageController.clear();
         }
         return; 
      }

      try {
        final response = await http.post(
          Uri.parse(apiUrl),
          headers: {
            'Content-Type': 'application/json; charset=UTF-8',
          },
          body: jsonEncode({
            'name': _nameController.text,
            'email': _emailController.text,
            'message': _messageController.text,
          }),
        );

        if (mounted) { // Check if widget is still mounted before showing SnackBar/setting state
           if (response.statusCode == 201 || response.statusCode == 200) { // 201 Created or 200 OK
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('הודעה נשלחה בהצלחה!'), backgroundColor: Colors.green),
            );
            _formKey.currentState!.reset();
            _nameController.clear();
            _emailController.clear();
            _messageController.clear();
          } else {
            // Handle error - Log details or show specific message
            print('Failed to submit form: ${response.statusCode} ${response.body}');
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('שגיאה בשליחת ההודעה. נסה שוב מאוחר יותר.'), backgroundColor: Colors.red),
            );
          }
        }
      } catch (e) {
        // Handle network or other errors
        print('Error submitting form: $e');
         if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
             SnackBar(content: Text('שגיאת רשת. בדוק את החיבור ונסה שוב.'), backgroundColor: Colors.red),
            );
         }
      } finally {
         if (mounted) {
            setState(() => _isSubmitting = false);
         }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final inputBorder = OutlineInputBorder(
      borderRadius: BorderRadius.circular(8),
      borderSide: BorderSide(color: kWhite.withOpacity(0.3), width: 1),
    );
    final focusedInputBorder = OutlineInputBorder(
      borderRadius: BorderRadius.circular(8),
      borderSide: BorderSide(color: kAccentTurquoise.withOpacity(0.8), width: 1.5),
    );

    return ClipRRect(
      borderRadius: BorderRadius.circular(15.0),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 10.0, sigmaY: 10.0),
        child: Container(
          padding: const EdgeInsets.all(30.0),
          decoration: BoxDecoration(
            color: kWhite.withOpacity(0.1), // Glassy background color
            borderRadius: BorderRadius.circular(15.0),
            border: Border.all(
              color: kWhite.withOpacity(0.2),
              width: 1.5,
            ),
          ),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                _buildTextFormField('שם', FontAwesomeIcons.user, controller: _nameController),
                const SizedBox(height: 20),
                _buildTextFormField('אימייל', FontAwesomeIcons.solidEnvelope,
                    keyboardType: TextInputType.emailAddress, controller: _emailController),
                const SizedBox(height: 20),
                _buildTextFormField('הודעה', FontAwesomeIcons.solidCommentDots,
                    maxLines: 4, controller: _messageController),
                const SizedBox(height: 30),
                ElevatedButton(
                  onPressed: _isSubmitting ? null : _submitForm,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: kAccentTurquoise,
                    padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 18),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                    textStyle: kButtonStyle,
                  ),
                  child: _isSubmitting
                      ? const SizedBox(
                          height: 20, width: 20,
                          child: CircularProgressIndicator(strokeWidth: 2, color: kPrimaryBlue),
                        )
                      : const Text('שליחה'),
                  // TODO: Add cool submit animation wrapping this button or the Text
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTextFormField(String label, IconData icon, {int maxLines = 1, TextInputType? keyboardType, required TextEditingController controller}) {
     final inputBorder = OutlineInputBorder(
      borderRadius: BorderRadius.circular(8),
      borderSide: BorderSide(color: kWhite.withOpacity(0.3), width: 1),
    );
    final focusedInputBorder = OutlineInputBorder(
      borderRadius: BorderRadius.circular(8),
      borderSide: BorderSide(color: kAccentTurquoise.withOpacity(0.8), width: 1.5),
    );

    return TextFormField(
      controller: controller, // Assign the controller
      maxLines: maxLines,
      keyboardType: keyboardType,
      style: kBodyStyle.copyWith(color: kWhite),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: kBodyStyle.copyWith(color: kWhite.withOpacity(0.6)),
        prefixIcon: FaIcon(icon, color: kWhite.withOpacity(0.6), size: 18),
        filled: true,
        fillColor: kWhite.withOpacity(0.05),
        contentPadding: const EdgeInsets.symmetric(vertical: 15, horizontal: 20),
        border: inputBorder,
        enabledBorder: inputBorder,
        focusedBorder: focusedInputBorder,
        // TODO: Add more specific error styling if needed
        errorStyle: const TextStyle(color: Colors.redAccent),
      ),
      validator: (value) {
        if (value == null || value.isEmpty) {
          return 'שדה חובה';
        }
        if (label == 'אימייל' && !RegExp(r"^\S+@\S+\.\S+$").hasMatch(value)) {
           return 'כתובת אימייל לא תקינה';
        }
        return null;
      },
    );
  }
} 