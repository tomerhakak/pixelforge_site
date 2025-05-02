import 'dart:ui'; // Import for ImageFilter

import 'package:flutter/material.dart';
import 'package:pixelforge_site/theme/colors.dart';
import 'package:pixelforge_site/theme/text_styles.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart'; // Import FontAwesome

class ServiceCard extends StatefulWidget {
  // Accepts the whole service data map
  final Map<String, dynamic> serviceData;

  const ServiceCard({
    super.key,
    required this.serviceData,
  });

  @override
  State<ServiceCard> createState() => _ServiceCardState();
}

class _ServiceCardState extends State<ServiceCard> with SingleTickerProviderStateMixin {
  bool _isHovered = false;
  final double iconCircleRadius = 35.0;
  late AnimationController _sizeController;
  late Animation<double> _sizeAnimation;

  @override
  void initState() {
    super.initState();
    _sizeController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 400),
    );
    _sizeAnimation = CurvedAnimation(parent: _sizeController, curve: Curves.easeInOut);

    // Trigger expansion automatically after a short delay
    Future.delayed(const Duration(milliseconds: 250), () { // Adjust delay as needed
      if (mounted) {
        _sizeController.forward();
      }
    });
  }

  @override
  void dispose() {
    _sizeController.dispose();
    super.dispose();
  }

  void _handleHover(bool hovering) {
    setState(() => _isHovered = hovering);
  }

  @override
  Widget build(BuildContext context) {
    // Extract data from the map
    final IconData icon = widget.serviceData['icon'] as IconData;
    final String title = widget.serviceData['title'] as String;
    final String openingSentence = widget.serviceData['openingSentence'] as String;
    final List<String> includes = List<String>.from(widget.serviceData['includes'] ?? []);
    final String? suitableFor = widget.serviceData['suitableFor'] as String?;
    final String? whyStrong = widget.serviceData['whyStrong'] as String?;

    final cardBorderRadius = BorderRadius.circular(16.0);
    final hoverColor1 = Colors.purpleAccent.withOpacity(0.6);
    final hoverColor2 = kAccentTurquoise.withOpacity(0.7);

    // Widget for the detailed content (includes list and footer)
    final Widget detailedContent = Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 20),
        Text(
          'מה זה כולל:',
          style: kBodyStyle.copyWith(
              fontWeight: FontWeight.w600,
              fontSize: 14,
              color: kAccentTurquoise.withOpacity(0.9)),
        ),
        const SizedBox(height: 8),
        ...includes.map((item) => _buildIncludeItem(item)).toList(),
        const SizedBox(height: 15),
        if (suitableFor != null || whyStrong != null)
          Text(
            suitableFor ?? whyStrong ?? '',
            style: kBodyStyle.copyWith(
                fontSize: 13,
                color: kWhite.withOpacity(0.7),
                fontStyle: FontStyle.italic),
          ),
      ],
    );

    // Remove the outer Animate wrapper, entry animation is handled in parent
    return MouseRegion(
      onEnter: (_) => _handleHover(true),
      onExit: (_) => _handleHover(false),
      cursor: SystemMouseCursors.click,
      child: Stack(
        clipBehavior: Clip.none,
        alignment: Alignment.topCenter,
        children: [
          Container(
            margin: EdgeInsets.only(top: iconCircleRadius),
            child: SizeTransition(
              sizeFactor: _sizeAnimation,
              axisAlignment: -1.0,
              child: AnimatedBuilder(
                  animation: _sizeController,
                  builder: (context, child) {
                    return Container(
                      decoration: BoxDecoration(
                        borderRadius: cardBorderRadius,
                        gradient: LinearGradient(
                          colors: [
                            kPrimaryBlue.withOpacity(0.85),
                            kPrimaryBlue.withBlue(kPrimaryBlue.blue + 10).withOpacity(0.90),
                          ],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                        boxShadow: _isHovered ? [
                          BoxShadow(color: hoverColor1.withOpacity(0.3), blurRadius: 15, spreadRadius: 1),
                          BoxShadow(color: hoverColor2.withOpacity(0.3), blurRadius: 15, spreadRadius: 1),
                        ] : [],
                      ),
                      child: ClipRRect(
                        borderRadius: cardBorderRadius,
                        child: BackdropFilter(
                          filter: ImageFilter.blur(sigmaX: _isHovered ? 5 : 2, sigmaY: _isHovered ? 5 : 2),
                          child: Container(
                            width: double.infinity,
                            padding: EdgeInsets.fromLTRB(25, iconCircleRadius + 15, 25, 25),
                            decoration: BoxDecoration(
                              borderRadius: cardBorderRadius,
                              border: Border.all(
                                color: _isHovered ? hoverColor2.withOpacity(0.8) : Colors.white.withOpacity(0.15),
                                width: _isHovered ? 2.0 : 1.5,
                              ),
                              color: Colors.transparent,
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Text(
                                  title,
                                  style: kBodyStyle.copyWith(
                                      fontWeight: FontWeight.bold,
                                      fontSize: 19,
                                      color: kWhite,
                                      height: 1.3),
                                ),
                                const SizedBox(height: 12),
                                Text(
                                  openingSentence,
                                  style: kBodyStyle.copyWith(
                                      fontSize: 14,
                                      color: kWhite.withOpacity(0.85),
                                      height: 1.4),
                                ),
                                // Detailed content is now included directly
                                detailedContent,
                              ],
                            ),
                          ),
                        ),
                      ),
                    );
                  },
                ),
            ),
          ),

          // Icon Circle (remains mostly the same)
          Positioned(
            top: 0,
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 250),
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: LinearGradient(
                  colors: _isHovered ? [hoverColor1.withOpacity(0.9), hoverColor2.withOpacity(0.9)] : [kPrimaryBlue.withBlue(50), kAccentTurquoise.withOpacity(0.5)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                border: Border.all(
                  color: _isHovered ? kWhite.withOpacity(0.5) : kWhite.withOpacity(0.2),
                  width: 1.5,
                ),
                boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.4), blurRadius: 10, offset: const Offset(0, 4))],
              ),
              child: FaIcon(
                icon,
                size: iconCircleRadius * 0.8,
                color: kWhite,
              ),
            ),
          ),
        ],
      ),
    );
  }

  // Helper to build list items for the 'includes' section
  Widget _buildIncludeItem(String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 6.0, right: 5.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.only(top: 5.0, left: 8.0),
            child: FaIcon(FontAwesomeIcons.check, size: 10, color: kAccentTurquoise.withOpacity(0.8)),
          ),
          Expanded(
            child: Text(
              text,
              style: kBodyStyle.copyWith(fontSize: 13, height: 1.4, color: kWhite.withOpacity(0.75)),
            ),
          ),
        ],
      ),
    );
  }
} 