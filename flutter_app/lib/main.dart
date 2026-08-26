import 'package:flutter/material.dart';

import 'features/auth/auth_gate.dart';

void main() {
  runApp(const VocabPlatformApp());
}

class VocabPlatformApp extends StatelessWidget {
  const VocabPlatformApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Vocab Platform',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.deepPurple,
        ),
        useMaterial3: true,
      ),
      home: const AuthGate(),
    );
  }
}r