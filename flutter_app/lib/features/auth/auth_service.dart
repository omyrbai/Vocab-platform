import 'dart:convert';

import 'package:http/http.dart' as http;

import '../../core/storage/token_storage.dart';

class AuthService {
  AuthService({
    TokenStorage? tokenStorage,
  }) : _tokenStorage = tokenStorage ?? TokenStorage();

  final TokenStorage _tokenStorage;

  // We will replace this with the correct address for your FastAPI server.
  static const String _baseUrl = 'http://10.0.2.2:8000';

  Future<bool> login({
    required String identifier,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/api/v1/auth/login'),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'identifier': identifier,
        'password': password,
      }),
    );

    if (response.statusCode != 200) {
      return false;
    }

    final data = jsonDecode(response.body) as Map<String, dynamic>;

    await _tokenStorage.saveTokens(
      accessToken: data['access_token'] as String,
      refreshToken: data['refresh_token'] as String,
    );

    return true;
  }

  Future<void> logout() async {
    await _tokenStorage.clearTokens();
  }
  Future<bool> refreshToken() async {
  final refreshToken = await _tokenStorage.getRefreshToken();

  if (refreshToken == null || refreshToken.isEmpty) {
    return false;
  }

  final response = await http.post(
    Uri.parse('$_baseUrl/api/v1/auth/refresh'),
    headers: {
      'Content-Type': 'application/json',
    },
    body: jsonEncode({
      'refresh_token': refreshToken,
    }),
  );

  if (response.statusCode != 200) {
    await _tokenStorage.clearTokens();
    return false;
  }

  final data = jsonDecode(response.body) as Map<String, dynamic>;

  await _tokenStorage.saveTokens(
    accessToken: data['access_token'] as String,
    refreshToken: data['refresh_token'] as String,
  );

  return true;
}
}