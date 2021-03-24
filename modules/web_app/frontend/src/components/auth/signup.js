import { Modal } from "react-bootstrap"
import FacebookLogin from 'react-facebook-login/dist/facebook-login-render-props'
import { GoogleLogin } from 'react-google-login'
import { FaFacebookSquare } from "react-icons/fa"
import { FcGoogle } from "react-icons/fc"
import { AuthMode, HTTP_CODE, Severity } from "../../shared/constants"
import ReactIconRender from "../../shared/react-icon-renderer"
import { ToastService } from "../../shared/toast.service"
import AuthService from "./auth-service"
import './auth.css'
import ValidatedSignupForm from "./vaidated-signup-form"

function SignupModal(props) {
  const setUserData = props.setUserData
  const authService = new AuthService()
  const toastService = new ToastService()

  const onSubmitSignup = (signupMode, userCredential, modalProps) => {
    let httpRequest = authService.signupNormal(userCredential)
    if (signupMode === AuthMode.Facebook) httpRequest = authService.authByFacebook(userCredential)
    if (signupMode === AuthMode.Google) httpRequest = authService.authByGoogle(userCredential)

    httpRequest.then(
      result => {
        if (result.status !== HTTP_CODE.SUCCESS) {
          toastService.displayToast(result, Severity.Warning)
          return
        }
        setUserData(result.data && result.data.user)
        toastService.displayToast(result, Severity.Success)
        modalProps.onHide()
      },
      error => toastService.displayToast(error.response, Severity.Error)
    )
  }

  return (
    <Modal {...props} aria-labelledby="contained-modal-title-vcenter">
      <div style={{ padding: "20px" }}>
        <div className="layout-grid centered-container auth-heading"><h2>Đăng ký</h2></div>
        <div className="layout-grid centered-container margin-bottom--20">
          <GoogleLogin
            clientId="xxx"
            buttonText="Login"
            onSuccess={(ggResponse) => onSubmitSignup(AuthMode.Google, ggResponse, props)}
            onFailure={(ggResponse) => { }}
            cookiePolicy={'single_host_origin'}
            render={renderProps => (
              <div onClick={renderProps.onClick}>
                <ReactIconRender className={'ext-login-btn'} color={'#4267B2'} IconComponent={FcGoogle} />
              </div>
            )}
          />
          <FacebookLogin style={{ 'margin-top': '-5px' }}
            appId="800436117349613"
            fields="name,email,picture"
            cssClass="btn btn-primary btn-block mt-2 ext-login-btn"
            callback={(response) => onSubmitSignup(AuthMode.Facebook, response, props)}
            render={renderProps => (
              <div onClick={renderProps.onClick}>
                <ReactIconRender className={'ext-login-btn'} color={'#4267B2'} IconComponent={FaFacebookSquare} />
              </div>
            )}
          />
        </div>

        <div className="layout-grid centered-container margin-bottom--20">
          <ValidatedSignupForm onSubmitSignup={(values) => onSubmitSignup(AuthMode.Normal, values, props)} />
        </div>
      </div>
    </Modal>
  )
}

export default SignupModal
