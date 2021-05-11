import API from '../../api'

export class AuthService {
  getToken(credentials) {
    return API
      .post("api/v1/auth/token", credentials)
      .then(result => result.data)
  }

  loginNormal = (userCredential) => {
    return API.post("api/v1/auth/get-token", userCredential)
  }

  signupNormal = (userCredential) => {
    console.log("[userCredential]", userCredential);
    return API.post("api/v1/auth/user", userCredential)
  }

  // Create user account if not exist
  // Signup and Login are combined into one single function
  authByFacebook = (fbResponse) => {
    const body = {
      fbToken: fbResponse.accessToken,
      fbId: fbResponse.id
    }
    return API.post("api/v1/auth/get-token/fb", body)
  }

  // Create user account if not exist
  // Signup and Login are combined into one single function
  authByGoogle = (ggResponse) => {
    const body = {
      ggToken: ggResponse.accessToken,
      ggId: ggResponse.googleId
    }
    return API.post("api/v1/auth/get-token/gg", body)

  }
}

export default AuthService
