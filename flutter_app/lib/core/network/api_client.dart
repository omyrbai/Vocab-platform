import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';

import '../storage/token_storage.dart';
import '../../features/auth/auth_service.dart';


class ApiClient {
  ApiClient({
    TokenStorage? tokenStorage,
    AuthService? authService,
    this.onTokenRefreshed,
  })  : _tokenStorage = tokenStorage ?? TokenStorage(),
        _authService = authService ?? AuthService();

  final TokenStorage _tokenStorage;
  final AuthService _authService;

  final VoidCallback? onTokenRefreshed;

  static const String _baseUrl = 'http://10.0.2.2:8000';

  // Only one refresh operation can happen at a time.
  Future<bool>? _refreshFuture;

  Future<http.Response> get(String path) async {
    return _sendWithAuth(
      method: 'GET',
      path: path,
    );
  }

  Future<http.Response> patch(
    String path, {
    Map<String, dynamic>? body,
  }) async {
    return _sendWithAuth(
      method: 'PATCH',
      path: path,
      body: body,
    );
  }

  Future<bool> _refreshTokenOnce() async {
    final existingRefresh = _refreshFuture;

    if (existingRefresh != null) {
      return existingRefresh;
    }

    final refreshFuture = _authService.refreshToken();

    _refreshFuture = refreshFuture;

    try {
      return await refreshFuture;
    } finally {
      if (identical(_refreshFuture, refreshFuture)) {
        _refreshFuture = null;
      }
    }
  }

  Future<http.Response> _sendWithAuth({
    required String method,
    required String path,
    Map<String, dynamic>? body,
    bool isRetry = false,
  }) async {
    final accessToken = await _tokenStorage.getAccessToken();

    final headers = <String, String>{
      'Content-Type': 'application/json',
    };

    if (accessToken != null && accessToken.isNotEmpty) {
      headers['Authorization'] = 'Bearer $accessToken';
    }

    final uri = Uri.parse('$_baseUrl$path');

    late http.Response response;

    if (method == 'GET') {
      response = await http.get(
        uri,
        headers: headers,
      );
    } else if (method == 'PATCH') {
      response = await http.patch(
        uri,
        headers: headers,
        body: body == null ? null : jsonEncode(body),
      );
    } else {
      throw UnsupportedError(
        'Unsupported HTTP method: $method',
      );
    }

    if (response.statusCode == 401 && !isRetry) {
      final refreshed = await _refreshTokenOnce();

      if (refreshed) {
        onTokenRefreshed?.call();
        
        return _sendWithAuth(
          method: method,
          path: path,
          body: body,
          isRetry: true,
        );
      }

      await _tokenStorage.clearTokens();
    }

    return response;
  }
}