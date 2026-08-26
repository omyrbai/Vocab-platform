import 'auth_service.dart';

class AuthController {
  AuthController({
    AuthService? authService,
  }) : _authService = authService ?? AuthService();

  final AuthService _authService;

  Future<bool> restoreSession() async {
    return _authService.refreshToken();
  }

  Future<bool> login({
    required String identifier,
    required String password,
  }) async {
    return _authService.login(
      identifier: identifier,
      password: password,
    );
  }

  Future<void> logout() async {
    await _authService.logout();
  }
}