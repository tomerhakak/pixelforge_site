import 'package:flutter/material.dart';
import 'package:pixelforge_site/theme/colors.dart';
import 'package:pixelforge_site/theme/text_styles.dart';
import 'package:flutter_animate/flutter_animate.dart';

class PortfolioItemCard extends StatefulWidget {
  final String title;
  final String imageUrl;
  final String tooltipMessage;

  const PortfolioItemCard({
    super.key,
    required this.title,
    required this.imageUrl,
    required this.tooltipMessage,
  });

  @override
  State<PortfolioItemCard> createState() => _PortfolioItemCardState();
}

class _PortfolioItemCardState extends State<PortfolioItemCard> {
  bool _isHovered = false;

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: widget.tooltipMessage,
      preferBelow: false,
      verticalOffset: 50,
      textStyle: kBodyStyle.copyWith(fontSize: 12, color: kPrimaryBlue),
      decoration: BoxDecoration(
        color: kAccentTurquoise,
        borderRadius: BorderRadius.circular(4),
      ),
      child: MouseRegion(
        onEnter: (_) => setState(() => _isHovered = true),
        onExit: (_) => setState(() => _isHovered = false),
        cursor: SystemMouseCursors.click, // Indicate it's clickable (for future)
        child: ClipRRect(
          borderRadius: BorderRadius.circular(12.0),
          child: Stack(
            alignment: Alignment.bottomCenter,
            children: [
              // Image with slight zoom on hover
              AnimatedScale(
                scale: _isHovered ? 1.05 : 1.0,
                duration: 250.ms,
                child: Image.network(
                  widget.imageUrl,
                  fit: BoxFit.cover,
                  width: double.infinity,
                  height: double.infinity,
                  // Add loading/error builders for better UX
                  loadingBuilder: (context, child, loadingProgress) {
                    if (loadingProgress == null) return child;
                    return const Center(child: CircularProgressIndicator(color: kAccentTurquoise));
                  },
                  errorBuilder: (context, error, stackTrace) {
                    return const Center(child: Icon(Icons.error_outline, color: Colors.redAccent));
                  },
                ),
              ),

              // Overlay that appears on hover
              AnimatedOpacity(
                opacity: _isHovered ? 1.0 : 0.0,
                duration: 250.ms,
                child: Container(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [
                        Colors.black.withOpacity(0.0),
                        Colors.black.withOpacity(0.7),
                        Colors.black.withOpacity(0.9),
                      ],
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      stops: const [0.0, 0.5, 1.0],
                    ),
                  ),
                ),
              ),

              // Title text shown on hover
              AnimatedPositioned(
                duration: 250.ms,
                bottom: _isHovered ? 20 : -50, // Slide in from bottom
                left: 20,
                right: 20,
                child: Text(
                  widget.title,
                  textAlign: TextAlign.center,
                  style: kHeadlineStyle.copyWith(fontSize: 20, color: kWhite, shadows: [
                    const Shadow(blurRadius: 4, color: Colors.black54)
                  ]),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
} 